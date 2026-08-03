"""Views for the CornHouse web frontend."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.conf import settings
import requests
from apps.users.models import User

def home(request):
    """Render the CornHouse home page."""
    return render(request, 'web/home.html')

def login_view(request):
    """Authenticate the user and store JWT tokens in session."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Always use internal URL on Render (port 10000)
        if settings.DEBUG:
            token_url = request.build_absolute_uri('/api/token/')
        else:
            token_url = 'http://127.0.0.1:10000/api/token/'
        try:
            response = requests.post(token_url, data={'username': username, 'password': password}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                request.session['access_token'] = data.get('access')
                request.session['refresh_token'] = data.get('refresh')
                request.session['user'] = username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        except requests.exceptions.RequestException as e:
            print(f"Login error: {e}, attempted URL: {token_url}")
            messages.error(request, 'Could not connect to the authentication server.')
    return render(request, 'web/login.html')

def logout_view(request):
    """Clear session and redirect to the home page."""
    request.session.flush()
    return redirect('home')

def dashboard(request):
    """Render the authenticated user dashboard."""
    token = request.session.get('access_token')
    if not token:
        return redirect('login')
    username = request.session.get('user')
    try:
        user = User.objects.get(username=username)
        role = user.role
        user_id = user.id
    except ObjectDoesNotExist:
        role = 'farmer'
        user_id = None
    return render(request, 'web/dashboard.html', {'token': token, 'role': role, 'user_id': user_id})

def register_view(request):
    """Handle new user registration."""
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
        except DatabaseError as e:
            messages.error(request, f"Database error: {str(e)}")
            return render(request, 'web/register.html')

    return render(request, 'web/register.html')

def knowledge_hub(request):
    """Render the knowledge hub page."""
    return render(request, 'web/knowledge_hub.html')

def knowledge_detail(request, article_id):
    """Render a single knowledge article detail page."""
    token = request.session.get('access_token')
    headers = {}
    if token:
        headers = {'Authorization': f'Bearer {token}'}
    if settings.DEBUG:
        article_url = request.build_absolute_uri(f'/api/knowledge/articles/{article_id}/')
    else:
        article_url = f'http://127.0.0.1:10000/api/knowledge/articles/{article_id}/'
    response = requests.get(article_url, headers=headers, timeout=10)
    if response.status_code == 200:
        article = response.json()
        return render(request, 'web/knowledge_detail.html', {'article': article})
    else:
        return redirect('knowledge_hub')
