from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="root", database="libraryV")
cur = con.cursor()


def GiveBook():
    top = Toplevel()
    top.geometry("650x600+550+200")
    top.title("Lend Book")
    top.resizable(False, False)

    cur.execute("SELECT * FROM books WHERE book_status=0")
    books = cur.fetchall()
    book_list = []
    for book in books:
        book_list.append(str(book[0]) + "-" + book[1])
    print(book_list)
    query2 = "SELECT * FROM members"
    cur.execute(query2)
    members = cur.fetchall()
    member_list = []
    for member in members:
        member_list.append(str(member[0]) + "-" + member[1])
    #######################Frames#######################

    # Top Frame
    topFrame = Frame(top, height=150, bg='white')
    topFrame.pack(fill=X)
    # Bottom Frame
    bottomFrame = Frame(top, height=600, bg='#fcc324')
    bottomFrame.pack(fill=X)
    # heading, image
    top_image = PhotoImage(file='icons/addperson.png')
    top_image_lbl = Label(topFrame, image=top_image, bg='white')
    top_image_lbl.place(x=120, y=10)
    heading = Label(topFrame, text='  Lend a Book ', font='arial 22 bold', fg='#003f8a', bg='white')
    heading.place(x=290, y=60)

    ###########################################Entries and Labels########################3

    # member name
    book_name = StringVar()
    lbl_name = Label(bottomFrame, text='Book: ', font='arial 15 bold', fg='white', bg='#fcc324')
    lbl_name.place(x=40, y=40)
    combo_name = ttk.Combobox(bottomFrame, textvariable=book_name)
    combo_name['values'] = book_list
    combo_name.place(x=150, y=45)

    # phone
    member_name = StringVar()
    lbl_phone = Label(bottomFrame, text='Member: ', font='arial 15 bold', fg='white', bg='#fcc324')
    lbl_phone.place(x=40, y=80)
    combo_member = ttk.Combobox(bottomFrame, textvariable=member_name)
    combo_member['values'] = member_list
    combo_member.place(x=150, y=85)

    def lendBook():
        member = member_name.get()
        book = book_name.get()
        book_id = book.split('-')[0]
        print(member, book, book_id)
        if (book and member != ""):
            try:
                query = "INSERT INTO borrows (bbook_id,bmember_id) VALUES(%s,%s)"
                cur.execute(query, (book, member))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database!", icon='info')
                cur.execute("UPDATE books SET book_status =%s WHERE book_id=%s", (1, book_id))
                con.commit()
            except:
                messagebox.showerror("Error", "Cant add to database", icon='warning')

        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')

    # Button
    button = Button(bottomFrame, text='Lend Book', command=lendBook)
    button.place(x=220, y=120)
    top.mainloop()
