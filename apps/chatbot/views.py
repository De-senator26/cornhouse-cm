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
            return JsonResponse({'error': 'No message'}, status=400)

        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            logger.error("GEMINI_API_KEY missing")
            return JsonResponse({'reply': '⚠️ API key not configured. Please contact admin.'})

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
        # Some versions of the genai ClientError expose different attributes
        status_code = getattr(e, 'status', None) or getattr(e, 'status_code', None)
        if status_code is None and getattr(e, 'args', None):
            first_arg = e.args[0]
            if isinstance(first_arg, int):
                status_code = first_arg

        logger.error(
            "Gemini ClientError: %s %s. %s",
            getattr(e, 'status', None),
            getattr(e, 'status_code', None),
            getattr(e, 'response', None) or getattr(e, 'body', None) or e.args,
        )

        # Some ClientError variants set a string status like 'RESOURCE_EXHAUSTED'
        status_text = getattr(e, 'status', None) or getattr(e, 'status_text', None)
        if isinstance(status_text, str) and 'RESOURCE_EXHAUSTED' in status_text.upper():
            status_code = 429

        # Also inspect the error text for numeric 429
        if status_code is None:
            if '429' in str(e):
                status_code = 429

        if status_code == 429:
            logger.warning("Gemini quota exhausted, serving local fallback.")
            # Pass the user message so keyword-based farming tips are returned
            fallback_reply = get_fallback_reply(user_message)
            return JsonResponse({'reply': fallback_reply})

        return JsonResponse({'reply': f'⚠️ AI service error: {str(e)}'}, status=500)
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        return JsonResponse({'reply': f'⚠️ Error: {str(e)}'}, status=500)

@csrf_exempt
def clear_history(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    return JsonResponse({'status': 'cleared'})
