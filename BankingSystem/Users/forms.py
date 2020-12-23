from django import forms
from .models import UserAccount


class UserCreationForm(forms.ModelForm):
    class Meta:
        model=UserAccount
        fields=['first_name','middle_name','last_name','emp_type','email']
