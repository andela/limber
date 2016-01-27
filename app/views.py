
from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from app.models import UserAuthentication, User
import requests
import jwt
from rest_framework_jwt import utils
from django.http import HttpResponseRedirect

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
            if 'next' in request.GET:
                    return HttpResponseRedirect('{}'.format(request.GET.get("next")))
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

