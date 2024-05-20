from django.contrib import auth
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account,DetailAccount, Product
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
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

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Kiểm tra tài khoản có tồn tại không
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            context = {'error': 'Tên đăng nhập hoặc mật khẩu không hợp lệ'}
            return render(request, 'app/login.html', context)
        
        if account.status == 'locked':
            # Nếu tài khoản bị khóa, trả về thông báo tài khoản bị khóa
            context = {'error': 'Tài khoản của bạn đã bị khóa.'}
            return render(request, 'app/login.html', context)
        
        # Xác thực tài khoản và đăng nhập
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            context = {'error': 'Tên đăng nhập hoặc mật khẩu không hợp lệ'}
            return render(request, 'app/login.html', context)
    else:
        return render(request, 'app/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = request.POST['name']
        sex = request.POST['sex']
        address = request.POST['address']
        phone = request.POST['phone']

        # Kiểm tra mật khẩu và mật khẩu xác nhận
        if password != confirm_password:
            messages.error(request, 'Mật khẩu không khớp.')
            return redirect('register')

        # Tạo tài khoản Django User và đặt mật khẩu
        user = User.objects.create(username=username, email=email)
        user.set_password(password)  # Đặt mật khẩu
        user.save()

        # Tạo tài khoản
        account = Account.objects.create(username=username, email=email, password=password)
        account.save()

        # Tạo thông tin chi tiết tài khoản
        detail_account = DetailAccount.objects.create(name=name, sex=sex, address=address, phone=phone, id_account=account)
        detail_account.save()

        # Chuyển hướng đến trang chủ sau khi đăng ký thành công
        return redirect('home')

    return render(request, 'app/register.html')

def home(request):
    return render(request, 'app/home.html')

def logout(request):
    auth_logout(request)
    return redirect('home')


def account_list(request):
    # Lấy tất cả thông tin tài khoản
    accounts = Account.objects.all()

    # Tạo danh sách chứa thông tin chi tiết tài khoản kèm theo thông tin account
    account_details = []
    for account in accounts:
        try:
            detail = account.detail  # Sử dụng related_name để lấy thông tin chi tiết tài khoản
        except DetailAccount.DoesNotExist:
            detail = None
        account_details.append({
            'account': account,
            'detail': detail
        })

    # Truyền thông tin vào template
    context = {
        'account_details': account_details,
    }
    return render(request, 'app/account_list.html', context)

def account_update(request, id):
    account = get_object_or_404(Account, id=id)
    detail_account = account.detail if hasattr(account, 'detail') else None
    
    if request.method == "POST":
        account.username = request.POST.get('username')
        account.email = request.POST.get('email')
        account.status = request.POST.get('status')
        account.role = request.POST.get('role')

        if detail_account:
            detail_account.name = request.POST.get('name')
            detail_account.sex = request.POST.get('sex')
            detail_account.address = request.POST.get('address')
            detail_account.phone = request.POST.get('phone')
            detail_account.save()
        else:
            detail_account = DetailAccount(
                id_account=account,
                name=request.POST.get('name'),
                sex=request.POST.get('sex'),
                address=request.POST.get('address'),
                phone=request.POST.get('phone')
            )
            detail_account.save()

        account.save()
        messages.success(request, 'Tài khoản đã được cập nhật thành công!')
        return redirect('account_list')
    
    context = {
        'account': account,
        'detail_account': detail_account,
    }
    return render(request, 'app/account_update.html', context)

def account_create(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = request.POST['name']
        sex = request.POST['sex']
        address = request.POST['address']
        phone = request.POST['phone']
        status = request.POST['status']
        role = request.POST['role']

        # Kiểm tra mật khẩu và mật khẩu xác nhận
        if password != confirm_password:
            messages.error(request, 'Mật khẩu không khớp.')
            return redirect('account_create')

        # Tạo tài khoản Django User và đặt mật khẩu
        user = User.objects.create(username=username, email=email)
        user.set_password(password)  # Đặt mật khẩu
        user.save()

        # Tạo tài khoản
        account = Account.objects.create(username=username, email=email, password=password, status=status, role=role)
        account.save()

        # Tạo thông tin chi tiết tài khoản
        detail_account = DetailAccount.objects.create(name=name, sex=sex, address=address, phone=phone, id_account=account)
        detail_account.save()

        # Hiển thị thông báo thành công và chuyển hướng đến trang account_list
        messages.success(request, 'Tài khoản đã được tạo thành công!')
        return redirect('account_list')

    context = {
        'ROLE_CHOICES': Account.ROLE_CHOICES,
        'STATUS_CHOICES': Account.STATUS_CHOICES,
    }
    
    return render(request, 'app/account_create.html', context)

