from django.db import models

# Create your models here.
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