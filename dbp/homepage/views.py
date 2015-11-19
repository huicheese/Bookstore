from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from models import Customers

def homepage(request):
	return render(request,'index.html')

def login(request):
	req = {'loginID':None,
	'pw':None,
	'error':False}

	if 'loginID' in request.GET:
		req['loginID'] = request.GET['loginID']
	if 'pw' in request.GET:
		req['pw'] = request.GET['pw']

	##omit this line first then submit 1 query then unomit this line
	q = Customers.objects.filter(loginid=req['loginID'])	
	print(q.values('pw'))
	print(req['pw'])

	if q.values('pw')[0]['pw'] != req['pw']:
		print 'Wrong password'
	else:
		print 'Login Successful!'
	###

	return render_to_response('login.html',req)

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