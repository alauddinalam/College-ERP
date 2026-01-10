from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.http import HttpResponseRedirect
from django.conf import settings


def signin(request):
    if request.user.is_authenticated:
        return redirect('myERP:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=email).first()
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('myERP:dashboard')

        messages.error(request, "Invalid email or password")
        return render(request, 'auth.html', {'show': 'signin'})

    return render(request, 'auth.html', {'show': 'signin'})


def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('fname', '').strip()
        email = request.POST.get('email', '').strip().lower()
        roll_no = request.POST.get('rollNo', '').strip()
        password = request.POST.get('pas')
        cfm_password = request.POST.get('cfmPas')

        # ✅ Check password match
        if password != cfm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'auth.html', {'show': 'signup'})

        # ✅ Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'auth.html', {'show': 'signup'})

        # ✅ Create new user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        # ✅ Create or get profile safely
        Profile.objects.get_or_create(user=user, defaults={'roll_no': roll_no})

        messages.success(request, "Account created successfully! Please login.")
        return redirect('accounts:signin')

    return render(request, 'auth.html', {'show': 'signup'})


def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('accounts:signin')
