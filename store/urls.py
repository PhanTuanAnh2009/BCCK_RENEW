from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import  product_list,index,login_view,register_view,logout_view,sanpham,product_detail,home
urlpatterns = [
    path('',index,name='index'),
    

path('products/', product_list, name='product_list'),
    path('register_custom/', register_view, name='register_custom'),
path('login_custom/',login_view, name='login_custom'),
    path('logout_custom/',logout_view, name='logout_custom'),

    path('home/',home,name='home'),
    path("nhapsp/",sanpham,name='sanpham'),
    path('product_stt/<int:product_id>/',product_detail, name='product_detail'),
    # path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),

  
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
