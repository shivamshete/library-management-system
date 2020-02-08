from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.db import connections
from django.db import models

cursor = connection.cursor()


# Create your views here.
def login(request):
    userexist = False
    message = "username and password does not match"
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']

        query = "SELECT * FROM Login WHERE username = '" + username + "' AND password ='" + password + "';"
        cursor.execute(query)

    if (cursor.fetchone() != None):
        userexist = True
    else:
       return render(request, 'login.html', {'userexist': userexist, 'message': message})
    return render(request, 'index.html', {'userexist': userexist, 'message': message})

def signup(request):
    ssnexist = False
    message = ""
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']

        email = request.POST['email']

        query = "SELECT * FROM Login WHERE username = '" + username + "'"
        cursor.execute(query)

        if (cursor.fetchone() != None):
            ssnexist = True
        else:
            query = 'INSERT INTO Login(username,password,email) VALUES("' + username + '","' + password + '","' + email + '");'
            cursor.execute(query)
            message = "Successfully added the admin ,plz return to login page to login"

    return render(request, 'signup.html', {'ssnexist': ssnexist, 'message': message})


def index(request):
    return render(request, 'index.html')


def addbook(request):
    ssnexist = False
    message = ""
    if (request.method == "POST"):
        isbn = request.POST['isbn']
        title = request.POST['title']
        availability = request.POST['availability']

        query = "SELECT isbn FROM Book WHERE isbn = '" + isbn + "'"
        cursor.execute(query)

        if (cursor.fetchone() != None):
            ssnexist = True
        else:
            query = 'INSERT INTO Book(isbn,title,availability) VALUES("' + isbn + '","' + title + '","' + availability + '");'
            cursor.execute(query)
            message = "Successfully added the book"

    return render(request, 'addbook.html', {'ssnexist': ssnexist, 'message': message})


def removebook(request):
    ssnnotexist = False
    message = ""
    if (request.method == "POST"):
        isbn = request.POST['isbn']

        query = "SELECT isbn FROM Book WHERE isbn = '" + isbn + "';"
        cursor.execute(query)

        if (cursor.fetchone() != None):
            query = 'DELETE  FROM Book WHERE isbn="' + isbn + '";'
            cursor.execute(query)
            message = "Successfully removed the book"
        else:
            ssnnotexist = True

    return render(request, 'removebook.html', {'ssnnotexist': ssnnotexist, 'message': message})


def addstudent(request):
    rollexist = False
    message = ""
    query = "SELECT student.roll, student.name,  student.department, student.phone FROM Student "
    cursor.execute(query)
    books = cursor.fetchall()

    if (request.method == "POST"):
        roll = request.POST['roll']
        name = request.POST['name']
        department = request.POST['department']
        phone = request.POST['phone']

        query = "SELECT roll FROM Student WHERE roll = '" + roll + "'"
        cursor.execute(query)

        if (cursor.fetchone() != None):
            rollexist = True
        else:
            query = 'INSERT INTO Student VALUES("' + roll + '","' + name + '","' + department + '","' + phone + '");'
            cursor.execute(query)

            message = "Successfully added the student"

    return render(request, 'addstudent.html', {'rollexist': rollexist, 'message': message,'books':books})


def issuebook(request):
    ssnexist = False
    message = ""
    if (request.method == "POST"):
        roll = request.POST['roll1']
        name = request.POST['name1']
        title = request.POST['title1']
        dateofissue = request.POST['dateofissue']

        query = "SELECT title FROM Book WHERE title = '" + title + "'"
        cursor.execute(query)

        if (cursor.fetchone() != None):
            query = 'INSERT INTO Issue(roll,name,dateofissue,title,status) VALUES("' + roll + '","' + name + '","' + dateofissue + '","' + title + '","I");'
            cursor.execute(query)
            query= "UPDATE Book set availability=availability-1 where title ='" + title + "'"
            cursor.execute(query)
            message = "now you can give the book to student"

        else:
            ssnexist=True
    return render(request, 'issuebook.html', {'ssnexist': ssnexist, 'message': message})



def checkfine(request):
    return render(request, 'checkfine.html')

