from django.shortcuts import render
import jwt
from rest_framework_jwt import utils
from django.http import HttpResponseRedirect


def comfirm_view(request):
    return render(request, 'limber/comfirmation_page.html')


def index(request):
    if 'token' in request.COOKIES:
        try:
            token = request.COOKIES.get('token')
            resp = utils.jwt_decode_handler(token)
            return HttpResponseRedirect('/dashboard/')
        except:
            pass

    return render(request, 'limber/landing.html')


def signup(request):
    if 'token' in request.COOKIES:
        try:
            token = request.COOKIES.get('token')
            resp = utils.jwt_decode_handler(token)
            return HttpResponseRedirect('/dashboard/')
        except:
            return HttpResponseRedirect('/')

    return render(request, 'limber/signup.html')


def login(request):
    if 'token' in request.COOKIES:
        try:
            token = request.COOKIES.get('token')
            resp = utils.jwt_decode_handler(token)
            return HttpResponseRedirect('/dashboard/')
        except:
            return HttpResponseRedirect('/')

    return render(request, 'limber/login.html')


def dashboard(request):
    data = {}
    if 'token' in request.COOKIES:
        try:
            token = request.COOKIES.get('token')
            data['resp'] = utils.jwt_decode_handler(token)
        except jwt.ExpiredSignatureError:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/')

    return render(request, 'limber/projects.html', {'data': data})


def create_project(request):
    data = {}
    if 'token' in request.COOKIES:
        try:
            token = request.COOKIES.get('token')
            data['resp'] = utils.jwt_decode_handler(token)
        except jwt.ExpiredSignatureError:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/signup/')

    return render(request, 'limber/create_project.html', {'data': data})


def respond_project_invite(request, invite_code):
    return render(
        request,
        'limber/invite_response.html',
        {'invite_code': invite_code}
    )

def respond_password_reset(request, reset_code):
    return render(
        request,
        'limber/password_reset_completion.html',
        {'reset_code': reset_code}
    )
