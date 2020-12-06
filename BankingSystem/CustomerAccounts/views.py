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
            print(request.POST['citizenship_no'])
            customer_id=CustomerProfile.objects.get(citizenship_no=request.POST['citizenship_no'])
            account_no=Account.objects.get(customer_id=customer_id)
            context={
                'account_no':account_no
            }
        return render(request,'accountcreation.html',context)
    else:
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