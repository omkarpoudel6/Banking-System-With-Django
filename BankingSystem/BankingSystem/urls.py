
from django.contrib import admin
from django.urls import path,include
from Users.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login,name="login"),
    path('accounts/',include('CustomerAccounts.urls',namespace='accounts'))
]
