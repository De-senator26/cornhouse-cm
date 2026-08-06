"""Views for the CornHouse web frontend."""
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.db.models import Avg, Count
from django.conf import settings
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from .models import UserFeedback

logger = logging.getLogger(__name__)


def home(request):
    """Render the CornHouse home page with recent user feedback & testimonials."""
    public_reviews = UserFeedback.objects.filter(is_public=True)[:6]
    stats = UserFeedback.objects.filter(is_public=True).aggregate(
        avg_rating=Avg('rating'),
        total_count=Count('id')
    )
    avg_rating = round(stats['avg_rating'] or 5.0, 1)
    total_count = stats['total_count'] or 0

    return render(request, 'web/home.html', {
        'reviews': public_reviews,
        'avg_rating': avg_rating,
        'total_reviews': total_count,
    })


def submit_feedback(request):
    """Process user feedback submission."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        role = request.POST.get('role', 'farmer')
        category = request.POST.get('category', 'general')
        comment = request.POST.get('comment', '').strip()

        try:
            rating = int(request.POST.get('rating', 5))
            if rating < 1 or rating > 5:
                rating = 5
        except (ValueError, TypeError):
            rating = 5

        if not comment:
            messages.error(request, 'Please enter your feedback comments before submitting.')
            next_url = request.META.get('HTTP_REFERER', '/')
            return redirect(next_url)

        user = request.user if request.user.is_authenticated else None

        # Build display name if empty
        if not name:
            if user:
                name = user.username
            else:
                name = "Anonymous Farmer"

        UserFeedback.objects.create(
            user=user,
            name=name,
            role=role,
            rating=rating,
            category=category,
            comment=comment,
            is_public=True
        )

        messages.success(request, '🎉 Thank you for your feedback! Your review helps us improve CornHouse for everyone.')
        next_url = request.META.get('HTTP_REFERER', '/')
        return redirect(next_url)

    return redirect('home')


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

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, 'Your account has been deactivated. Please contact support.')
                return render(request, 'web/login.html')
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
            try:
                User.objects.get(username=username)
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
