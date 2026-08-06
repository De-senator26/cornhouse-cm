"""URLs for the CornHouse web frontend."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('knowledge/', views.knowledge_hub, name='knowledge_hub'),
    path('knowledge/<int:article_id>/', views.knowledge_detail, name='knowledge_detail'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
]