from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import  add_to_cart,product_list,index,login_view,register_view,logout_view,sanpham,descrip
urlpatterns = [
    path('',index,name='index'),
    

path('products/', product_list, name='product_list'),
    path('register_custom/', register_view, name='register_custom'),
path('login_custom/',login_view, name='login_custom'),
    path('logout_custom/',logout_view, name='logout_custom'),

    path('descrip/',descrip,name='descrip'),
    path("nhapsp/",sanpham,name='sanpham'),
    
    path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),

  
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
