from django.urls import path
from . import views

app_name='manager'

urlpatterns=[
    path("",views.dashboard,name='dashboard'),
    path('create_user/',views.create_user,name='create_user'),
    path('user_info/',views.user_info,name='user_info'),
    path('user_detail/<int:id>/',views.user_detail,name='user_detail'),
    path('update_user_profile',views.update_user_profile,name='update_user_profile'),
    path('change_user_password',views.change_user_password,name='change_user_password'),

    path('account_opened_by_user/<int:id>/',views.account_opened_by_user,name='account_opened_by_user'),
    path('transaction_by_user/<int:id>/<int:type>/',views.transaction_by_user,name='transaction_by_user')
]