from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Profile
from .forms import QuickRegistrationForm, QuickLoginForm

def register(request):
    if request.method == 'POST':
        form = QuickRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['nickname'],
                password=form.cleaned_data['password']
            )
            Profile.objects.create(
                user=user,
                nickname=form.cleaned_data['nickname']
            )
            login(request, user)
            return redirect(request.GET.get('next', 'news_list'))
    else:
        form = QuickRegistrationForm()

    return render(request, 'profiles/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = QuickLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['nickname'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'news_list'))
    else:
        form = QuickLoginForm()

    return render(request, 'profiles/login.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('news_list')