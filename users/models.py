from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(mobile)
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)  # If you don't want to use passwords
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(mobile, password, **extra_fields)


class CustomerUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True,blank=True,null=True)
    mobile = models.CharField(unique=True,max_length=10)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    address=models.TextField(null=True,blank=True)
    backup_password=models.CharField(max_length=200,null=True,blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.mobile




class Product(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    product_name=models.CharField(max_length=100)
    p_desc=models.TextField(max_length=100)
    product_image=models.ImageField(upload_to="products",default="product.png")
    weight=models.IntegerField(default=0)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    customer_price=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    retailer_price=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    datetime =models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_id()
        super(Product, self).save(*args, **kwargs)

    def generate_id(self):
        last_product = Product.objects.order_by('-id').first()
        if last_product:
            last_id = last_product.id
            last_number = int(last_id[4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f"PRO{new_number:08d}"





    # def __str__(self):
    #     return str(self.product.product_name)+" order by Order Rs.-"+str(self.amount)


class Order(models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,null=True, blank=True)
    amount=models.DecimalField(max_digits=8,decimal_places=2,null=True, blank=True)
    advance=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_id()
        super(Order, self).save(*args, **kwargs)

    def generate_id(self):
        last_order = Order.objects.order_by('-id').first()
        if last_order:
            last_id = last_order.id
            last_number = int(last_id[4:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f"UORD{new_number:08d}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



    def __str__(self):
        return f"{self.quantity} x {self.product}"