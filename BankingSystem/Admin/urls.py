from django.urls import path
from . import views

app_name='manager'

urlpatterns=[
    path('',views.Manager_home,name="manager_home"),
    path('user_creation',views.user_creation,name="user_creation")
]