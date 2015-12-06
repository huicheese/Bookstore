from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Max, Q
from models import Customers, Orders, Books, Feedbacks,Orders,OrderItems, Ratings
from django.template import RequestContext

from .forms import loginform, RegForm, BookForm, advsearchform, FeedbackForm, ViewForm

from datetime import datetime
#for regrex
import re
from django.db import connection

def homepage(request):

    q = Books.objects.all().order_by('?')[:9]

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
    q = Books.objects.filter(isbn=isbn)
    p = Feedbacks.objects.filter(isbn=isbn)

    #default values for the bookform and the feedbackform
    bookdefault = {'qty':1}
    feedbackdefault = {'feedback':1,'comment':''}
    viewdefault = {'num':1}
    num = 0

    #if it's a post request
    if request.method == 'POST':

        #If it's a feedbackform request
        if 'feedback' in  request.POST:
            feedbackform = FeedbackForm(request.POST)
            bookform = BookForm(bookdefault)
            viewform = ViewForm(bookdefault)


            if feedbackform.is_valid():
                if "loginid" in request.session:
                    review = feedbackform.cleaned_data['feedback']
                    comment = feedbackform.cleaned_data['comment']
                    customer = Customers.objects.get(loginid=request.session["loginid"])
                    book = Books.objects.get(isbn=isbn)
                    f = Feedbacks(loginid=customer,isbn=book,review=review,optionalcomment=comment,feedback_date=str(datetime.now()))
                    f.save()
                    print ('Feedback posted!')
                else:
                    print ('Login to give feedback')

        elif 'num' in request.POST:
            feedbackform = FeedbackForm(feedbackdefault)
            bookform = BookForm(bookdefault)
            viewform = ViewForm(request.POST)

            if viewform.is_valid():
                num = viewform.cleaned_data['num']

        #If it's a bookform request
        elif 'qty' in request.POST:
            bookform = BookForm(request.POST)
            feedbackform = FeedbackForm(feedbackdefault)
            feedbackform = FeedbackForm(feedbackdefault)


            if bookform.is_valid():
                if "loginid" in request.session:
                    qty = bookform.cleaned_data['qty']
                    book = Books.objects.get(isbn=isbn)

                    print ('Processing order')

                    temp = request.session["orders"]
                    if isbn in temp:
                        temp[isbn] = temp[isbn]+qty
                    else:
                        temp[isbn]= qty


                    if temp[isbn] > book.stock:
                        print 'Insufficient Stock!'

                    else:
                        print temp
                        request.session["orders"] = temp
                        return HttpResponseRedirect('/homepage/checkout')

                else:
                    print ('Login to order')

        #Else if it's a rating request
        else:
            bookform = BookForm(bookdefault)
            feedbackform = FeedbackForm(feedbackdefault)


            if "loginid" in request.session and request.session['loginid'] != request.POST['loginid']:

                rating = request.POST['rating']
                ratingid = Customers.objects.get(loginid=request.session['loginid'])
                feedbackid = Customers.objects.get(loginid=request.POST['loginid'])
                book = Books.objects.get(isbn=isbn)
                p = Ratings(isbn=book,feedbackid=feedbackid,ratingid=ratingid,rating=rating)
                p.save()
                print 'Ratings posted!'
                return HttpResponseRedirect('/homepage/')

            elif request.session['loginid'] == request.POST['loginid']:
                print 'You cannot review yourself!'
            else:
                print 'Please login first'


    #If it's not a post request
    else:
        #create the default forms
        bookform = BookForm(bookdefault)
        feedbackform = FeedbackForm(feedbackdefault)
        viewform = ViewForm(viewdefault)

    #If user is logged in render the page with the Welcome ___! and signout options
    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        user = Customers.objects.filter(loginid=loginid).values()[0]
        cursor = connection.cursor()
        print isbn
        cursor.execute("SELECT feedbacks.loginID, feedbacks.review, feedbacks.optionalComment from feedbacks where (feedbacks.ISBN = %s) AND feedbacks.loginID IN (select feedbackID from (select * from ratings where ratings.ISBN=%s) group by feedbackID ORDER BY avg(rating) DESC LIMIT %s)",[isbn,isbn,num])
        views = cursor.fetchall()
        cursor.close()

        return render(request,'book.html',{'bookform':bookform, 'feedbackform':feedbackform, 'viewform': viewform,'login':login,'loginid':loginid, 'book':q[0], 'feedbacks':p, 'views':views})

    #Else rendeer the page with the register and login options
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
                request.session["orders"] = dict()
                request.session.set_expiry(3000)
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

    if request.method == 'POST':
        if 'sorting' in request.POST:
            authors = request.session['authors']
            publisher = request.session['publisher']
            title = request.session['title']
            subject = request.session['subject']
            sorter = request.POST['sorting']
            if sorter == 'asc_year':
                q = Books.objects.filter(title__contains=title,authors__contains=authors,publisher__contains=publisher,subject__contains=subject).order_by('yearpublished')
            elif sorter == 'desc_year':
                q = Books.objects.filter(title__contains=title,authors__contains=authors,publisher__contains=publisher,subject__contains=subject).order_by('-yearpublished')
            elif sorter == 'asc_score':
                q = Books.objects.raw("SELECT * FROM Books INNER JOIN (SELECT avg(review) A, ISBN FROM feedbacks GROUP BY ISBN) T ON Books.ISBN=T.ISBN WHERE Books.subject LIKE %s OR Books.title LIKE %s OR Books.authors LIKE %s OR Books.publisher LIKE %s ORDER BY T.A ASC", [subject, title, authors, publisher])
            elif sorter == 'desc_score':
                q = Books.objects.raw("SELECT * FROM Books INNER JOIN (SELECT avg(review) A, ISBN FROM feedbacks GROUP BY ISBN) T ON Books.ISBN=T.ISBN WHERE Books.subject LIKE %s OR Books.title LIKE %s OR Books.authors LIKE %s OR Books.publisher LIKE %s ORDER BY T.A DESC", [subject, title, authors, publisher])
            else:
                q = Books.objects.filter(title__contains=title,authors__contains=authors,publisher__contains=publisher,subject__contains=subject)
            if "login" in request.session and "loginid" in request.session:
                login = request.session["login"]
                loginid = request.session["loginid"]
                return render(request, 'results.html', {'login':login,'loginid':loginid, 'booklist':q})

            return render(request, 'results.html', {'booklist':q})
        # create a form instance and populate it with data from the request:
        form = advsearchform(request.POST)
        # check whether it's valid:
        if form.is_valid():
            authors = form.cleaned_data['authors'].lstrip()
            publisher = form.cleaned_data['publisher'].lstrip()
            title = form.cleaned_data['title'].lstrip()
            subject = form.cleaned_data['subject'].lstrip()
            request.session['authors']=authors
            request.session['publisher']=publisher
            request.session['title']=title
            request.session['subject']=subject
            q = Books.objects.filter(title__contains=title,authors__contains=authors,publisher__contains=publisher,subject__contains=subject)
            if "login" in request.session and "loginid" in request.session:
                login = request.session["login"]
                loginid = request.session["loginid"]
                return render(request, 'results.html', {'form': form,'login':login,'loginid':loginid, 'booklist':q})

            return render(request, 'results.html', {'form': form, 'booklist':q})


    else:
        form = advsearchform(initial={'authors':' ', 'publisher':' ', 'title':' ', 'subject':' '})

    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        return render(request, 'advsearch.html', {'form': form,'login':login,'loginid':loginid})

    return render(request, 'advsearch.html', {'form': form})

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title'])

        found_entries = Books.objects.filter(entry_query).order_by('title')
        print query_string
        print entry_query
        print found_entries
    return render_to_response('results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def checkout(request):

    # Get the Customer Object and Book Object
    # if "loginid" in request.session:
    # customer = Customers.objects.get(loginid=request.session["loginid"])
    # book = Books.objects.get(isbn=isbn)

    #Create the order object using the Book, Customer object (because they are foreign keys)
    # Orders.objects.create(loginid=customer,order_date=str(datetime.now()),order_status="Pending Order")

    #Get the order number (we do this because it's auto increment so we don't know what's the number)
    # o=Orders.objects.filter(loginid=request.session['loginid']).order_by('-oid')[0]

    #Get the order object
    # order=Orders.objects.filter(oid=o.oid)

    #Save object item
    # order_item = OrderItems(isbn=book,oid=order[0],qty=qty)
    # order_item.save()
    form = loginform(request.POST)
    if "login" in request.session and "loginid" in request.session:

        login = request.session["login"]
        loginid = request.session["loginid"]
        return render (request,'checkout.html',{'login':login,'loginid':loginid})
    else:
        return HttpResponseRedirect('/homepage/login')

def user(request):
    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        user = Customers.objects.filter(loginid=loginid).values()[0]
        cursor = connection.cursor()

        cursor.execute("SELECT books.title, feedbacks.review, feedbacks.optionalComment FROM books,feedbacks WHERE feedbacks.loginID = %s AND books.ISBN = feedbacks.ISBN",[loginid])
        feedbacks = cursor.fetchall()
        cursor.execute("SELECT books.title AS title, ratings.rating AS rating, ratings.ratingID AS rid FROM books,ratings WHERE ratings.feedbackID = %s AND books.ISBN = ratings.ISBN",[loginid])
        ratings = cursor.fetchall()
        cursor.execute("SELECT orders.oid, books.title, order_items.qty, orders.order_date, orders.order_status FROM books,orders,order_items WHERE orders.loginID = %s AND orders.oid = order_items.oid AND order_items.ISBN = books.ISBN",[loginid])
        orders = cursor.fetchall()
        cursor.close()

    return render (request,'user.html',{'user':user, 'orders':orders, 'feedbacks':feedbacks,'ratings':ratings,'login':login,'loginid':loginid})

def admin(request):
    if "login" in request.session and "loginid" in request.session:
        login = request.session["login"]
        loginid = request.session["loginid"]
        user = Customers.objects.filter(loginid=loginid).values()[0]
        cursor = connection.cursor()

        #cursor.execute("SELECT books.title, feedbacks.review, feedbacks.optionalComment FROM books,feedbacks WHERE feedbacks.loginID = %s AND books.ISBN = feedbacks.ISBN",[loginid])
        cursor.execute("SELECT books.title, order_items.isbn AS isbn, sum(order_items.qty) FROM books,order_items,orders WHERE order_items.oid = orders.oid AND orders.order_status=%s AND books.isbn = order_items.isbn group by order_items.isbn order by sum(order_items.qty) DESC LIMIT 5",["Payment Received"])
        #select ISBN, sum(qty) from order_items inner join orders where order_items.oid = orders.oid and orders.order_status='Payment Received' group by ISBN order by sum(qty) DESC limit m
        feedbacks = cursor.fetchall()
        cursor.execute("SELECT books.title AS title, ratings.rating AS rating, ratings.ratingID AS rid FROM books,ratings WHERE ratings.feedbackID = %s AND books.ISBN = ratings.ISBN",[loginid])
        ratings = cursor.fetchall()
        cursor.execute("SELECT orders.oid, books.title, order_items.qty, orders.order_date, orders.order_status FROM books,orders,order_items WHERE orders.loginID = %s AND orders.oid = order_items.oid AND order_items.ISBN = books.ISBN",[loginid])
        orders = cursor.fetchall()
        cursor.close()

    return render (request,'admin.html',{'user':user, 'orders':orders, 'feedbacks':feedbacks,'ratings':ratings,'login':login,'loginid':loginid})