def fines(request):
    diff=0
    if (request.method == "POST"):
        roll = request.POST['roll']
        title = request.POST['title']

        #query = "create procedure calc_fine1(in rollno int,in bookname varchar(30)) begin set @datediff=0; set @fineamt=0; select datediff(curdate(),dateofissue) from Issue where roll=rollno and title=bookname into @datediff; if @datediff>15 and @datediff<=30 then set @fineamt=(@datediff-15)*5; " \
         #       "elseif @datediff>30 then set @fineamt=((15*5)+(@datediff-30)*50);  else set @fineamt=0;end if;" \
          #      "update Issue set status='R' where roll=rollno and title=bookname; " \
           #     "insert into Fine values(rollno,curdate(),@fineamt); end"
        #cursor.execute(query)
        #query = "call calc_fine('" + roll + "','" + title + "');"

        #cursor.execute(query)
        query="select datediff(curdate(),dateofissue) from Issue where roll= '"+ roll +"' and title= '"+ title +"';"
        cursor.execute(query)
        results=cursor.fetchall()
        for result in results:
            query="insert into Fine(roll,sdate,amt) values ('"+roll+"',curdate(),'"+ str(result[0])+"')"
            cursor.execute(query)


        print(diff)
        sql = "select amt from Fine where roll = (%s)"
        val = (roll,)
        cursor.execute(sql, val)
        amount = cursor.fetchmany(size=1)
        sql = "select dateofissue from Issue where roll = (%s)"
        val = (roll,)
        cursor.execute(sql, val)
        issuedate = cursor.fetchmany(size=1)
        sql = "select title from Issue where roll= (%s)"
        val = (roll,)
        cursor.execute(sql, val)
        bookname = cursor.fetchmany(size=1)
        record = [roll, amount[0][0], issuedate[0][0],bookname[0][0]]

    return render(request, 'fines.html', {'record': record})

def showbooks(request):
    books = ""
    message = ""
    get = True
    if (request.method == "POST"):
        if ('search' in request.POST):
            get = False
            keywords = request.POST['search'].split(',')
            comparision = ""
            for keyword in keywords:
                keyword = keyword.strip()
                keyword = "%" + keyword + "%"
                if (comparision != ""):
                    comparision += " AND "
                comparision += "(Book.isbn LIKE '" + keyword + "' OR Book.title LIKE '" + keyword + "' )"

            query = "SELECT Book.isbn, Book.title,  Book.Availability FROM Book   WHERE " + comparision
            cursor.execute(query)
            books = cursor.fetchall()
            return render(request, 'showbooks.html', {'books': books, 'message': "", 'get': get})

        elif ('cardno' in request.POST):
            keywords = request.POST['cardno'].split(',')
            print(keywords)
            cardno = keywords[0]
            isbn = keywords[1]
            print(cardno, isbn)
            query = "SELECT COUNT(Card_id) FROM Borrower WHERE Card_id = '" + cardno + "' GROUP BY Card_id"
            cursor.execute(query)

            if (cursor.fetchone() != None):
                query = "SELECT COUNT(Loan_id) FROM Book_Loans WHERE Book_Loans.Card_id = '" + str(
                    cardno) + "' AND Book_Loans.Date_in IS NULL GROUP BY Book_Loans.Card_id"
                cursor.execute(query)
                result = cursor.fetchone()
                if (result == None):
                    query = "SELECT Book.Availability FROM Book WHERE Book.Isbn = '" + isbn + "'"
                    cursor.execute(query)
                    availability = cursor.fetchone()
                    if (availability[0] == 1):
                        query = 'INSERT INTO Book_Loans(Isbn, Card_id, Date_out, Due_date, Date_in) VALUES("' + isbn + '","' + str(
                            cardno) + '",CURDATE(),DATE_ADD(Date_out,INTERVAL 14 DAY),NULL)'
                        cursor.execute(query)
                        query = 'UPDATE Book SET Book.Availability = "0" WHERE Book.isbn = "' + isbn + '"'
                        cursor.execute(query)
                        message = "Successfully checked out book. Return within 14 days to avoid fine"
                    else:
                        message = "Book is not available"
                else:
                    query = "SELECT Book.Availability FROM Book WHERE Book.Isbn = '" + isbn + "'"
                    cursor.execute(query)
                    if (result[0] < 3):
                        query = 'INSERT INTO Book_Loans(Isbn, Card_id, Date_out, Due_date, Date_in) VALUES("' + isbn + '","' + str(
                            cardno) + '",CURDATE(),DATE_ADD(Date_out,INTERVAL 14 DAY),NULL)'
                        cursor.execute(query)
                        query = 'UPDATE Book SET Book.Availability = "0" WHERE Book.isbn = "' + isbn + '"'
                        cursor.execute(query)
                        message = "Successfully checked out book. Return within 14 days to avoid fine"
                    else:
                        message = "Maximum of only 3 books can be checked out"
            else:
                message = "Invalid Card Number."

            return render(request, 'showbooks.html', {'books': books, 'message': message, 'get': get})

        else:
            print(request.POST)
            return render(request, 'showbooks.html', {'books': books, 'message': message, 'get': get})

    else:
        return render(request, 'showbooks.html', {'books': books, 'message': message, 'get': get})
