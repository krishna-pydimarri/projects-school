from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from polls.models import Choice, Question


def index(request):
    #print(request)
    return HttpResponse( Question.objects.all())#"Hello, I am Krishna. You're at the polls index.")