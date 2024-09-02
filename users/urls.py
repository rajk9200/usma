
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products),
    path('add_product/', views.add_product),
    path('add_customer/', views.add_customers),
    path('place_order/', views.place_order),
    path('new_order/', views.new_order),
    path('orders/', views.orders),
    path('product_list/', views.product_list),
    path('customers/', views.customers),
    path('register/', views.regsier_view),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view),
    path('', views.dashboard_view,name='dashboard'),
    path('dashboard/', views.admin_dashboard,name='admin_dashboard'),


]
