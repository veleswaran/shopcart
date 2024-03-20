import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from shop.form import CustomUserForm
from .models import *
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def index(request):
    product = Product.objects.filter(trending =0)
    return render(request,'index.html',{'product':product})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            pwd = request.POST.get('password')
            user = authenticate(request,username=name,password = pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully')
                return redirect('/')
            else:
                messages.error(request,'Invalid User Name or Password')
                return render(request,'shop/login.html')
        return render(request,'shop/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')


def register(request):
    form = CustomUserForm()
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registeration success you can login now')
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})


def collections(request):
    catagory =Category.objects.filter(status=0)
    return render(request,'shop/collections.html', {'category':catagory})


def collectionsview(request,name):
    if Category.objects.filter(name=name,status=0):
        products = Product.objects.filter(category__name = name)
        return render(request,'shop/product/products.html', {'products':products,'category_name':name})
    else:
        messages.warning(request,'No such catagory')
        return redirect('collections')
    
# def product_details(request, category, product):
#     category_exists = Category.objects.filter(name=category, status=0).exists()
#     if category_exists:
#         product_instance = get_object_or_404(Product, name=product, status=0)
#         return render(request, 'shop/product/productdetail.html', {'product': product_instance})
#     else:
#         messages.error(request, "No such category found")
#         return redirect('collections')
    
def product_details(request,category,product):
    if Category.objects.filter(name=category,status=0):
        if Product.objects.filter(name = product,status=0):
            products = Product.objects.filter(name = product,status = 0 ).first()
            return render(request,'shop/product/productdetail.html', {'products':products})
        else:
            messages.error(request,"no such product found")
            return redirect('collections')
    else:   
        messages.error(request,"No such catagory Found")
        return redirect('collections')
    

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data= json.loads(request.body)
            product_id = data['pid']
            product_qty = data['product_qty']
            print(product_id,product_qty)
            print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added in Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Avaoilable'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request,'shop/cartpage.html',{'cart':cart})
    
    else:
        return redirect('/')
    
def remove_cart(request,cid):
    cart = Cart.objects.get(id=cid)
    cart.delete()
    return redirect('cart_page')

def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data= json.loads(request.body)
            product_id = data['pid']
            print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added in Favourite'},status=200)       
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def fav_view(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request,'shop/fav.html',{'fav':fav})
    
    else:
        return redirect('/')

def remove_fav(request,cid):
    fav = Favourite.objects.get(id=cid)
    fav.delete()
    return redirect('fav_view_page')