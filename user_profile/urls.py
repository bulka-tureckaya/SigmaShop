from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('user_profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit, name='edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]