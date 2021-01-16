from django.db import models
from django import forms
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from django.forms import ValidationError
import random
# Create your models here.

class CustomerProfile(models.Model):

    CHOICES=(
        ('101','Saving'),
        ('102','Current'),
        ('103','DEMAT'),
        ('104','Fixed Deposit')
    )

    GENDER_CHOICES=(
        ('M','MALE'),
        ('F','FEMALE'),
        ('O','OTHERS')
    )

    user_id = models.CharField(max_length=10,blank=False,default="Null")
    first_name=models.CharField(max_length=30,blank=False)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=False)
    account_type=models.CharField(max_length=13,choices=CHOICES)
    address=models.CharField(max_length=100,blank=False)
    gender=models.CharField(max_length=6,choices=GENDER_CHOICES)
    phone=models.CharField(max_length=10, blank=False)
    email=models.CharField(max_length=100, blank=False)
    citizenship_no=models.CharField(max_length=60, blank=False, unique=True)
    father_name=models.CharField(max_length=60, blank=False)
    mother_name=models.CharField(max_length=60, blank=False)
    grandfather_name=models.CharField(max_length=60, blank=False)
    spouse_name=models.CharField(max_length=60,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.first_name+" "+self.middle_name+" "+self.last_name)

class Account(models.Model):
    user_id=models.CharField(max_length=10,blank=False,default="Null")
    accountNo=models.CharField(max_length=12,blank=False,unique=True)
    customer_id=models.OneToOneField(CustomerProfile,on_delete=models.DO_NOTHING)
    balance=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def generate_accountNo(self,account_type):
        randomNo=random.randint(10000,99999)
        account_no="2072"+str(randomNo)+account_type
        print(account_type)
        while (Account.objects.filter(accountNo=account_no)):
            randomNo = random.randint(10000,99999)
            account_no = "2072" + str(randomNo) + account_type
        self.accountNo = account_no
        return str(self.accountNo)



    def get_availableBalance(self,balance):
        if balance==0:
            return str(0)
        else:
            return str(balance-1000)

    def __str__(self):
        return str(self.accountNo)


class Transaction(models.Model):
    user_id=models.CharField(max_length=10,blank=False,default="Null")
    account=models.CharField(max_length=12,blank=False)
    amount=models.PositiveIntegerField(blank=False)
    remarks=models.CharField(max_length=250,blank=False)
    action=models.CharField(max_length=6,blank=False)
    cheque_No=models.CharField(max_length=8,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.action=="Credit":
            return str(str(self.account)+"+"+str(self.amount)+"<"+str(self.remarks))
        if self.action=="Debit":
            return str(str(self.account) + "-" + str(self.amount) + "<" + str(self.remarks))

class Cheque(models.Model):
    account_No=models.CharField(max_length=12,blank=False)
    cheque_No=models.CharField(max_length=8,blank=False,unique=True)
    spend=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cheque_No}"

@receiver(post_save,sender=CustomerProfile)
def post_save_generate_account_no(sender,instance,created,**kwargs):
    if created:
        # Account.objects.create(customer_id=instance)
        account = Account()
        account.customer_id = instance
        account.user_id=instance.user_id
        account.accountNo = account.generate_accountNo(instance.account_type)
        account.save()

@receiver(post_save,sender=Transaction)
def post_save_add_balance_in_account(sender,instance,created,**kwargs):
    if created and instance.action=="Credit":
        account=Account.objects.get(accountNo=instance.account)
        account.balance=int(account.balance)+int(instance.amount)
        account.save()
    elif created and instance.action=="Debit":
        account = Account.objects.get(accountNo=instance.account)
        account.balance = int(account.balance) - int(instance.amount)
        account.save()

@receiver(pre_save,sender=Transaction)
def pre_save_check_chequeNo_is_already_used_or_not(sender,instance,**kwargs):
    cheque_no=instance.cheque_No
    print(cheque_no)
    cheque=Cheque.objects.filter(cheque_No=cheque_no,spend=False)
    print(cheque)
    if cheque:
        cheque2=Cheque.objects.get(cheque_No=cheque_no,spend=False)
        print(cheque2.spend)
        cheque2.spend=True
        cheque2.save()
        print(cheque2.spend)
    else:
        print("Cheque Already in use")
        raise forms.ValidationError("Cheque Number Error")


