from django.urls import path
from . import views

app_name = 'analysisApp'
urlpatterns = [
    path('',views.index, name='index'),
    path('/details/<int:product_id>/', views.view_details, name= 'details')
]