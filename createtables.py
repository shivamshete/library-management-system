import pymysql

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'lib1'

myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database)

def createTableBook(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE Book(isbn VARCHAR(10) NOT NULL, title VARCHAR(255), availability INT NOT NULL DEFAULT 1, CONSTRAINT BKPK PRIMARY KEY(isbn));'
    cur.execute(query)
    print("Created Table Book")

def createTableStudent(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE Student(roll INT NOT NULL PRIMARY KEY, name VARCHAR(255) NOT NULL , department VARCHAR(20) NOT NULL , phone BIGINT NOT NULL);'
    cur.execute(query)
    print("Created Table Student")

def createTableIssue(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE Issue(roll INT, name VARCHAR(255)  ,dateofissue DATE , title VARCHAR(255) NOT NULL, status VARCHAR(20) ,FOREIGN KEY(roll) REFERENCES Student(roll));'
    cur.execute(query)
    print("Created Table Issue")

def createTableLogin(conn):
    cur = conn.cursor()
    query = 'CREATE TABLE Login(username VARCHAR(255) NOT NULL PRIMARY KEY  ,password VARCHAR(255) , email VARCHAR(255) );'
    cur.execute(query)
    print("Created Table Login")

def createTableFine(conn):
    cur = conn.cursor()
    query = 'create table Fine(roll int,sdate date,amt int);'
    cur.execute(query)
    print("Created Table Fine")


cursor = myConnection.cursor()
cursor.execute("DROP SCHEMA lib1;")
cursor.execute("CREATE SCHEMA lib1;")
cursor.execute("USE lib1;")

createTableBook(myConnection)
createTableStudent(myConnection)
createTableIssue(myConnection)
createTableLogin(myConnection)
createTableFine(myConnection)
#createTableAuthors(myConnection)
#createTableBorrower(myConnection)
#createTableBookLoans(myConnection)
#createTableFines(myConnection)
myConnection.close()