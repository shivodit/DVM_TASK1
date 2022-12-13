# 
# from .script import populate
import openpyxl as xl
import os.path 
import pickle 

DAT_FILE = "PROG.dat"


class Book():
    def __init__(self,name,author,isbn):
        self.name = name
        self.author = author
        self.isbn = isbn
        self.borrow = ''
        self.reserve = ''

    def borrow_book(self,borrower):
        if self.is_available():
            self.reserve = ''
            self.borrow = borrower
        else :
            print('book is not available right now. ')

    def return_book(self,borrower):
        if self.borrow == borrower:
            self.borrow = ''

    def reserve_book(self,borrower):
        if self.is_available():
            self.reserve = borrower
        else:
            print('book is not available right now.')
    
    def is_available(self):
        if self.borrow == '' and self.reserve =='':
            return True
        else :
            return False        

    def __str__(self):
        print("{:13} | {:13} | {:13} ".format(self.name,self.author,self.isbn))

class Shelf():
    def __init__(self,genre):
        self.genre = genre
        self.catalog = []

    def show_catalog(self):
        print("{:13} | {:25} | {:35} ".format("NAME","AUTHOR","ISBN"))
        for i in self.catalog:
            print(i)

    def add_book(self,book,user_type):
        if user_type != "LIB":
            print("Not Authorized! ")
            return 
        self.catalog.append(book)

    def remove_book(self,index,user_type):
        if user_type != "LIB":
            print("Not Authorized! ")
            return 
        try:
            self.catalog.pop(index)
        except KeyError:
            print("book of this index is not in the self")
    

    def get_books_count(self):
        return len(self.catalog)

    def populate_book(self,file_name,user_type):
        workbook = xl.load_workbook(filename=file_name)
        sheet = workbook.active
        dim = sheet.calculate_dimension()
        for row in sheet[dim]:
            if row[0].value in ("Name",""):
                continue
            
            self.add_book(Book(*[i.value for i in row]),user_type)
    
    def __str__(self):
        return f"genre - {self.genre} total books - {self.get_books_count()}"


class User():
    def __init__(self,name,password,user_type):
        self.name = name 
        self.password = password
        self.user_type = user_type

    def __str__(self):
        return f"{self.name}- type - {self.user_type}"

def save_prog(database):
    with open(DAT_FILE,"wb") as f:
        pickle.dump(database,f)

def fetch_prog():
    if os.path.exists(DAT_FILE):    
        with open(DAT_FILE,"rb") as f:
            return pickle.load(f)
    else:
        users = []
        shelves = []
        database = {"users":users,"shelves":shelves}
        return database

def user_handle(users):
    menu = "1. login\n2. register"
    option = int(input(menu))
    if option == 1:
        name = input("name: ")
        password = input("password: ")
        for i in users:
            if i.name == name and i.password == password:
                return i, users
            else :
                print('please try again or register as a new user')
                return user_handle(users)
    if option == 2:
        name = input("name: ")
        password = input("password: ")
        user_type = input("user_type: (LIB/USR) ")
        user = User(name,password,user_type)
        users.append(user)
        return user, users

def select_shelf(shelves):
    genre = input("Please enter the genre of the shelf: ")
    for i in shelves:
        if i.genre == genre:
            return i
        else:
            print("no genre")
            return 0


# while 1:
#     i = input(">> ")
#     if i == "^Z":
#         break
#     try:
#         print(eval(i))
#     except:
#         print(exec(i))


database = fetch_prog()
users, shelves = database["users"], database["shelves"]
current_user,users = user_handle(users)
database["users"] = users
save_prog(users)

# while 1:
#     """under construction :) """
#     if current_user.user_type == 'USR':
#         print("0. exit\n1. borrow book\n2. reserve book\n3. return book \n")
#         option = input() 
#     elif current_user.user_type == 'LIB':
#         print("0. exit\n1. add shelf\n2. add book\n3. remove book\n")
#         option = input() 
