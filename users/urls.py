
from django.urls import path
from . import views

from .helper import generate_invoice,download_invoice
urlpatterns = [
    path('order_list/', views.order_list,name='order_list'),
    path('product_list/', views.product_list,name='product_list'),
    path('customer_list/', views.customer_list,name='customer_list'),
    path('profile/', views.profile_view,name='profile'),


    path('invoice/<id>', download_invoice, name='invoice'),
    path('report/', generate_invoice, name='invoice'),
    path('d/', views.generate_pdf, name='d'),
    path('one_product/<id>', views.one_product),
    path('one_order/<id>', views.one_order),
    path('products/', views.products),
    path('add_product/', views.add_product),
    path('add_customer/', views.add_customers),
    path('place_order/', views.place_order),
    path('new_order/', views.new_order),
    path('orders/', views.orders),


    path('customers/', views.customers,name="customers"),
    path('register/', views.regsier_view),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view),

    path('', views.dashboard_view,name='dashboard'),
    path('dashboard/', views.admin_dashboard,name='admin_dashboard'),


]
