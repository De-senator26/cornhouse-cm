import json
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai.errors import ClientError

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
        status_code = getattr(e, 'status', None)
        if status_code == 429:
            logger.warning("Gemini quota exhausted.")
            return JsonResponse({
                'reply': '🌽 Sorry, Gemini quota is exhausted. Please check your Google AI billing and quota, or try again later.'
            }, status=429)
        logger.error(f"Gemini ClientError: {e}")
        return JsonResponse({'reply': f'⚠️ AI service error: {str(e)}'}, status=500)
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        return JsonResponse({'reply': f'⚠️ Error: {str(e)}'}, status=500)

@csrf_exempt
def clear_history(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    return JsonResponse({'status': 'cleared'})
