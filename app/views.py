from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from app.models import UserProfile

# Create your views here.


def index(request):
    content = {
        'title': 'Welcome'
    }
    return render(request, 'index.html', content)


def login(request):
    template = "login.html"
    content = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check for form validation
        if form.is_valid():
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            # Check if a user exists
            user = User.objects.filter(
                user_name=user_name, password=password).values('user_name', 'user_id')
            if user:
                # the user exists, redirect to profile page
                template = "profile.html"
                content['message'] = "Welcome {}".format(user[0]['user_name'])
            else:
                # user does not exist, display wrong credentials
                content['message'] = "Wrong Credentials."

    elif request.method == 'GET':
        form = LoginForm()
        content['title'] = 'Login'
        content['form'] = form

    return render(request, template, content)


def register(request):
    template = "register.html"
    content = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            # Check if a user already exists
            # try:
            user = User.objects.create_user(username,email,password)
            user_profile = UserProfile.objects.create(user=user, user_type=1)
            if user_profile and user_profile is not None:
                content['message'] = 'User created successfully.'
                #redirect
                template = "profile.html"
            else:
                content['message'] = 'User already exists.'
            
    elif request.method == 'GET':
        # if the request method is GET
        form = RegistrationForm()
        content['title'] = 'Register'
        content['form'] = form

    return render(request, template, content)
