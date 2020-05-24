from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm



class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True)
    address = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(min_length=10, max_length=11, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'address', 'phone_number')

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email Exists")
        return self.cleaned_data


class MenuForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=150)
    price = forms.CharField(max_length=10)
    type = forms.CharField(max_length=10)
    item_id = forms.CharField(max_length=50)

    class Meta:
        model = ModelForm
        fields = ('name', 'description', 'price', 'type', 'item_id')

    def clean(self, value):
        try:
            return MenuForm.objects.get(pk=value)
        except:
            raise ValidationError

    def getName(self):
        return self.name

    def is_valid(self):
        return True

DELIVERY_OPTIONS = (
    ("1", "Pickup - No Delivery"),
    ("2", "Delivery - In House"),
    ("3", "Delivery - 3rd Party"),
)

TIP_OPTIONS = (
    ("1", "None"),
    ("2", "15%"),
    ("3", "18%"),
    ("4", "20%"),
    ("5", "Custom Amount"),
)
class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    address = forms.CharField(max_length=50, required=True)
    comments = forms.CharField(max_length=150, required=False)
    delivery_method = forms.ChoiceField(choices=DELIVERY_OPTIONS, required=True)
    phone_number = forms.CharField(max_length=11, min_length=10, required=True)
    tip = forms.ChoiceField(choices=TIP_OPTIONS, required=True)
    tipAmount = forms.DecimalField(max_digits=5)
    price = forms.DecimalField(max_digits=5)

    class Meta:
        model = ModelForm
        fields = ('name', 'address', 'comments', 'delivery_method', 'phone_number', 'price', 'tip', 'tipAmount')

    def clean(self, value):
        try:
            return CheckoutForm.objects.get(pk=value)
        except:
            raise ValidationError

    def getName(self):
        return self.name

    def is_valid(self):
        return True



