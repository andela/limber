from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from app.models import User

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
            user_name = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            # Check if a user already exists
            user = User.objects.filter(email=email, user_name=user_name)
            if user:
                # if user does actually exist, notify the user
                content['message'] = 'User already exists.'
            else:
                # Create a new user
                new_user = User.objects.create(
                    user_name=user_name, email=email, password=email, user_type=1)
                if new_user:
                    content['message'] = 'User created successfully.'
                    # Render new layout but ideally we should be calling a new
                    # route
                    template = "profile.html"
    elif request.method == 'GET':
        # if the request method is GET
        form = RegistrationForm()
        content['title'] = 'Register'
        content['form'] = form

    return render(request, template, content)
