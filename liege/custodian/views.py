from django.shortcuts import redirect, render
from django.http import HttpResponse
# Create your views here.


def index(response):
    return HttpResponse("test custodian")