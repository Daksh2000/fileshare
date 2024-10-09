from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    # Registration, login, and logout
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='fileupload/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # File management views
    path('upload/', views.upload_file, name='upload-file'),
    path('files/', views.file_list, name='file-list'),
    path('delete/<int:pk>/', views.delete_file, name='delete-file'),
    path('share/<int:pk>/', views.share_file, name='share-file'),

    # Publicly shared file view
    path('public/<str:public_url>/', views.public_file, name='public-file'),
]
