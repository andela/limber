
from django.shortcuts import render
from django.http import HttpResponse
#from django.template import RequestContext, loader


# Create your views here.
def index1(request):
	return render(request,"test.html")
