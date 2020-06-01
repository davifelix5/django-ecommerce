from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ListProducts.as_view(), name="list"),
    path('<slug>', views.ProductsDetails.as_view(), name="details"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('addtocart/', views.AddToCart.as_view(), name="cart_add"),
    path('removefromcart/', views.RemoveFromCart.as_view(), name="cart_remove"),
    path('order_info/', views.OrderInfo.as_view(), name="info"),
]
