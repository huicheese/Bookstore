create table books(
    ISBN char(15),
    title char(50) NOT NULL,
    authors char(100) NOT NULL,
    publisher char(50) NOT NULL,
    yearPublished int(4) NOT NULL,
    stock int NOT NULL CHECK(stock>=0),
    price float NOT NULL CHECK(price>=0),
    format char(9) CHECK(format='Hardcover'OR format='Softcover'),
    keywords char(100),
    subject char(100),
    picture text,
    PRIMARY KEY (ISBN)
);


create table customers(
    fullName char(100) NOT NULL,
    loginID char(30),
    pw char(50) NOT NULL,
    majorCCN char(19),
    address char(100) NOT NULL,
    phoneNum char(25),
    PRIMARY KEY (loginID)
);


create table orders(
    oid INTEGER PRIMARY KEY AUTOINCREMENT,
    loginID char(30) NOT NULL,
    order_date time NOT NULL,
    order_status char(30),
    CHECK(order_status ='Pending Order'
        OR order_status='Payment Received'
        OR order_status='Shipped'
        OR order_status='Canceled'
        OR order_status='Returned'),
    foreign key (loginID) references customers(loginID)
);


create table order_items(
    oid INTEGER,
    ISBN char(15),
    qty int NOT NULL CHECK (qty >=0),
    primary key (ISBN, oid),
    foreign key (ISBN) references books(ISBN)
    foreign key (oid) references orders(oid)
);



create table feedbacks(
    loginID char(30) not null,
    ISBN char(15) not null,
    review INTEGER CHECK(review>=1 AND review <=10),
    optionalComment text,
    feedback_date time not null,
    primary key(loginID, ISBN),
    foreign key (loginID) references customers(loginID),
    foreign key (ISBN) references books(ISBN)
);

create table ratings(
    ISBN char(15),
    feedbackID char(30) CHECK(feedbackID != ratingID),
    ratingID char(30),
    rating INTEGER CHECK (rating>=0 AND rating <=2),
    primary key (ISBN, feedbackID, ratingID),
    foreign key (ratingID) references customers(loginID),
    foreign key (feedbackID, ISBN) references feedbacks(loginID, ISBN)
);

drop table feedbacks;
drop table ratings;
drop table order_items;
drop table orders;
drop table books;
drop table customers;


insert into customers VALUES ('full name','loginID','password', 'majorCCN','address','696969696969');
insert into customers VALUES ('full name','loginID2','password', 'majorCCN','address','696969696969');
insert into books VALUES ('b','title','author','publisher', 1999, 9, 99, 'Hardcover', 'keyword','subject','https://www.google.com.sg/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0CAcQjRxqFQoTCMi-uqvcg8kCFUdVjgodEuMHEw&url=http%3A%2F%2Fwww.pearsonhighered.com%2Feducator%2Fproduct%2FComputer-Networking-A-TopDown-Approach-5E%2F9780136079675.page&psig=AFQjCNHjfi_1vQ7Y8tPhOqb1edlShwnaMw&ust=1447171565211177');
insert into orders(loginID,order_date,order_status) VALUES ('loginID',1999-02-15,'Shipped');
insert into feedbacks VALUES ('loginID','b',1,'wow this book sucks',1999-09-11);
insert into order_items VALUES (1, 'b',1);
insert into ratings VALUES ('b','loginID','loginID2',0);

select * from books;
select * from customers;
select * from orders;
