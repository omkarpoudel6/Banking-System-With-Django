from django.shortcuts import render

# Create your views here.
def createAccount(request):
    return render(request,'accountcreation.html')

def viewAccount(reqeust):
    return render(reqeust,'viewaccount.html')

def deposit(request):
    return render(request,'deposit.html')

def withdraw(request):
    return render(request,'withdraw.html')