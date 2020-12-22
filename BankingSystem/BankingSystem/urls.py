
from django.contrib import admin
from django.urls import path,include
from Users.views import Login,logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',Login,name="login"),
    path('logout/',logout_view,name="logout"),

    path('accounts/',include('CustomerAccounts.urls',namespace='accounts')),
    # path('manager/',include('Admin.urls',namespace='manager'))
]
