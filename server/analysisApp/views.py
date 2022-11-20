from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    return HttpResponse("hello")

def view_details(request, product_id):
    product = ProductModel.objects.get(product_id= product_id)
    context = {'product': product}
    return render(request, 'analysisApp/product_details.html',context)