from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
# Create your views here.
from django.http import HttpResponse
from django import forms
from models import Customers
from .search import NameForm
from .forms import loginform, advsearchform

def homepage(request):
	return render(request,'index.html')

def login(request):
# if this is a POST request we need to process the form data
    if request.method == 'POST':
		# create a form instance and populate it with data from the request:
        form = loginform(request.POST)
        # check whether it's valid:
        if form.is_valid():
			login = form.cleaned_data['login']
			pw = form.cleaned_data['pw']
			q = Customers.objects.filter(loginid=login)
			if not q:
				print 'Wrong LoginID'
			elif q.values('pw')[0]['pw'] != pw:
				print 'Wrong password'
			else:
				print 'Login Successful!'
				#Session object created here
				request.session["login"]= True
				return HttpResponseRedirect('/homepage/')
    else:
        form = loginform()

    return render(request, 'login.html', {'form': form})

def registration(request):

	req = {'fullName':None,
	'loginID':None,
	'pw':None,
	'cfm_pw':None,
	'majorCCN':None,
	'address':None,
	'phoneNum':None,
	'q':None,
	'error':False}

	if 'fullName' in request.GET:
		req['fullName'] = request.GET['fullName']
	if 'loginID' in request.GET:
		req['loginID'] = request.GET['loginID']
	if 'pw' in request.GET:
		req['pw'] = request.GET['pw']
	if 'cfm_pw' in request.GET:
		req['cfm_pw'] = request.GET['cfm_pw']
	if 'majorCCN' in request.GET:
		req['majorCCN'] = request.GET['majorCCN']
	if 'address' in request.GET:
		req['address'] = request.GET['address']
	if 'phoneNum' in request.GET:
		req['phoneNum'] = request.GET['phoneNum']

	req['q'] = Customers.objects.filter(loginid=req['loginID']);

	if req['fullName'] =="" or req['loginID'] =="" or req['pw'] != req['cfm_pw'] or req['majorCCN']== "" or req['address'] == "" or req['phoneNum'] == "":
		req['error'] = True
	else:
		p = Customers(fullname = req['fullName'], loginid = req['loginID'], pw =req['pw'], majorccn = req['majorCCN'], address = req['address'], phonenum = req['phoneNum'])
		p.save()

	return render_to_response('registration.html',req)

def advsearch(request):
	# if this is a POST request we need to process the form data
    if request.method == 'POST':
		# create a form instance and populate it with data from the request:
        searchform = advsearchform(request.POST)
        # check whether it's valid:
        if searchform.is_valid():
			author = searchform.cleaned_data['author']
			publisher = searchform.cleaned_data['publisher']
			title = searchform.cleaned_data['title']
			subject = searchform.cleaned_data['subject']
			q = Customers.objects.filter(loginid=search)
			if not q:
				print 'Wrong LoginID'
			elif q.values('pw')[0]['pw'] != pw:
				print 'Wrong password'
			else:
				print 'Login Successful!'
				#Session object created here
				request.session["login"]= True
				return HttpResponseRedirect('/homepage/')
    else:
        form = advsearchform()

    return render(request, 'advsearch.html', {'form': form})

def search(request):
	if 'q' in request.GET:
		message = 'You searched for: %r' % request.GET['q']
	else:
		message = 'You submitted an empty form.'
	return HttpResponse(message)