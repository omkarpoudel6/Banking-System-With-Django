from django import forms
from .models import CustomerProfile

class AccountCreationForm(forms.ModelForm):
    class Meta:
        model=CustomerProfile
        fields='__all__'
        # exclude=('created_at','updated_at',)