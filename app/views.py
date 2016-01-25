
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from app.models import UserAuthentication, User
import requests

# Create your views here.
def register_member_to_org(request):
    #import ipdb; ipdb.set_trace()

    if request.method == "GET":
        if 'code' in request.GET:
            code = request.GET.get('code')
            import ipdb; ipdb.set_trace()
            response = requests.get("http://127.0.0.1:8000/api/orginvite/{}/?register=".format(code))
            if response.status_code == 200:
                return HttpResponseRedirect('/profile')
            if response.status_code == 428 :
                return HttpResponseRedirect('/register/')
                
            if response.status_code == 403:
                return HttpResponseRedirect("/login/?next=/api/org_registration/?code={}".format(code))

            return HttpResponseRedirect('/profile')



def index(request):
    """Homepage."""
    user_session = request.session.get('user_id')
    if user_session and user_session is not None:
        return HttpResponseRedirect('/profile')
    content = {
        'title': 'Welcome'
    }
    return render(request, 'index.html', content)


def user_login(request):
    """Process user login."""
    template = "login.html"
    content = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check for form validation
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            # Check if a user exist

            user = authenticate(email=email, password=password)
         
            
            if user:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect('{}'.format(request.GET.get("next")))
                

                return HttpResponseRedirect('/api')
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

    return render(request, 'login.html', content)


def register(request):
    """Process user registration."""
    user_session = request.session.get('user_id')
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
            user_profile = User.create_userprofile(
                username=username, email=email, password=password)
            if user_profile and user_profile is not None:
                user = authenticate(email=email, password=password)
                if user:
                    login(request, user)
                    return HttpResponseRedirect('/api')
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
    """User logout."""
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def profile(request):
    """Profile view."""
    content = {}

    template = 'profile.html'
    if request.method == 'GET':
        content['message'] = 'Welcome {}.'.format(
            request.user.email)
        return render(request, template, content)
