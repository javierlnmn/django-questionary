from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.models import CustomUser

def login_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        login(request, user)
        return redirect('common:index')
    except Exception:
        return redirect('users:login') 