"""Views for the CornHouse web frontend."""
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.conf import settings
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User

logger = logging.getLogger(__name__)


def home(request):
    """Render the CornHouse home page."""
    return render(request, 'web/home.html')


def _issue_jwt_for_user(user):
    """Generate a JWT access/refresh pair directly for an authenticated User object.

    This avoids the fragile self-HTTP request to /api/token/ which can fail
    due to network issues, host resolution, or misconfigured ports.
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def login_view(request):
    """Authenticate the user and store JWT tokens in session."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'web/login.html')

        # Authenticate directly against the database — no HTTP round-trip needed.
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, 'Your account has been deactivated. Please contact support.')
                return render(request, 'web/login.html')
            # Issue JWT tokens directly (no self-HTTP call)
            try:
                access_token, refresh_token = _issue_jwt_for_user(user)
            except Exception as exc:
                logger.error("JWT generation failed for %s: %s", username, exc)
                messages.error(request, 'Login succeeded but token generation failed. Please try again.')
                return render(request, 'web/login.html')

            login(request, user)
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            request.session['user'] = username
            return redirect('dashboard')
        else:
            # Give a clearer error so users know what went wrong.
            try:
                db_user = User.objects.get(username=username)
                # User exists but password is wrong
                logger.warning("Failed login attempt for existing user: %s", username)
                messages.error(request, 'Incorrect password. Please try again.')
            except User.DoesNotExist:
                messages.error(request, 'No account found with that username. Please register first.')

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
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        role = request.POST.get('role', 'farmer')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        # Validate role against allowed choices
        allowed_roles = [r[0] for r in User.ROLE_CHOICES]
        if role not in allowed_roles:
            role = 'farmer'

        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'web/register.html')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'web/register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'web/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another.')
            return render(request, 'web/register.html')

        if phone and User.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered.')
            return render(request, 'web/register.html')

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone,
                role=role,
                is_verified=False,
            )
            messages.success(request, f'Account created successfully! Welcome, {username}. Please log in.')
            return redirect('login')
        except DatabaseError as exc:
            logger.error("Registration DatabaseError for %s: %s", username, exc)
            messages.error(request, f'Database error: {exc}')
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
    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        if response.status_code == 200:
            article = response.json()
            return render(request, 'web/knowledge_detail.html', {'article': article})
    except requests.exceptions.RequestException as exc:
        logger.error("Knowledge detail fetch failed for article %s: %s", article_id, exc)
    return redirect('knowledge_hub')
