from django.contrib import admin
from .models import CustomerProfile,Account,Transaction,Cheque
#
# # Register your models here.
admin.site.register(CustomerProfile)
# admin.site.register(Account)
# admin.site.register(Transaction)
# admin.site.register(Cheque)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id','accountNo','customer_id','balance']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id','account','amount','remarks','action']

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    readonly_fields = ['account_No','cheque_No','spend']
