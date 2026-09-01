import json
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai.errors import ClientError
from apps.users.models import User
from .models import ChatMessage
from .fallback import get_fallback_reply

logger = logging.getLogger(__name__)


def _get_request_user(request):
    """Retrieve user object from request.user or session username."""
    if hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    username = request.session.get('user')
    if username:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    return None


def chat_page(request):
    if not request.session.get('access_token'):
        return redirect('login')

    user = _get_request_user(request)
    history = []
    question_count = 0

    if user:
        try:
            messages_qs = ChatMessage.objects.filter(user=user).order_by('created_at')
            history = [{'role': m.role, 'content': m.content} for m in messages_qs]
            question_count = ChatMessage.objects.filter(user=user, role='user').count()
        except Exception as exc:
            logger.error("Error loading chat history for user %s: %s", user, exc)
            history = []
            question_count = 0
    else:
        question_count = request.session.get('question_count', 0)

    return render(request, 'chatbot/chat.html', {
        'history': history,
        'question_count': question_count
    })


@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        try:
            data = json.loads(request.body.decode('utf-8') if request.body else '{}')
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        user = _get_request_user(request)

        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            logger.info("GEMINI_API_KEY missing, serving local agricultural fallback.")
            reply = get_fallback_reply(user_message)
        else:
            try:
                client = genai.Client(api_key=api_key)
                model_name = 'gemini-2.0-flash'
                prompt = f"""You are an agricultural assistant for CornHouse, helping rural maize farmers in Cameroon.
Answer the following question in simple, clear language (English or French). If the question is not about agriculture,
politely redirect to farming topics.
Question: {user_message}"""

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                reply = response.text
            except ClientError as e:
                logger.warning("Gemini ClientError (%s), serving local fallback.", e)
                reply = get_fallback_reply(user_message)
            except Exception as e:
                logger.error(f"Chatbot error: {e}, serving local fallback.")
                reply = get_fallback_reply(user_message)

        # Save to database if authenticated
        if user:
            ChatMessage.objects.create(user=user, role='user', content=user_message)
            ChatMessage.objects.create(user=user, role='bot', content=reply)
            question_count = ChatMessage.objects.filter(user=user, role='user').count()
        else:
            session_count = request.session.get('question_count', 0) + 1
            request.session['question_count'] = session_count
            question_count = session_count

        return JsonResponse({'reply': reply, 'question_count': question_count})

    except Exception as e:
        logger.error(f"Unexpected chat API error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def clear_history(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    user = _get_request_user(request)
    if user:
        ChatMessage.objects.filter(user=user).delete()

    request.session['question_count'] = 0
    return JsonResponse({'status': 'cleared', 'question_count': 0})

