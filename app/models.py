from django.db import models
from django.contrib.auth.models import User

class Acount(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    password = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    role = models.BooleanField(default=False, null=True, blank=True)

    
class Detail_Acount(models.Model):
    acount = models.ForeignKey(Acount, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    sex = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self) :
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=200, null=True)
    deciption = models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self) :
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Bill(models.Model):
    acount = models.ForeignKey(Acount, on_delete=models.SET_NULL, null=True, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)

class Bill_Detail(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    total_price = models.CharField(max_length=200, null=True)

    
class Cart(models.Model):
    acount = models.ForeignKey(Acount, on_delete=models.SET_NULL, null=True, blank=False)
    def __str__(self):
        return str(self.id)

class Cart_Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.IntegerField(default=0, null=True, blank=True)

