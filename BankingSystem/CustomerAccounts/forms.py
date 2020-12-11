from django import forms
from django.forms import ValidationError
from .models import CustomerProfile,Transaction,Account

class AccountCreationForm(forms.ModelForm):
    class Meta:
        model=CustomerProfile
        fields='__all__'
        # exclude=('created_at','updated_at',)


