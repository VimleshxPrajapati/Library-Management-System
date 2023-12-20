from tkinter import *
from tkinter import ttk
import addbook, givebook, addmember
import mysql.connector
from tkinter import messagebox

con = mysql.connector.connect(host="localhost", user="root", password="root", database="libraryv")
cur = con.cursor()


def addBoook():
    addbook.AddBook()


def giveBoook():
    givebook.GiveBook()


def addMemberr():
    addmember.AddMember()


def searchBooks():
    value = ent_search.get()
    cur.execute("SELECT * FROM books WHERE book_name LIKE %s", ('%' + value + '%',))
    search = cur.fetchall()
    print(search)
    list_books.delete(0, END)
    count = 0
    for book in search:
        list_books.insert(count, str(book[0]) + "-" + book[1])
        count += 1


def listBooks():
    value = listChoice.get()
    if value == 1:
        cur.execute("SELECT * FROM books")
        allbooks = cur.fetchall()
        list_books.delete(0, END)

        count = 0
        for book in allbooks:
            list_books.insert(count, str(book[0]) + "-" + book[1])
            count += 1

    elif value == 2:
        cur.execute("SELECT * FROM books WHERE book_status =%s", (0,))
        books_in_library = cur.fetchall()
        list_books.delete(0, END)

        count = 0
        for book in books_in_library:
            list_books.insert(count, str(book[0]) + "-" + book[1])
            count += 1
    else:
        cur.execute("SELECT * FROM books WHERE book_status =%s", (1,))
        taken_books = cur.fetchall()
        list_books.delete(0, END)

        count = 0
        for book in taken_books:
            list_books.insert(count, str(book[0]) + "-" + book[1])
            count += 1


def displayBooks(evt):
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    count = 0
    list_books.delete(0, END)
    for book in books:
        print(book)
        list_books.insert(count, str(book[0]) + "-" + book[1])
        count += 1

    def bookInfo(evt):
        value = str(list_books.get(list_books.curselection()))
        id = value.split('-')[0]
        cur.execute("SELECT * FROM books WHERE book_id=%s", (id,))
        book_info = cur.fetchall()
        print(book_info)
        list_details.delete(0, 'end')
        list_details.insert(0, "Book Name : " + book_info[0][1])
        list_details.insert(1, "Author : " + book_info[0][2])
        list_details.insert(2, "Page : " + book_info[0][3])
        list_details.insert(3, "Language : " + book_info[0][4])
        if book_info[0][5] == 0:
            list_details.insert(4, "Status : Avaiable")
        else:
            list_details.insert(4, "Status : Not Avaiable")

    def doubleClick(evt):
        global given_id
        value = str(list_books.get(list_books.curselection()))
        given_id = value.split('-')[0]
        givebook.GiveBook()

    def displayStatistics(evt):
        cur.execute("SELECT count(book_id) FROM books")
        count_books = cur.fetchall()
        cur.execute("SELECT count(member_id) FROM members")
        count_members = cur.fetchall()
        cur.execute("SELECT count(book_status) FROM books WHERE book_status=1")
        taken_books = cur.fetchall()
        print(count_books)
        lbl_book_count.config(text='Total :' + str(count_books[0][0]) + ' books in library')
        lbl_member_count.config(text="Total member : " + str(count_members[0][0]))
        lbl_taken_count.config(text="Taken books :" + str(taken_books[0][0]))
        # displayBooks()

    list_books.bind('<<ListboxSelect>>', bookInfo)
    tabs.bind('<<NotebookTabChanged>>', displayStatistics)
    list_books.bind('<Double-Button-1>', doubleClick)


root = Tk()
root.title("Library Management System")
root.geometry("1200x650")
root.iconbitmap("icons/icon.ico")
topFrame = Frame(root, width=1200, height=60, bg='#f8f8f8', padx=20, relief=SUNKEN, borderwidth=2)
topFrame.pack(side=TOP, fill=X)
# center frame
centerFrame = Frame(root, width=1200, relief=RIDGE, bg='#e0f0f0', height=530)
centerFrame.pack(side=TOP)
# Center Left Frame
centerLeftFrame = Frame(centerFrame, width=850, height=600, bg='#e0f0f0', borderwidth=2, relief='sunken')
centerLeftFrame.pack(side=LEFT)
# center right frame
centerRightFrame = Frame(centerFrame, width=350, height=600, bg='#e0f0f0', borderwidth=2, relief='sunken')
centerRightFrame.pack()

