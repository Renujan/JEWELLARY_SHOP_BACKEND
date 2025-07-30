from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
    path('enquiry/', views.send_enquiry, name='send-enquiry'),
    path('submit_order/', views.submit_order, name='submit-billing'),
]
