from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product
# Create your views here.
def home(request):
    context = {}
    return render(request, 'app/home.html', context)

def cart(request):
    context = {}
    return render(request, 'app/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'app/checkout.html', context)
#dan
def product_list(request):
    items_product = Product.objects.all()
    search_query = request.GET.get('search_query')

    if search_query:
        items_product = Product.objects.filter(name__icontains=search_query)

    return render(request, 'app/product_list.html', {"items_product": items_product})

def product_create(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES['image']  # Sử dụng request.FILES để lấy tệp hình ảnh
        status = request.POST['status']

        item_product = Product(name=name, description=description, price=price, image=image, status=status)
        item_product.save()

        messages.success(request,'sản phẩm đã được tạo thành công!')
        return redirect('/list')  # Chuyển hướng tới trang danh sách sản phẩm sau khi tạo
    return render(request,'app/product_create.html',{})

def product_update(request, id):
    item_product = Product.objects.get(id=id)
    if request.method == "POST":
        item_product.name = request.POST['name']
        item_product.description = request.POST['description']
        item_product.price = request.POST['price']
        item_product.status = request.POST['status']
        
        # Kiểm tra nếu người dùng đã chọn một tệp hình ảnh mới
        if 'image' in request.FILES:
            item_product.image = request.FILES['image']

        item_product.save()

        messages.success(request, 'Sản phẩm đã được cập nhật thành công!')
        return redirect('/list')  # Chuyển hướng tới trang danh sách sản phẩm sau khi cập nhật
    return render(request, 'app/product_update.html', {"item_product": item_product})