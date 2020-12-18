from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from .forms import AccountCreationForm,DepositForm,WithdrawForm
from .models import Account,CustomerProfile,Transaction

# Create your views here.
def createAccount(request):
    if request.method=="POST":
        form=AccountCreationForm(request.POST)
        print(form)
        if form.is_valid():
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

def viewAccount(request):
    if request.method=="POST":
        if 'account_no' in request.POST:
            account_no=request.POST['account_no']
            account=Account.objects.filter(accountNo=account_no)
            if account:
                account2=Account.objects.get(accountNo=account_no)
                available_balance = account2.get_availableBalance(account2.balance)
                customer_id=account2.customer_id.id
                accountholder=CustomerProfile.objects.get(id=customer_id)
                context={
                    'accountholder':accountholder,
                    'available_balance':available_balance,
                    'show_buttons':True
                }
                return render(request,'viewaccount.html',context)
            else:
                context={
                    'error':'Account No Do not match'
                }
                return render(request,'viewaccount.html',context)

        elif 'account_number' in request.POST:
            account_no=request.POST['account_number']
            print(account_no)
            account=Account.objects.get(accountNo=account_no)
            account.first_name=request.POST['first_name']
            account.middle_name = request.POST['middle_name']
            account.last_name = request.POST['last_name']
            account.address = request.POST['address']
            account.phone = request.POST['phone']
            account.email = request.POST['email']
            account.father_name = request.POST['father_name']
            account.mother_name = request.POST['mother_name']
            account.grandfather_name = request.POST['grandfather_name']
            account.spouse_name = request.POST['spouse_name']
            account.save()
            print(account.middle_name)
            return redirect("/accounts/viewaccount/")
    return render(request,'viewaccount.html')

def deposit(request):
    if request.method=="POST":
        deposit_form=DepositForm(request.POST)
        if deposit_form.is_valid():
            print(deposit_form)
            deposit_form.save()
            return redirect('/accounts/deposit/')
        else:
            context={
                'error':'Account No Error'
            }
            return render(request,'deposit.html',context)
    else:
        return render(request,'deposit.html')


def withdraw(request):
    withdraw_form=WithdrawForm()
    if request.method == "POST":
        if 'account_no' in request.POST:
            account_no = request.POST['account_no']
            account = Account.objects.filter(accountNo=account_no)
            if account:
                account2 = Account.objects.get(accountNo=account_no)
                available_balance = account2.get_availableBalance(account2.balance)
                customer_id = account2.customer_id.id
                accountholder = CustomerProfile.objects.get(id=customer_id)
                context = {
                    'accountholder': accountholder,
                    'available_balance': available_balance,
                    'show_amount_form':True
                }
                return render(request, 'withdraw.html', context)
            else:
                context = {
                    'error': 'Account No Do not match'
                }
                return render(request, 'withdraw.html', context)
        if 'amount' in request.POST:
            withdrawForm=WithdrawForm(request.POST)
            print(withdrawForm)
            if withdrawForm.is_valid():
                withdrawForm.save()
                return redirect("/accounts/withdraw/")
            else:
                context={
                    'error':'Invalid Balance'
                }
                return render(request,'withdraw.html',context)

    context={
        'form':withdraw_form
    }

    return render(request, 'withdraw.html',context)

def transaction(request,id):
    transaction=Transaction.objects.filter(account=id).order_by("-created_at")
    print(transaction)
    context={
        'account_no':id,
        'transaction':transaction
    }
    return render(request,'transaction.html',context)