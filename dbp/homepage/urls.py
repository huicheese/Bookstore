from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.homepage,name='homepage'),
	url(r'login',views.login,name='login'),
	url(r'registration',views.registration,name='register'),
	url(r'book',views.book,name='book'),
]