from uuid import uuid4

from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse
from django.urls import reverse
from requests import request


# Create your views here.
def home_page_view(request):
    print(f"Request token: {request.session.get('token')}")
    token = request.session.get('token')
    if request.method == "GET":
        if not token:
            token = uuid4().hex
            request.session['token'] = token
        return render(request, "home.html", {"token": request.session['token']})

    elif request.method == "POST":
        if not token:
            return HttpResponseNotAllowed("No token in session")
        print("Checkout submitted!")
        return HttpResponse("Checkout submitted!")


def dashboard_view(request):
    return render(request, "dashboard.html")

