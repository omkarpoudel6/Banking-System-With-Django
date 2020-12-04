from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
# Create your models here.

class CustomerProfile(models.Model):

    CHOICES=(
        ('101','Saving'),
        ('102','Current'),
        ('103','DEMAT'),
        ('104','Fixed Deposit')
    )

    first_name=models.CharField(max_length=30,blank=False)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=False)
    account_type=models.CharField(max_length=3,choices=CHOICES,default=None)
    address=models.CharField(max_length=100,blank=False)
    phone=models.CharField(max_length=10)
    email=models.CharField(max_length=100)
    father_name=models.CharField(max_length=60)
    mother_name=models.CharField(max_length=60)
    grandfather_name=models.CharField(max_length=60)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.first_name+" "+self.middle_name+" "+self.last_name)

class Account(models.Model):
    accountNo=models.CharField(max_length=12,blank=False)
    customer_id=models.OneToOneField(CustomerProfile,on_delete=models.CASCADE)
    balance=models.PositiveIntegerField(default=1000)
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
        return self.accountNo

    def __str__(self):
        return str(self.accountNo)


class Transaction(models.Model):
    sender=models.ForeignKey(Account,related_name='sender',on_delete=models.DO_NOTHING)
    receiver=models.ForeignKey(Account,related_name='receiver',on_delete=models.DO_NOTHING)
    amount=models.PositiveIntegerField(blank=False)
    remarks=models.CharField(max_length=250,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(str(self.sender)+">"+str(self.receiver))



@receiver(post_save,sender=CustomerProfile)
def post_save_generate_account_no(sender,instance,created,**kwargs):
    if created:
        # Account.objects.create(customer_id=instance)
        account = Account()
        account.customer_id = instance
        account.accountNo = account.generate_accountNo(instance.account_type)
        account.save()
