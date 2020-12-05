from django.shortcuts import render
from .forms import AccountCreationForm

# Create your views here.
def createAccount(request):
    form=AccountCreationForm()
    context={
        'form':form
    }
    return render(request,'accountcreation.html',context)

def viewAccount(reqeust):
    return render(reqeust,'viewaccount.html')

def deposit(request):
    return render(request,'deposit.html')

def withdraw(request):
    return render(request,'withdraw.html')