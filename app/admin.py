from django.contrib import admin
from .models import Account, DetailAccount, Product

# Register your models here.
admin.site.register(Account)
admin.site.register(DetailAccount)
admin.site.register(Product)

