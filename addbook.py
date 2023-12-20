from tkinter import *
from tkinter import messagebox
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="root", database="libraryV")
cur = con.cursor()


def AddBook():
    top = Toplevel()
    top.geometry("650x600+550+200")
    top.title("Add Book")
    top.resizable(False, False)

    #######################Frames#######################

    # Top Frame
    topFrame = Frame(top, height=150, bg='white')
    topFrame.pack(fill=X)
    # Bottom Frame
    bottomFrame = Frame(top, height=600, bg='#fcc324')
    bottomFrame.pack(fill=X)
    # heading, image
    top_image = PhotoImage(file='icons/addbook.png')
    top_image_lbl = Label(topFrame, image=top_image, bg='white')
    top_image_lbl.place(x=120, y=10)
    heading = Label(topFrame, text='  Add Book ', font='arial 22 bold', fg='#003f8a', bg='white')
    heading.place(x=290, y=60)

    ###########################################Entries and Labels########################3

    # name
    lbl_name = Label(bottomFrame, text='Name :', font='arial 15 bold', fg='white', bg='#fcc324')
    lbl_name.place(x=40, y=40)
    ent_name = Entry(bottomFrame, width=30, bd=4)
    ent_name.insert(0, 'Please enter a book name')
    ent_name.place(x=150, y=45)
    # author
    lbl_author = Label(bottomFrame, text='Author :', font='arial 15 bold', fg='white', bg='#fcc324')
    lbl_author.place(x=40, y=80)
    ent_author = Entry(bottomFrame, width=30, bd=4)
    ent_author.insert(0, 'Please enter a author name')
    ent_author.place(x=150, y=85)
    # page
    lbl_page = Label(bottomFrame, text='Page :', font='arial 15 bold', fg='white', bg='#fcc324')
    lbl_page.place(x=40, y=120)
    ent_page = Entry(bottomFrame, width=30, bd=4)
    ent_page.insert(0, 'Please enter page size')
    ent_page.place(x=150, y=125)
    # language
    lbl_language = Label(bottomFrame, text='Language :', font='arial 15 bold', fg='white', bg='#fcc324')
    lbl_language.place(x=40, y=160)
    ent_language = Entry(bottomFrame, width=30, bd=4)
    ent_language.insert(0, 'Please enter a Language')
    ent_language.place(x=150, y=165)

    # Button

    def addBook():
        name = ent_name.get()
        author = ent_author.get()
        page = ent_page.get()
        language = ent_language.get()
        if (name and author and page and language != ""):
            try:
                query = "INSERT INTO books (book_name,book_author,book_page,book_language) VALUES(%s,%s,%s,%s)"
                cur.execute(query, (name, author, page, language))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database", icon='info')

            except:
                messagebox.showerror("Error", "Cant add to database", icon='warning')
        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')

    button = Button(bottomFrame, text='Add Book', command=addBook)
    button.place(x=270, y=200)
    top.mainloop()
