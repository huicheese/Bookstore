from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import Customers, Orders, Books, Feedbacks

from .forms import loginform, RegForm, BookForm, advsearchform, FeedbackForm

#for regrex
import re

def homepage(request):

    q = Books.objects.all()[:9]

    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        return render(request,'index.html',{'login':login,'loginid':loginid,'booklist':q})
    else:
        return render(request,'index.html',{'booklist':q})

def signout(request):
    request.session.flush()
    return HttpResponseRedirect('/homepage/')

def book(request,isbn):
    print isbn
    q = Books.objects.filter(isbn=isbn)

    p = Feedbacks.objects.filter(isbn=isbn)[:5]
    print p

    bookdefault = {'qty':1}
    feedbackdefault = {'feedback':1,'comment':''}
    print (request)

    if request.method == 'POST':

        if 'feedback' in  request.POST:
            print (request.POST['feedback'])
            feedbackform = FeedbackForm(request.POST)
            bookform = BookForm(bookdefault)

            if feedbackform.is_valid():
                print ('Feedback posted!')
        
        elif 'qty' in request.POST:
            bookform = BookForm(request.POST)
            feedbackform = FeedbackForm(feedbackdefault)

            if bookform.is_valid():

                if q[0].stock<= 0:
                    print ("Insufficient Stock!")

                else:
                    qty = bookform.cleaned_data['qty']
                    print ('Order sent!')
                    print (qty)
                    return HttpResponseRedirect('/homepage/checkout') 

        else:
            print ('Rating posted!')
            bookform = BookForm(bookdefault)
            feedbackform = FeedbackForm(feedbackdefault)
            print (request.POST['rating'])
            return render(request,'book.html',{'bookform':bookform, 'feedbackform':feedbackform, 'book':q[0], 'feedbacks':p})

    else:
        bookform = BookForm(bookdefault)
        feedbackform = FeedbackForm(feedbackdefault)

    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        return render(request,'book.html',{'bookform':bookform, 'feedbackform':feedbackform,'login':login,'loginid':loginid, 'book':q[0], 'feedbacks':p})

    return render(request,'book.html',{'bookform':bookform, 'feedbackform':feedbackform, 'book':q[0], 'feedbacks':p})

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
                request.session["loginid"] = login
                request.session["login"]= True
                request.session.set_expiry(300) 
                return HttpResponseRedirect('/homepage/')
    else:
        form = loginform()

    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        return render(request, 'login.html', {'form': form, 'login':login,'loginid':loginid})

    return render(request, 'login.html', {'form': form})

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

                elif re.match("^[0-9]{16}|[0-9]{13}$",majorccn) == None:
                    print('Invalid Credit Card No.!')

                elif re.match("[0-9]+",phonenum) == None:
                    print('Invalid Phone No.!')

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

    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        return render(request,'registration.html', {'regform':regform, 'success':success,'login':login,'loginid':loginid})

    return render(request,'registration.html', {'regform':regform, 'success':success})

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

    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        return render(request, 'advsearch.html', {'form': form,'login':login,'loginid':loginid})

    return render(request, 'advsearch.html', {'form': form})

def checkout(request):
    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        return render (request,'checkout.html',{'login':login,'loginid':loginid})

    return render (request,'checkout.html')

def user(request):
    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        q = Customers.objects.filter(loginid=loginid)
        data = q.values()[0]
        data['login']=login
        data['loginid']=loginid

    return render (request,'user.html',data)

