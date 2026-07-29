import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
import json


@login_required
def chat_page(request):
    # Load all previous messages for this user, ordered oldest → newest
    history = request.user.chat_messages.all()
    return render(request, 'chatbot/chat.html', {'history': history})


@login_required
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Save the user's message
            ChatMessage.objects.create(
                user=request.user,
                role='user',
                content=user_message,
            )

            # Build conversation history for Gemini (last 20 exchanges = 40 messages)
            recent = request.user.chat_messages.order_by('-created_at')[:40]
            recent = list(reversed(recent))

            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.5-flash')

            system_prompt = (
                "You are an agricultural assistant for CornHouse, helping rural maize farmers in Cameroon. "
                "Answer questions in simple, clear language (English or French). "
                "If the question is not about agriculture, politely redirect to farming topics."
            )

            # Reconstruct the chat using Gemini's multi-turn history format
            chat_history = []
            for msg in recent[:-1]:  # all but the current message
                gemini_role = 'user' if msg.role == 'user' else 'model'
                chat_history.append({
                    'role': gemini_role,
                    'parts': [msg.content],
                })

            chat = model.start_chat(history=chat_history)
            response = chat.send_message(
                f"{system_prompt}\n\nQuestion: {user_message}"
                if not chat_history
                else user_message
            )
            bot_reply = response.text

            # Save the bot's reply
            ChatMessage.objects.create(
                user=request.user,
                role='bot',
                content=bot_reply,
            )

            return JsonResponse({'reply': bot_reply})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def clear_history(request):
    """Delete all chat messages for the current user."""
    if request.method == 'POST':
        request.user.chat_messages.all().delete()
        return JsonResponse({'status': 'cleared'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
