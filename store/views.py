from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import locale
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')


   

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    cart = request.session.get('cart', [])
    cart.append({
        "id": product.id,
        "name": product.name,
        "price": int(product.price),
        "image_url":product.image.url,
        "quantity": quantity,
    })
    request.session['cart'] = cart

  
    notifications = request.session.get('notifications', [])
    notifications.insert(0, f"Bạn đã thêm '{product.name}' vào giỏ hàng.")
    request.session['notifications'] = notifications[:5] 

    return render(request, 'store/pay.html')


def product_list(request):
    keyword = request.GET.get('q', '').strip()
    if keyword:
        products = Product.objects.filter(name__icontains=keyword)
    else:
        products = Product.objects.all()
    for p in products:
        formatted = locale.currency(p.price, grouping=True)
        print(formatted)
        if formatted.endswith(',00 ₫'):
            formatted = formatted.replace(',00 ₫', ' ₫')
        p.formatted_price = formatted

    stars = range(1, 6)   
    return render(request, 'store/products.html', {
        'products': products,
        'stars': stars,
    })



def index_api(request):
    return render(request,'store/api-learn.html')
def product_list_api(request):
    
    keyword = request.GET.get('q', '').strip()
    if keyword:
        products = Product.objects.filter(name__icontains=keyword)
    else:
        products = Product.objects.all()
    data=[]
    for p in products:
        
        data.append({
            'id':p.id,
            'name':p.name,
            'price':p.price,
          
            'stock':p.stock,
            'descrip':p.descrip,
            'image':p.image.url if p.image else ''
        })
    return JsonResponse(data,safe=False)
@csrf_exempt

@csrf_exempt
def thanhtoan(request):
    products=Product.objects.all()
    data=[]
    for p in products:
        
        data.append({
            'id':p.id,
            'name':p.name,
            'price':p.price,
            'quantity':p.quantity,    
            'stock':p.stock,
            'descrip':p.descrip,
            'image':p.image.url if p.image else ''
        })
    return JsonResponse(data,safe=False)

def product_delete_api(request,id):
    p=get_object_or_404(Product,id=id)
    if request.method=='POST':
        p.delete()
        return JsonResponse({'message':'Deleted'})
    return JsonResponse({'error' : 'POST required'},status=400)
@csrf_exempt
def product_update_api(request,id):
    p = get_object_or_404(Product,id=id)
    if request.method=='POST':
        print("???")
        print(request.POST)
        p.name=request.POST.get('name',p.name)
        p.price=request.POST.get('price',p.price)
       
        p.stock=request.POST.get('stock',p.stock)
        print(request.POST.get('price'))
        if 'image' in request.FILES:
            p.image=request.FILES['image']
        p.save()
        return JsonResponse({'message':'Updated'})
    return JsonResponse({'error':'POST required'},status=400)
@csrf_exempt
def product_create_api(request):
    name=request.POST.get('name')
    price=request.POST.get('price')
    stock=request.POST.get('stock',10)
    descrip=request.POST.get('descrip')
    image=request.FILES.get('image')
    
    #tao doi tuong 
    product=Product.objects.create(name=name,price=price,stock=stock,descrip=descrip,image=image)
    return JsonResponse({'message':'thanh cong',"id":product.id})
def index(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    if not user_id:
        
        return redirect('login_custom')

    
    context = {'username': username}
    return redirect('product_list')



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

     
        if not username or not email or not password or not password_confirm:
            messages.error(request, "Vui lòng điền đủ thông tin.")
            return redirect('register_custom')

        if password != password_confirm:
            messages.error(request, "Mật khẩu nhập lại không khớp.")
            return redirect('register_custom')


        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username đã được sử dụng.")
            return redirect('register_custom')

        
        user = CustomUser(username=username, email=email)
        user.set_password(password) 
        user.save()

        messages.success(request, f"Đăng ký thành công! Chào mừng {username}")
      
        request.session['user_id'] = user.id  
        request.session['username'] = user.username
        return redirect('index')

    return render(request, 'store/custom_register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
            return redirect('login_custom')

     
        if user.check_password(password):
           
            print('đăng nhập thành công')
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            messages.success(request, f"Chào mừng {username}!")
            return redirect('product_list')
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
            return redirect('login_custom')

    return render(request, 'store/custom_login.html')


def logout_view(request):
    request.session.flush()  
    messages.success(request, "Đăng xuất thành công.")
    return redirect('login_custom')


# def product(request):
#     if request.method == "POST":
        
#         if 'product_id' in request.POST and request.POST['product_id']:
#             product_id = request.POST['product_id']
#             product = get_object_or_404(Product, id=product_id)
            
#             product.name = request.POST['name']
#             product.price = request.POST['price']
#             product.stock = request.POST['stock']
#             if 'image' in request.FILES:
#                 product.image = request.FILES['image']
#             product.save()
#             return redirect('product')
#         else:
            
#             name = request.POST['name']
#             price = request.POST['price']
#             stock = request.POST['stock']
#             image = request.FILES.get('image')
#             product = Product(name=name, price=price, stock=stock, image=image)
#             product.save()
#             return redirect('product')

#     products = Product.objects.all()

  
#     product = Product()

#     context = {
#         'products': products,
#         'product': product  
#     }

#     return render(request, 'store/product.html', context)


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('product')
def product_detail(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    formatted = locale.currency(product.price, grouping=True)

    
    return render(request, 'store/descrip.html', {
        'product': product,
        'formatted_price': formatted,
    })
def home(request):
    return render(request, 'store/index.html')

def sanpham(request):
    if request.method=="POST":
        name = request.POST['name']
        price = request.POST['price']
        stock = request.POST['stock']
        descrip=request.POST['descrip']
        image = request.FILES.get('image')
        product = Product(name=name, price=price, stock=stock,descrip=descrip, image=image)
        product.save()
        return redirect('sanpham')

    products = Product.objects.all()

  
    product = Product()

    context = {
        'products': products,
        'product': product  
    }

    return render(request, 'store/nhapsp.html', context)

def timKiem(request)  :
    keyword = request.GET.get('q', '').strip()

    if keyword:
        products = Product.objects.filter(name__icontains=keyword)
    else:
        products = Product.objects.all()

    return render(request, 'products.html', {
        'products': products,
    })
