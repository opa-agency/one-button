from django.shortcuts import render


def home_page_view_two(request):
    return render(request, "applicationtwo/home.html")
