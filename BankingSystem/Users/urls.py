from django.urls import path
from . import views

app_name='manager'

urlpatterns=[
    path("dashboard/",views.dashboard,name='dashboard'),
    path('create_user/',views.create_user,name='create_user'),
    path('user_info/',views.user_info,name='user_info'),
    path('change_user_password',views.change_user_password,name='change_user_password')
]