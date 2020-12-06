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
    if reqeust.method=="POST":
        account_no=reqeust.POST['account_no']
        account=Account.objects.get(accountNo=account_no)
        print(account)
        if account:
            customer_id=account.customer_id.id
            print(customer_id)
            accountholder=CustomerProfile.objects.get(id=customer_id)
            print(accountholder.first_name)
            context={
                'account':account
            }
            return render(reqeust,'viewaccount.html',context)
        else:
            context={
                'error':'Account No Do not match'
            }
            return render(reqeust,'viewaccount.html',context)
        print(account)
        print(account_no)
    return render(reqeust,'viewaccount.html')

def deposit(request):
    return render(request,'deposit.html')

def withdraw(request):
    return render(request,'withdraw.html')