# search bar
search_bar = LabelFrame(centerRightFrame, width=340, height=75, text='Search Box', bg='#9bc9ff')
search_bar.pack(fill=BOTH)
lbl_search = Label(search_bar, text='Search :', font='arial 12 bold', bg='#9bc9ff', fg='white')
lbl_search.grid(row=0, column=0, padx=20, pady=10)
ent_search = Entry(search_bar, width=30, bd=5)
ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
btn_search = Button(search_bar, text='Search', font='arial 12', bg='#fcc324', fg='white', command=searchBooks)
btn_search.grid(row=0, column=4, padx=20, pady=10)

# list bar
list_bar = LabelFrame(centerRightFrame, width=340, height=175, text='List Box', bg='#fcc324')
list_bar.pack(fill=BOTH)
lbl_list = Label(list_bar, text='Sort By', font='times 16 bold', fg='#2488ff', bg='#fcc324')
lbl_list.grid(row=0, column=2)
listChoice = IntVar()
rb1 = Radiobutton(list_bar, text='All Books', var=listChoice, value=1, bg='#fcc324')
rb2 = Radiobutton(list_bar, text='In Library', var=listChoice, value=2, bg='#fcc324')
rb3 = Radiobutton(list_bar, text='Borrowed Books', var=listChoice, value=3, bg='#fcc324')
rb1.grid(row=1, column=0)
rb2.grid(row=1, column=1)
rb3.grid(row=1, column=2)
btn_list = Button(list_bar, text='List Books', bg='#2488ff', fg='white', font='arial 12', command=listBooks)
btn_list.grid(row=1, column=3, padx=40, pady=10)

# title and image
image_bar = Frame(centerRightFrame, width=340, height=350)
image_bar.pack(fill=BOTH)
title_right = Label(image_bar, text='Welcome to our Library', font='arial 16 bold')
title_right.grid(row=0)
img_library = PhotoImage(file='icons/library.png')
lblImg = Label(image_bar, image=img_library)
lblImg.grid(row=1)

# add book
iconbook = PhotoImage(file='icons/add_book.png')
btnbook = Button(topFrame, text='Add Book', image=iconbook, compound=LEFT, font='arial 12 bold', command=addBoook)
btnbook.pack(side=LEFT)
# add member button
iconmember = PhotoImage(file='icons/users.png')
btnmember = Button(topFrame, text='Add Member', font='arial 12 bold', image=iconmember, compound=LEFT,
                   command=addMemberr)
btnmember.pack(side=LEFT, padx=5,pady=5)
# give book
icongive = PhotoImage(file='icons/givebook.png')
btngive = Button(topFrame, text='Give Book', font='arial 12 bold', padx=10, image=icongive, compound=LEFT,
                 command=giveBoook)
btngive.pack(side=LEFT)

###############tab1###############################
tabs = ttk.Notebook(centerLeftFrame, width=730, height=580)
tabs.pack()
tab1_icon = PhotoImage(file='icons/books.png')
tab2_icon = PhotoImage(file='icons/members.png')
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tabs.add(tab1, text='Library Management', image=tab1_icon, compound=LEFT)
tabs.add(tab2, text='Statistics', image=tab2_icon, compound=LEFT)
tabs.bind('<ButtonRelease-1>', displayBooks)
# list books
list_books = Listbox(tab1, width=40, height=25, bd=5, font='times 12 bold')
sb = Scrollbar(tab1, orient=VERTICAL)
list_books.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
sb.config(command=list_books.yview)
list_books.config(yscrollcommand=sb.set)
sb.grid(row=0, column=0, sticky=N + S + E)

# list details
list_details = Listbox(tab1, width=80, height=20, bd=5, font='times 12 bold')
list_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)

b=Button(tab1,text="__Coded By Vi__",font='times 20 bold')
b.grid(row=0, column=1,padx=90,pady=20 ,sticky=SW)

##########################tab2####################################
# statistics
lbl_book_count = Label(tab2, text="", pady=20, font='verdana 14 bold')
lbl_book_count.grid(row=0)
lbl_member_count = Label(tab2, text="", pady=20, font='verdana 14 bold')
lbl_member_count.grid(row=1, sticky=W)
lbl_taken_count = Label(tab2, text="", pady=20, font='verdana 14 bold')
lbl_taken_count.grid(row=2, sticky=W)
displayBooks("")

root.mainloop()
