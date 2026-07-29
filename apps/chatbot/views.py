import google.generativeai as genai
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from apps.users.models import User
from .models import ChatMessage
import json


def _get_session_user(request):
    """Return the User object for the logged-in session, or None."""
    username = request.session.get('user')
    if not username:
        return None
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def chat_page(request):
    # Redirect to login if not logged in via session
    if not request.session.get('access_token'):
        return redirect('login')

    user = _get_session_user(request)
    history = user.chat_messages.all() if user else []
    return render(request, 'chatbot/chat.html', {'history': history})


def chat_api(request):
    if request.method == 'POST':
        # Guard: must be logged in
        if not request.session.get('access_token'):
            return JsonResponse({'error': 'Not authenticated'}, status=401)

        user = _get_session_user(request)
        if not user:
            return JsonResponse({'error': 'User not found'}, status=401)

        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Save the user's message
            ChatMessage.objects.create(user=user, role='user', content=user_message)

            # Build conversation history for Gemini (last 40 messages = 20 exchanges)
            recent = list(user.chat_messages.order_by('-created_at')[:40])
            recent.reverse()

            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.5-flash')

            system_prompt = (
                "You are an agricultural assistant for CornHouse, helping rural maize farmers in Cameroon. "
                "Answer questions in simple, clear language (English or French). "
                "If the question is not about agriculture, politely redirect to farming topics."
            )

            # Reconstruct multi-turn Gemini history (all but the current message)
            chat_history = []
            for msg in recent[:-1]:
                gemini_role = 'user' if msg.role == 'user' else 'model'
                chat_history.append({'role': gemini_role, 'parts': [msg.content]})

            chat = model.start_chat(history=chat_history)
            full_message = f"{system_prompt}\n\nQuestion: {user_message}" if not chat_history else user_message
            response = chat.send_message(full_message)
            bot_reply = response.text

            # Save the bot's reply
            ChatMessage.objects.create(user=user, role='bot', content=bot_reply)

            return JsonResponse({'reply': bot_reply})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def clear_history(request):
    """Delete all chat messages for the current session user."""
    if request.method == 'POST':
        if not request.session.get('access_token'):
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        user = _get_session_user(request)
        if user:
            user.chat_messages.all().delete()
        return JsonResponse({'status': 'cleared'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
