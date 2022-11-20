from django.urls import path
from . import views

urlpatterns = [
    path('', views.foward_home, name='foward_home'),
    path('search/', views.search, name='search')
    # path('home/', views.home, name='home'),
    # path('modal/<int:id>/', views.product_detail, name='product_detail'),
    # path('home/keyrecommendation/<int:id>/', views.product_detail, name='keyrecommendation'),
    # path('review/<int:review_id>/', views.review_detail, name='review_select'),
    # path('home/delete/<int:id>', views.delete_product, name='delete_product'),
    # path('trend/<int:id>/', views.trend, name='trend'),
]