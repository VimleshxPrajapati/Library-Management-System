from tkinter import *
from tkinter import messagebox
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="root", database="libraryV")
cur = con.cursor()


def AddMember():
    top = Toplevel()
    top.geometry("650x600+550+200")
    top.title("Add Member")
    top.resizable(False, False)

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
    heading = Label(topFrame, text='  Add Person ', font='arial 22 bold', fg='#003f8a', bg='white')
    heading.place(x=290, y=60)

    ###########################################Entries and Labels########################3

    # member name
    lbl_name = Label(bottomFrame, text='Name :', font='arial 15 bold', fg='white', bg='#fcc324')
    lbl_name.place(x=40, y=40)
    ent_name = Entry(bottomFrame, width=30, bd=4)
    ent_name.insert(0, 'Please enter Person name')
    ent_name.place(x=150, y=45)
    # phone
    lbl_phone = Label(bottomFrame, text='Phone :', font='arial 15 bold', fg='white', bg='#fcc324')
    lbl_phone.place(x=40, y=80)
    ent_phone = Entry(bottomFrame, width=30, bd=4)
    ent_phone.insert(0, 'Please enter Phone Number')
    ent_phone.place(x=150, y=85)

    def addMember():
        name = ent_name.get()
        phone = ent_phone.get()
        if (name and phone != ""):
            try:
                query = "INSERT INTO members (member_name,member_phone) VALUES(%s,%s)"
                cur.execute(query, (name, phone))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database", icon='info')

            except:
                messagebox.showerror("Error", "Cant add to database", icon='warning')
        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')

    # Button
    button = Button(bottomFrame, text='Add Member', command=addMember)
    button.place(x=270, y=120)
    top.mainloop()
