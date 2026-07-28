import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import json

def chat_page(request):
    return render(request, 'chatbot/chat.html')

def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""You are an agricultural assistant for CornHouse, helping rural maize farmers in Cameroon. 
Answer the following question in simple, clear language (English or French). If the question is not about agriculture, 
politely redirect to farming topics.
Question: {user_message}"""
            
            response = model.generate_content(prompt)
            return JsonResponse({'reply': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
