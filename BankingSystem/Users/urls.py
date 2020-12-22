from django.urls import path
from . import views

app_name='manager'

urlpatterns=[
    path("dashboard/",views.dashboard,name='dashboard'),
    path('create_user/',views.create_user,name='create_user'),
    path('user_info/',views.user_info,name='user_info')
]