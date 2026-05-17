from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class SecretDataView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        current_user = request.user.username
        
        return Response({
            "message": f"Hello {current_user}, you successfully authenticated with a JWT!"
        })
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password is incorrect.')
            
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def dashboard_view(request):
    user_role = request.user.profile.role

    context = {
        'username': request.user.username,
        'role': user_role,
    }

    return render(request, 'accounts/dashboard.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
