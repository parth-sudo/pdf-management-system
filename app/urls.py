from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('discuss/<int:pk>/', views.discuss, name='discuss'),
    path('post-comment/', views.post_comment, name='post-comment'),
    path('share-pdf/<int:pdf_id>/', views.share_pdf, name='share-pdf'),
]