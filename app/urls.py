from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('list/', views.product_list,name="product_list"),
    path('create/', views.product_create,name="product_create"),
    path('update/<int:id>/', views.product_update,name="product_update"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account_list/', views.account_list,name="account_list"),
    path('accounts/update/<int:id>/', views.account_update, name='account_update'),
    path('account_create/', views.account_create,name="account_create"),
    
]

urlpatterns += static(settings.MEDIA_URL   , document_root=settings.MEDIA_ROOT)