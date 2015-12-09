from django.conf.urls import include,url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^$', views.homepage,name='homepage'),
	url(r'login',views.login,name='login'),
	url(r'registration',views.registration,name='register'),
	url(r'advsearch',views.advsearch,name='advsearch'),
	url(r'^book/([0-9]{3}-[0-9]{10})/$',views.book,name='book'),
	url(r'checkout',views.checkout,name='checkout'),
	url(r'signout',views.signout,name='signout'),
	url(r'user',views.user,name='user'),
	url(r'admin',views.admin,name='admin'),
	url(r'results',views.search,name='results')
]
