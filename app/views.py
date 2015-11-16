from django.shortcuts import render
from .forms import LoginForm, RegistrationForm

# Create your views here.
def index(request):
	content = {
	'title' : 'Welcome'
	}
	return render(request, 'index.html', content)

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			return HttpResponseRedirect('/thanks/')

	else:
		form = LoginForm()

	content = {
		'title' : 'Login',
		'form': form
	}

	return render(request, "login.html", content)

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			
			return HttpResponseRedirect('/thanks/')

	else:
		form = RegistrationForm()

	content = {
		'title' : 'Register',
		'form': form
	}

	return render(request, "register.html", content)
