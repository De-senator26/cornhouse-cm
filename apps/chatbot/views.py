import json
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai.errors import ClientError
from .fallback import get_fallback_reply

logger = logging.getLogger(__name__)

def chat_page(request):
    if not request.session.get('access_token'):
        return redirect('login')
    return render(request, 'chatbot/chat.html')

@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            logger.info("GEMINI_API_KEY missing, serving local agricultural fallback.")
            fallback_reply = get_fallback_reply(user_message)
            return JsonResponse({'reply': fallback_reply})

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
        return JsonResponse({'reply': response.text})

    except ClientError as e:
        logger.warning("Gemini ClientError (%s), serving local fallback.", e)
        fallback_reply = get_fallback_reply(user_message)
        return JsonResponse({'reply': fallback_reply})
    except Exception as e:
        logger.error(f"Chatbot error: {e}, serving local fallback.")
        fallback_reply = get_fallback_reply(user_message)
        return JsonResponse({'reply': fallback_reply})


@csrf_exempt
def clear_history(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    return JsonResponse({'status': 'cleared'})
