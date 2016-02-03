from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from app.models import UserAuthentication, User
import requests
import jwt
from rest_framework_jwt import utils
from django.http import HttpResponseRedirect

# Create your views here.


def comfirm_view(request):
    return render(request, 'limber/comfirmation_page.html')


def index(request):
    cookie = request.COOKIES.has_key('token')
    if cookie:
        try:
            token = request.COOKIES.get('token')
            resp = utils.jwt_decode_handler(token)
            return HttpResponseRedirect('/dashboard/')
        except:
            pass
            # return HttpResponseRedirect('/')

    return render(request, 'limber/landing.html')


def signup(request):
    cookie = request.COOKIES.has_key('token')
    if cookie:
        try:
            token = request.COOKIES.get('token')
            resp = utils.jwt_decode_handler(token)
            return HttpResponseRedirect('/dashboard/')
        except:
            return HttpResponseRedirect('/')

    return render(request, 'limber/signup.html')


def dashboard(request):
    cookie = request.COOKIES.has_key('token')
    data = {}
    if cookie:
        try:
            token = request.COOKIES.get('token')
            data['resp'] = utils.jwt_decode_handler(token)
        except jwt.ExpiredSignatureError:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/signup/')

    return render(request, 'limber/projects.html', {'data': data})

def create_project(request):
    cookie = request.COOKIES.has_key('token')
    data = {}
    if cookie:
        try:
            token = request.COOKIES.get('token')
            data['resp'] = utils.jwt_decode_handler(token)
        except jwt.ExpiredSignatureError:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/signup/')

    return render(request, 'limber/create_project.html', {'data': data})