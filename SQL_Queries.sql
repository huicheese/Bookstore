   
--check for uniqueness of ID
select case when exists(select * from customers where loginID="requested user name" limit 1) then cast(1 as bit) else cast(0 as bit) end
    --Returns 1 if there exists a user with the loginID
    --Returns 0 otherwise

--registration of a new user
insert into customers values (fullname, loginID, pw, majorCCN, address, phoneNum)
-- Ordering: After registration, a user can order one or more books. A user may order multiple copies of a book, one or more times. (The charging of the credit card and the shipment of the books are outside the scope of this project).

--    Orders table
insert into orders(loginID, order_date,order_status) values ('mhatib',datetime('now'),'Pending Order');

--Order_items table
insert into order_items values ((select oid from orders where order_date=(select MAX(order_date) from orders) and loginID=’loginID’'),'978-0253009081',5)


--User record: upon user demand, you should print the full record of a user: • his/her account information • his/her full history of orders (book name, number of copies, date etc.) • his/her full history of feedbacks • the list of all the feedbacks he/she ranked with respect to usefulness   
--  his/her account information
    select * from customers where loginID=’loginID’ limit 1

--  his/her full history of orders
    select * from hasOrders where loginID='loginID'

--<????> select * from Orders O inner join Order_items OI on O.oid=OI.oid where O.loginID=<LOGINID>;



--   -list of all feedbacks he/she ranked with respect to usefulness
    select * from ratings where ratingID=’loginID’

--   -his/her full history of feedbacks
    select * from feedback where loginID='loginID'
-- New book: The store manager records the details of a new book, along with the number of new books that have arrived in the warehouse.

    insert into books VALUES ('ISBN','title','author','publisher', 1999, 9, 99, 'Hardcover', 'keyword','subject','https://url_to_book_image’)

-- Arrival of more copies: The store manager increases the number of copies in inventory.
    
    update books set stock=3 where ISBN='ISBN'

--Feedback recordings: Users can record their feedback for a book. You should record the date, the numerical score (0= terrible, 10= wonderful), and an optional short text. No changes are allowed; only one feedback per user per book is allowed.

    insert into feedback VALUES (‘loginID’,'ISBN','5',’optional_comments’,’20120618 10:34:09 AM‘)


--Usefulness ratings: Users can assess other uses’ feedback, give a numerical score 0, 1, or 2 (’useless’, ’useful’, ’very useful’ respectively). A user is not allowed to rate his/her own feedback.

    insert into ratings values (‘ISBN’,’feedbackID’,’ratingID’,1)

--Book Browsing: Users may search for books, by asking conjunctive queries on the authors, and/or publisher, and/or title, and/or subject. Your system should allow the user to specify that the results are to be sorted a) by year, or b) by the average score of the feedbacks.

select *  from books where title like ‘%title_key%’ or authors like ‘%author_key%” or  publisher or ‘%publisher_key%” or subject like “%subject_key%” Order by yearPublished ASC

--//Just delete the [and attribute “%keyword%”] when the user does not want it. 
    

--Useful feedbacks: For a given book, a user could ask for the top n most ‘useful’ feedbacks. The value of n is user-specified (say, 5, or 10). The ‘usefulness’ of a feedback is its average ‘usefulness’ score.

select avg(rating) from (select * from ratings where ISBN='b') group by feedbackID

select * from feedbacks where (ISBN = '978-0345803481') AND loginID IN (select feedbackID from (select * from ratings where ISBN='978-0345803481') group by feedbackID ORDER BY avg(rating) DESC LIMIT 5) 

--Book recommendation: Like most e-commerce websites, when a user orders a copy of book ‘A’, your system should give a list of other suggested books. Book ‘B’ is suggested, if there exist a user ‘X’ that bought both ‘A’ and ‘B’. The suggested books should be sorted on decreasing sales count (i.e., most popular first); count only sales to users like ‘X’ (i.e. the users who bought both ‘A’ and ‘B’).

    select ISBN,sum(qty) from (select * from order_items inner join orders where order_items.oid=orders.oid and orders.order_status='Payment Received' and loginID<>'mhatib') inner join (select loginID as idl from order_items inner join orders where order_items.oid = orders.oid and orders.order_status='Payment Received' and loginID<>'mhatib' and ISBN='978-0253009081') group by ISBN order by sum(qty) DESC limit 1

--Statistics: Every month, the store manager wants • the list of the m most popular books (in terms of copies sold in this month) • the list of m most popular authors • the list of m most popular publishers

  --  -list of the m most popular books (in terms of copies sold in this month =k)

    select ISBN, sum(qty) from order_items inner join orders where order_items.oid = orders.oid and orders.order_status='Payment Received' group by ISBN order by sum(qty) DESC limit m

    --list of m most popular authors 

select authors, sum(sqt) from (select ISBN as tis, sum(qty) as sqt from order_items inner join orders where order_items.oid = orders.oid and orders.order_status='Payment Received' group by ISBN order by sum(qty)) as a inner join books where tis=books.ISBN group by authors order by sum(sqt) DESC limit m

    --list of m most popular publishers

select publisher, sum(sqt) from (select ISBN as tis, sum(qty) as sqt from order_items inner join orders where order_items.oid = orders.oid and orders.order_status='Payment Received' group by ISBN order by sum(qty)) as a inner join books where tis=books.ISBN group by publisher order by sum(sqt) DESC limit m
