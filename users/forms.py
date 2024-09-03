from django import forms

from django.contrib.auth.models import User



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerUser,Product

class RegisterForm(forms.ModelForm):

    re_password = forms.CharField(max_length=200, required=True)
    class Meta:
        model = CustomerUser
        fields = ('mobile', 'first_name', 'last_name','password')


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("re_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )



class LoginForm(forms.Form):
    mobile=forms.CharField(max_length=10)
    password=forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ('mobile', 'first_name', 'last_name','email','address')

    def __init__(self, *args, **kwargs):
        super(AddCustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


