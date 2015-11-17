from django.shortcuts import render

# Create your views here.
def index(request):
	content = {
		"title" : "Welcome"
	}
	return render(request, "index.html", content)


def sign_up(request):
	content = {
		"title" : "Welcome"
	}
	return render(request, "index.html", content)
