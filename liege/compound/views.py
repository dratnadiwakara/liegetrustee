from django.shortcuts import render,HttpResponse

def index(request):
    return render(request,"compound/compound_home.html")