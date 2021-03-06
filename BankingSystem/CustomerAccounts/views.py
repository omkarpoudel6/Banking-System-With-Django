from django.contrib import messages
from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.db import IntegrityError

from .forms import AccountCreationForm,DepositForm,WithdrawForm
from .models import Account,CustomerProfile,Transaction,Cheque
from django.contrib.auth.decorators import login_required

from django.forms import ValidationError

# Create your views here.
@login_required(login_url="/login")
def createAccount(request):
    if request.method=="POST":
        form=AccountCreationForm(request.POST)
        if form.is_valid():
            print("form saved")
            form.save()
            print(request.POST['citizenship_no'])
            customer_id=CustomerProfile.objects.get(citizenship_no=request.POST['citizenship_no'])
            account_no=Account.objects.get(customer_id=customer_id)
            print(account_no)
            context={
                'account_no':account_no
            }
            return render(request,'accountcreation.html',context)
        else:
            return HttpResponse("Form Invalid")
    else:
        form=AccountCreationForm()
        context={
            'form':form
        }
        return render(request,'accountcreation.html',context)

@login_required(login_url="/login")
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

        elif 'customer_id' in request.POST:
            customer_id=request.POST['customer_id']
            customer=CustomerProfile.objects.get(id=customer_id)
            customer.first_name=request.POST['first_name']
            customer.middle_name = request.POST['middle_name']
            customer.last_name = request.POST['last_name']
            customer.address = request.POST['address']
            customer.phone = request.POST['phone']
            customer.email = request.POST['email']
            customer.father_name = request.POST['father_name']
            customer.mother_name = request.POST['mother_name']
            customer.grandfather_name = request.POST['grandfather_name']
            customer.spouse_name = request.POST['spouse_name']
            customer.save()
            return redirect("/accounts/viewaccount/")
    return render(request,'viewaccount.html')

@login_required(login_url="/login")
def deposit(request):
    if request.method=="POST":
        deposit_form=DepositForm(request.POST)
        print(deposit_form)
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

@login_required(login_url="/login")
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
            context={}
            withdrawForm=WithdrawForm(request.POST)
            print(withdrawForm)
            if withdrawForm.is_valid():
                try:
                    withdrawForm.save()
                    messages.success(request, 'Transaction Sucessfull')
                    return HttpResponseRedirect("/accounts/withdraw")
                except ValidationError:
                    context['error']='Cheque Number Error'
            else:
                context['error']='Balance or Cheque Number Error'
            return render(request,'withdraw.html',context)
    context={
        'form':withdraw_form
    }
    return render(request, 'withdraw.html',context)

@login_required(login_url="/login")
def transaction(request,id):
    if request.method=="POST":
        start_date=request.POST['startdate']
        end_date=request.POST['enddate']
        account_no=request.POST['account_no']
        print(start_date)
        print(end_date)
        print(account_no)
        transaction=Transaction.objects.filter(account=account_no, created_at__range=[start_date,end_date])
        context={
            'transaction':transaction,
            'account_no':account_no
        }
        return render(request,'transaction.html',context)
    else:
        transaction=Transaction.objects.filter(account=id).order_by("-created_at")
        print(transaction)
        context={
            'account_no':id,
            'transaction':transaction
        }
        return render(request,'transaction.html',context)

@login_required(login_url='/login')
def printChequest(request):
    context={}
    if request.method == "POST":
        if 'accountNo' in request.POST:
            account_no=request.POST['accountNo']
            if Account.objects.filter(accountNo=account_no):
                totalchequeissued=Cheque.objects.filter(account_No=account_no,spend=False).count()
                lastchequenumber=Cheque.objects.last()
                context['totalunspendcheque']=totalchequeissued
                context['showchequeprintform']=True
                context['lastchequenumber']=lastchequenumber
                context['accountno']=account_no
            else:
                return HttpResponse("Account Don't Exists")
        elif 'chequestartnumber' in request.POST:
            account_no=request.POST['accountno']
            chequestartnumber=request.POST['chequestartnumber']
            noofcheques=request.POST['numberofcheque']
            try:
                for x in range(int(chequestartnumber),int(chequestartnumber)+int(noofcheques)):
                    cheque=Cheque()
                    cheque.account_No=account_no
                    cheque.cheque_No=x
                    cheque.save()
                    context['message']='Cheque Printed!!!'
            except IntegrityError:
                context['errormessage']='Cheque Number already Exists'
    return render(request,'printcheque.html',context)
