"""cis498Final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from cis498 import views as cisviews


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', cisviews.home, name='home'),
    url(r'^home/$', cisviews.home, name='homepage'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^stafflogin/$', cisviews.stafflogin, name='stafflogin'),
    url(r'^stafflogout/$', cisviews.staff_logout, name='stafflogout'),
    url(r'^signup/$', cisviews.signup, name='signup'),
    url(r'^staffhome/$', cisviews.staffhome, name='staffhome'),
    url(r'^updateOrders/(?P<item_id>[-\w]+)/$', cisviews.updateOrders, name='updateOrders'),
    url(r'^updateDriverOrders/(?P<item_id>[-\w]+)/$', cisviews.updateDriverOrders, name='updateDriverOrders'),
    url(r'^checkout/$', cisviews.checkout, name='checkout'),
    url(r'^ordertracker/$', cisviews.ordertracker, name='ordertracker'),
    url(r'^driverhome/$', cisviews.driverhome, name='driverhome'),
    url(r'^add_to_cart/(?P<item_id>[-\w]+)$', cisviews.add_to_cart, name='add_to_cart'),
    url(r'^delete_from_cart/(?P<item_id>[-\w]+)$', cisviews.delete_from_cart, name='delete_from_cart'),
    url(r'^editMenuItem/$', cisviews.editMenuItem, name='editMenuItem'),
    url(r'^customerreport/$', cisviews.customer_report, name='customerreport'),
    url(r'^driverreport/$', cisviews.driver_report, name='driverreport'),
]
