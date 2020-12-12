from django.urls import path
from . import views

app_name='accounts'

urlpatterns=[
    path('',views.createAccount,name='create_new_account'),
    path('viewaccount/',views.viewAccount,name='view_account'),
    path('withdraw/',views.withdraw,name='withdraw_money'),
    path('deposit/',views.deposit,name='deposie_money')
]