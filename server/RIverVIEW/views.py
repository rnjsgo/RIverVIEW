# from functions import *
from django.shortcuts import render, redirect
from .models import ProductModel, ReviewModel, ProductKeyword
import re
# from viz_trend import *
from collections import Counter, defaultdict

def foward_home(request):
    if request.method == 'GET':
        T_Products = [ProductModel.objects.all().order_by('-search_value')[i * 5:i * 5 + 5] for i in range(4)]
        R_Products = [ProductModel.objects.all().order_by('-created_at')[i * 5:i * 5 + 5] for i in range(4)]
        return render(request, 'RIverVIEW/main.html')

