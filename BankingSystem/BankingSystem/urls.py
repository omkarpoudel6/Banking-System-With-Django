
from django.contrib import admin
from django.urls import path,include
from Users.views import Login,logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Login,name="login"),
    path('logout/',logout_view,name="logout"),
    path('accounts/',include('CustomerAccounts.urls',namespace='accounts'))
]
