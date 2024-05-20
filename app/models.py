from django.db import models

# Create your models here.
# Định nghĩa class Account
from django.db import models
from django.contrib.auth.hashers import make_password

from django.db import models
from django.contrib.auth.hashers import make_password

class Account(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('locked', 'Locked'),
    )
    id = models.AutoField(primary_key=True)  
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # Sử dụng default để gán giá trị mặc định

    def save(self, *args, **kwargs):
        # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class DetailAccount(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    id_account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='detail')


# Định nghĩa class Product
class Product(models.Model):
    STATUS_CHOICES = [
        ('in_stock', 'Còn hàng'),
        ('out_of_stock', 'Hết hàng'),
        ('discontinued', 'Ngừng kinh doanh'),
    ]
    
    id = models.AutoField(primary_key=True)  # ID của product là khoá chính
    name = models.CharField(max_length=200)  # Tên product
    description = models.TextField(blank=True, null=True)  # Mô tả product
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Giá của product không có phần thập phân
    image = models.ImageField(null=False, upload_to='images',default=None)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')  # Trạng thái của product