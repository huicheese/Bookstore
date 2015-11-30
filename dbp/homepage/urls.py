from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.homepage,name='homepage'),
	url(r'login',views.login,name='login'),
	url(r'registration',views.registration,name='register'),
	url(r'advsearch',views.advsearch,name='advsearch'),
	url(r'book',views.book,name='book'),
	url(r'checkout',views.checkout,name='checkout'),
	url(r'signout',views.signout,name='signout'),
	url(r'user',views.user,name='user')
]