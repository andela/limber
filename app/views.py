
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from app.models import UserProfile

# Create your views here.


def index(request):
    user_session = request.session.get('user_id', None)
    if user_session and user_session is not None:
        return HttpResponseRedirect('/profile')
    content = {
        'title': 'Welcome'
    }
    return render(request, 'index.html', content)


def user_login(request):

    template = "login.html"
    content = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check for form validation
        if form.is_valid():
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            # Check if a user exists
            user = authenticate(username=user_name, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/profile')
            else:
                # user does not exist, display wrong credentials
                form = LoginForm(request.POST)
                content['title'] = 'Login'
                content['form'] = form
                content['message'] = "Wrong Credentials."

    elif request.method == 'GET':
        form = LoginForm()
        content['title'] = 'Login'
        content['form'] = form

    return render(request, template, content)


def register(request):
    user_session = request.session.get('user_id', None)
    if user_session and user_session is not None:
        return HttpResponseRedirect('/profile')

    template = "register.html"
    content = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_profile = UserProfile.create_user(
                username=username, email=email, password=password)
            if user_profile and user_profile is not None:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponseRedirect('/profile')
            else:
                content['message'] = 'User already exists.'
                form = RegistrationForm(request.POST)
                content['title'] = 'Register'
                content['form'] = form

    elif request.method == 'GET':
        # if the request method is GET
        form = RegistrationForm()
        content['title'] = 'Register'
        content['form'] = form

    return render(request, template, content)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Profile view
@login_required(login_url='/login')
def profile(request):
    content = {}

    template = 'profile.html'
    if request.method == 'GET':
        content['message'] = 'Welcome {}.'.format(
            request.user.username)
        return render(request, template, content)
