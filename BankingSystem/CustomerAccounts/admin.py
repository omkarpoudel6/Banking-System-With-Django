from django.contrib import admin
from .models import CustomerProfile,Account,Transaction
#
# # Register your models here.
admin.site.register(CustomerProfile)
# admin.site.register(Account)
# admin.site.register(Transaction)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id','accountNo','customer_id','balance']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id','account','amount','remarks','action']
