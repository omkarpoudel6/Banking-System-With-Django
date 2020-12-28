from django import forms
from django.forms import ValidationError
from .models import CustomerProfile,Transaction,Account

class AccountCreationForm(forms.ModelForm):
    class Meta:
        model=CustomerProfile
        fields='__all__'
        # exclude=('created_at','updated_at',)


class DepositForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['user_id','account','amount','remarks','action']

    def clean_account(self,*args,**kwargs):
        account_no=self.cleaned_data.get('account')
        print(account_no)
        account=Account.objects.filter(accountNo=account_no)
        if account==None:
            raise forms.ValidationError('Invalid Account Number')
        else:
            return account_no

class WithdrawForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['user_id','account','amount','remarks','action']

# class CustomerProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model=CustomerProfile
#         fields=['first_name','middle_name','last_name','address','phone','email','father_name','mother_name','grandfather_name','spouse_name']

