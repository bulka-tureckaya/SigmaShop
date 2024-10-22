from django.shortcuts import render, redirect
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, login, logout
from django.shortcuts import resolve_url

from .forms import UserUpdateForm, SignupForm, LoginForm

@login_required(login_url='/profile/login')
def profile(request):
    current_user = request.user

    return render(request, 'user_profile/profile.html', {'current_user': current_user})

def edit(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('user_profile:profile')

    else:
        form = UserUpdateForm(instance=current_user)

    return render(request, 'user_profile/edit.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile:profile')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

class LoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return resolve_url('/')
    
@login_required(login_url='/profile/login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')