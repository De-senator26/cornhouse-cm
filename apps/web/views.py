"""Views for the CornHouse web frontend."""
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from apps.users.models import User

def home(request):
    return render(request, 'web/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Build absolute URL for the token endpoint
        token_url = request.build_absolute_uri('/api/token/')
        try:
            # Log the URL being used (visible in Render logs)
            print(f"Attempting login with token_url: {token_url}")
            response = requests.post(token_url, data={'username': username, 'password': password}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                request.session['access_token'] = data.get('access')
                request.session['refresh_token'] = data.get('refresh')
                request.session['user'] = username
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        except requests.exceptions.RequestException as e:
            print(f"Login error: {e}, attempted URL: {token_url}")
            messages.error(request, 'Could not connect to the authentication server.')
    return render(request, 'web/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('home')

def dashboard(request):
    token = request.session.get('access_token')
    if not token:
        return redirect('login')
    username = request.session.get('user')
    try:
        user = User.objects.get(username=username)
        role = user.role
        user_id = user.id
    except User.DoesNotExist:
        role = 'farmer'
        user_id = None
    return render(request, 'web/dashboard.html', {'token': token, 'role': role, 'user_id': user_id})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'web/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'web/register.html')

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered.")
            return render(request, 'web/register.html')

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone,
                role=role,
                is_verified=False
            )
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'web/register.html')

    return render(request, 'web/register.html')

def knowledge_hub(request):
    return render(request, 'web/knowledge_hub.html')

def knowledge_detail(request, article_id):
    token = request.session.get('access_token')
    headers = {}
    if token:
        headers = {'Authorization': f'Bearer {token}'}
    article_url = request.build_absolute_uri(f'/api/knowledge/articles/{article_id}/')
    response = requests.get(article_url, headers=headers)
    if response.status_code == 200:
        article = response.json()
        return render(request, 'web/knowledge_detail.html', {'article': article})
    else:
        return redirect('knowledge_hub')
