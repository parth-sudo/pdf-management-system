from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('discuss/<int:pk>/', views.discuss, name='discuss'),
    path('post-comment/', views.post_comment, name='post-comment'),
    path('about/', views.about, name='about'),
    path('guest-comment/', views.guest_comment, name='guest-comment'),
]