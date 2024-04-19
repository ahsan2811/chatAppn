from django.shortcuts import render, redirect
from django.contrib import auth
from .models import Account, UserProfile
from django.contrib.auth.decorators import login_required
from chat.models import FriendRequest
# Create your views here.

def login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method=="POST":
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password=request.POST.get('password')
        print(password)
        username=email.split("@")[0]
        user=Account.objects.create(first_name=first_name, last_name=last_name,
                                    email=email, username=username,
                                    password=password)
        user.set_password(password)
        user.is_active=True
        user.save()
        user_profile=UserProfile.objects.create(user=user)
        user_profile.save()
        return redirect('login')
    else:
        return render(request,'register.html')

def user_profile(request):
    profile=UserProfile.objects.get(user=request.user)
    friend_requests=FriendRequest.objects.filter(receiver=request.user)
    context={'profile': profile,
             'friend_requests': friend_requests}
    return render(request, 'user_profile.html', context)

def change_profile_picture(request):
    if request.method=="POST":
        profile_picture=request.FILES.get("profile_picture")
        user_profile=UserProfile.objects.get(user=request.user)
        user_profile.profile_picture=profile_picture
        user_profile.save()
        return redirect('user_profile')    