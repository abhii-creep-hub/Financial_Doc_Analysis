from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    name="super user"
    # products = product.object.all()
    return render(request, "home.html", )

def about(request):
    return HttpResponse("This is about page")

