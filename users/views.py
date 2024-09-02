from django.shortcuts import render
# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm,LoginForm,AddCustomerForm,ProductForm
from django.contrib.auth import authenticate,login,logout
from .models import CustomerUser,Product,Order,OrderItem
import json

def dashboard_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    return render(request,'index.html')

def admin_dashboard(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    return render(request,'admin_dashboard.html')


def customers(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    customer_list =CustomerUser.objects.filter().exclude(is_staff=True).order_by('-id')
    context['customer_list']=customer_list
    return render(request,'customers.html',context)


def orders(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    orders_list =Order.objects.filter().order_by('-id')
    print(orders_list)
    context['orders_list']=orders_list
    return render(request,'orders.html',context)


def products(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    product_list =Product.objects.filter().order_by('-id')
    context['product_list']=product_list
    return render(request,'products.html',context)


def new_order(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    product_list =Product.objects.filter().order_by('-id')
    context['product_list']=product_list
    return render(request,'new_order.html',context)

def product_list(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    product_list = Product.objects.filter().order_by('-id')
    v_key =request.GET.get('v_key')
    print(v_key)
    if v_key:
        product_list = product_list.filter(product_name__istartswith=v_key)
    print(product_list)

    context['product_list']=product_list
    return render(request,'product_list.html',context)






def add_customers(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    form = AddCustomerForm(request.POST or None)
    if form.is_valid():

        cus =CustomerUser()
        cus.password=cus.set_password(form.cleaned_data['mobile'])
        cus.backup_password=cus.set_password(form.cleaned_data['mobile'])
        cus.mobile=form.cleaned_data['mobile']
        cus.first_name=form.cleaned_data['first_name']
        cus.last_name=form.cleaned_data['last_name']
        cus.address=form.cleaned_data['address']
        cus.backup_password = "usma"+str(form.cleaned_data['mobile'])
        cus.save()
        return redirect('/customers/')
    context['form']=form

    return render(request,'add_customer.html',context)



def add_product(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('/products/')
    context['form']=form

    return render(request,'add_product.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {}
    form = LoginForm(request.POST or None)

    if form.is_valid():
        user = authenticate(username=request.POST.get('mobile'), password=request.POST.get('password'))
        print(user)
        if user:
            login(request,user)
            print(user)
            if user.is_staff:
                return redirect('/dashboard/')

            return redirect('/')
        else:
            print("Failed")
            # messages.add_message(request, messages.INFO,"login failed." )
    context['form'] = form
    return render(request,"login.html",context)

def regsier_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {}
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)  # Don't save the user to the database just yet
        user.set_password(form.cleaned_data['password'])  # Hash and set the password
        user.save()
        return redirect('login')
        print("done>>>>>>>>>>>>>>>>>>>>>")
    context['form'] = form
    return render(request,"signup.html",context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/login")


def create_order(user, cart_items,status="",amount=0,advance=0):
    # Create a new order
    order = Order.objects.create(user=user,status=status,amount=amount,advance=advance)

    # Add each product in the cart to the order with quantity
    for item in cart_items:
        product = Product.objects.get(id=item['id'])
        quantity = item['qty']
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    return order


def place_order(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("/login")
    if not request.user.is_staff:
        return redirect('/')
    customer_list =CustomerUser.objects.filter().exclude(is_staff=True).order_by('-id')
    context['customer_list']=customer_list

    if request.method=="POST":
        cart_items =request.POST.get("cart_list",{})
        id_customer=request.POST.get('id_customer')
        cart_items=json.loads(cart_items)
        user =CustomerUser.objects.get(id=id_customer)

        print(user,cart_items)
        print(cart_items)
        total_amount =float(request.POST.get('total_amount'))
        p_status =request.POST.get('p_status')
        advance =float(request.POST.get('advance'))
        print(total_amount,p_status,advance)
        create_order(user,cart_items,p_status,total_amount,advance)

        return redirect('/orders/')


    return render(request,'place_order.html',context)