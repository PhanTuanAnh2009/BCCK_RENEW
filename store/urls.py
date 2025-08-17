from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import  *
urlpatterns = [
    path('',index,name='index'),
    path('add_to_cart/<int:product_id>/',add_to_cart,name='add_to_cart'),

    path('products/', product_list, name='product_list'),
    path('register_custom/', register_view, name='register_custom'),
    path('login_custom/',login_view, name='login_custom'),
    path('logout_custom/',logout_view, name='logout_custom'),
    path('api-learn/',index_api,name='index_api'),
    path('home/',home,name='home'),
    path("nhapsp/",sanpham,name='sanpham'),
    path('product_stt/<int:product_id>/',product_detail, name='product_detail'),
    # path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('api/products/',product_list_api,name="product_list_api"),
    path('api/products/create',product_create_api,name='product_create_api
    path('api/products/update/<int:id>/',product_update_api,name='product_update_api'),
    path('api/products/delete/<int:id>/',product_delete_api,name='product_delete_api')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
