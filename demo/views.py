from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, RememberMeToken
import hashlib
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

def account_recovery(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            hint = user.userprofile.password_hint
            return render(request, 'hint.html', {'hint': hint})
    return render(request, 'account_recovery.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'remember_me' in request.POST:
                token = hashlib.sha256(user.username.encode()).hexdigest()
                RememberMeToken.objects.update_or_create(user=user, defaults={'token': token})
                response = redirect('home')
                response.set_cookie('remember_me', token, max_age=30*24*60*60)
                return response
            return redirect('home')
    return render(request, 'login.html')

def insecure_storage(request):
    users_with_same_password = []
    if request.method == 'POST':
        password = request.POST.get('password')
        users = User.objects.all()
        for user in users:
            if check_password(password, user.password):
                users_with_same_password.append(user.username)
    return render(request, 'insecure_storage.html', {'users_with_same_password': users_with_same_password})

@login_required
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')
