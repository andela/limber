from django.shortcuts import render

# Create your views here.
def index(request):
	content = {
		"title" : "Welcome"
	}
	return render(request, "index.html", content)

def login(request):
	content = {
		"title" : "Login"
	}
	return render(request, "login.html", content)

def register(request):
	content = {
		"title" : "Register"
	}
	return render(request, "register.html", content)
