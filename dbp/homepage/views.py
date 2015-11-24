from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import Customers

from .forms import NameForm , RegForm


def homepage(request):
	return render(request,'index.html')

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
		# create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
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
        form = NameForm()

    return render(request, 'login.html', {'form': form})

# def login(request):
# 	req = {'loginID':None,
# 	'pw':None,
# 	'error':False}
#
# 	if 'loginID' in request.GET:
# 		req['loginID'] = request.GET['loginID']
# 	if 'pw' in request.GET:
# 		req['pw'] = request.GET['pw']
#
# 	##omit this line first then submit 1 query then unomit this line
# 	# q = Customers.objects.filter(loginid=req['loginID'])
# 	# print(q.values('pw'))
# 	# print(req['pw'])
# 	#
# 	# if q.values('pw')[0]['pw'] != req['pw']:
# 	# 	print 'Wrong password'
# 	# else:
# 	# 	print 'Login Successful!'
# 	# 	#Session object created here
# 	# 	request.session["login"]= True
# 	###
#
# 	return render_to_response('login.html',req)

def registration(request):

	success = False

	if request.method == 'POST':
		print(request.POST['fullname'])		
		regform = RegForm(request.POST)

		if regform.is_valid():
			fullname = regform.cleaned_data['fullname']
        	login = regform.cleaned_data['loginid']
        	pw = regform.cleaned_data['pw']
        	cfmpw = regform.cleaned_data['cfmpw']
        	majorccn = regform.cleaned_data['majorccn']
        	address = regform.cleaned_data['address']
        	phonenum = regform.cleaned_data['phonenum']

        	q = Customers.objects.filter(loginid=login);
        	if not q:
        		print('usename avaiable!')
        		
        		if pw!=cfmpw:
        			print('Password mismatch!')
        		else:
        			p = Customers(fullname = fullname, loginid = login, pw =pw, majorccn = majorccn, address = address, phonenum = phonenum)
        			p.save()
        			print('account created!')
        			request.session["login"]= True	
        			success = True			
        	else:
        		print('username taken!')
	else:
		regform = RegForm()

	return render(request,'registration.html', {'regform':regform, 'success':success})
