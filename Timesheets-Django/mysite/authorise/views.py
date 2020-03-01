from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect


def landing(request):
    return render(request, 'authorise/landing.html')

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')