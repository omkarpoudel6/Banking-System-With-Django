from django.shortcuts import render
from .forms import AccountCreationForm
from .models import Account,CustomerProfile

# Create your views here.
def createAccount(request):
    if request.method=="POST":
        form=AccountCreationForm(request.POST)
        print(form)
        if form.is_valid():
            print(form)
            form.save()
            customer_id=CustomerProfile.objects.filter(first_name=request.POST['first_name'])
            account_no=Account.objects.filter(customer_id=customer_id)
            print(account_no)

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