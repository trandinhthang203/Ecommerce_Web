from django.shortcuts import render 
from django.http import HttpResponse
from .models import *
import json

# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/home.html', context)

def cart(request):
    account = request.user.acount
    cart = Cart.objects.all()
    items = Cart_Item.objects.all()
    context = {'items': items, 'cart': cart}
    return render(request, 'app/cart.html', context)

def checkout(request):
    account = request.user.acount
    cart = Cart.objects.all()
    items = Cart_Item.objects.all()
    context = {'items': items, 'cart': cart}
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    acount = request.user.acount
    product = Product.objects.get(id = productId)
    cart = Cart.objects.all()
    items = Cart_Item.objects.all()
    if action == 'add':
        Cart_Item.quantity += 1
    elif action == 'remote':
        Cart_Item.quantity -= 1
    Cart_Item.save()

def detail(request):
    idd = request.GET.get('id', '')
    products = Product.objects.filter(id = idd)
    context = {'products': products}
    return render(request, 'app/detail.html', context)
