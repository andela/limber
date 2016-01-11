from django.shortcuts import render


def index(request):
    return render(request, 'limber/landing.html')


def signup(request):
    return render(request, 'limber/signup.html')
