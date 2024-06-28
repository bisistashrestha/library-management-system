import pymysql as mysql
import customtkinter as ctk
import tkinter as tk
from PIL import Image
from tkinter import messagebox,Grid
from CTkTable import *
import time
import datetime

#Login Function
def login_account():
    username=username_entry2.get()
    password=password_entry2.get()
    if username!='' and password!='':
        cur.execute("Select password from users where username='{}';".format(username))
        result=cur.fetchone()
        if result:
            if result[0]==password:
                messagebox.showinfo("Success", "Logged In Successfully.")
                home()
            else:
                messagebox.showerror("Error", "Invalid Password.")
        else:
            messagebox.showerror("Error", "Account Not Found.")
    else:
        messagebox.showerror("Error", "Enter All Data.")         

#Login Page
def login():
    frame2=ctk.CTkFrame(master=image_label, width=320, height=360, corner_radius=15, fg_color="white")
    frame2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    login_l2=ctk.CTkLabel(master=frame2, text="Login", font=('Calibri', 30), text_color="black")
    login_l2.place(x=60, y=45)

    global username_entry2
    global password_entry2

    username_entry2=ctk.CTkEntry(master=frame2, placeholder_text="Username", width=220)
    username_entry2.place(x=50, y=110)

    password_entry2=ctk.CTkEntry(master=frame2, placeholder_text="Password", width=220, show="*")
    password_entry2.place(x=50, y=165)

    login_button2=ctk.CTkButton(master=frame2, width=90, text="Login", corner_radius=10, cursor='hand2', command=login_account, font=('Calibri', 15), text_color="black")
    login_button2.place(x=110, y=220)

#Home Page
def home():
    global username_entry2
    username=username_entry2.get()
    window.destroy()
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    home=ctk.CTk()
    home.title("Library Management System")
    width,height=1200,420
    v_dim=str(width)+'x'+str(height)
    home.geometry(v_dim)
    home.minsize(950,300)
    home.maxsize(1200,420)

    Grid.rowconfigure(home,0,weight=1)
    Grid.columnconfigure(home,1,weight=1)

    dashboard_frame=ctk.CTkFrame(master=home, width=300, height=700, corner_radius=15, fg_color="black")
    dashboard_frame.grid(row=0,column=0,padx=15,pady=4,sticky="NSEW")

    mainframe=ctk.CTkScrollableFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="black")
    mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
    
    #All Members Page for Admin
    def AllMembers():
        #Function to show all members table
        def memtable():
            cur.execute("Select * from members order by {};".format(SortByMemberOptionmenu.get()))
            data=cur.fetchall()
            value=[('Member ID','Member Name','Age','Gender','Email','Phone Number')]
            for i in data:
                value.append(i)
            table = CTkTable(mainframe, row=len(data)+1, column=6, values=value, header_color="#17E490", text_color=("white","black"), colors=["white", "white"],corner_radius=15)
            table.grid(row=2,column=1,pady=18,columnspan=6,sticky="nsew")

        #Fuction to search members
        def searchmem():
            key=SearchMember.get()
            cur.execute("Select * from members where Member_ID like '%{}%' or Name like '%{}%' or Email like '%{}%' or Phone_Number like '%{}%' order by {};".format(key,key,key,key,SortByMemberOptionmenu.get()))
            data=cur.fetchall()
            cur.execute("select * from members;")
            data2=cur.fetchall()
            value=[('Member ID','Member Name','Age','Gender','Email','Phone Number')]
            for i in data:
                value.append(i)
            table2 = CTkTable(mainframe, row=len(data2)+1, column=6, values=value, header_color="#17E490", text_color=("white","black"), colors=["white", "white"])
            table2.grid(row=2,column=1,pady=18,columnspan=6,sticky="nsew")

        #Window Layout
        mainframe=ctk.CTkScrollableFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="black")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
        AddMemberButton=ctk.CTkButton(mainframe,text="➕ Add Member",command=AddMember,fg_color="transparent", font=('Tahoma', 16),hover_color="grey")
        AddMemberButton.grid(row=0,column=1,padx=5,pady=4)
        DeleteMemberButton=ctk.CTkButton(mainframe,text="🗑 Delete Member",command=DeleteMember,fg_color="transparent", font=('Tahoma', 16),hover_color="grey")
        DeleteMemberButton.grid(row=0,column=2,padx=5,pady=4)
        EditMemberButton=ctk.CTkButton(mainframe,text="✏️ Edit Member",command=EditMember,fg_color="transparent", font=('Tahoma', 16),hover_color="grey")
        EditMemberButton.grid(row=0,column=3,padx=5,pady=4)
        l2=ctk.CTkLabel(master=mainframe, text="Sort By:", font=('Tahoma', 16), text_color="white")
        l2.grid(row=0,column=4,padx=15,pady=4)
        sortbymember_var=ctk.StringVar(value="Member_ID")
        SortByMemberOptionmenu=ctk.CTkOptionMenu(mainframe, values=["Member_ID", "Name", "Age", "Gender"], variable=sortbymember_var,fg_color="#0E0F0F",button_color="#0E0F0F")
        SortByMemberOptionmenu.grid(row=0,column=5,padx=5,pady=4)
        SortByMemberButton=ctk.CTkButton(mainframe,text="Sort Results",command=memtable,fg_color="transparent", font=('Tahoma', 16),hover_color="grey")
        SortByMemberButton.grid(row=0,column=6,padx=5,pady=4)
        l3=ctk.CTkLabel(master=mainframe, text="All Members 👤:", font=('Tahoma', 20), text_color="white")
        l3.grid(row=1,column=1,padx=25,pady=4)
        SearchMember = ctk.CTkEntry(mainframe, placeholder_text="Search Member", width=220,fg_color="transparent")
        SearchMember.grid(row=1,column=4,pady=4,columnspan=2)
        SearchMemberButton=ctk.CTkButton(mainframe,text="Search",command=searchmem,fg_color="transparent", font=('Tahoma', 16),hover_color="grey")
        SearchMemberButton.grid(row=1,column=6,padx=5,pady=4)
        memtable()

    #All Books Page for Admin
    def AllBooks():
        #Function to show all books table
        def booktable():
            cur.execute("Select Book_ID,Book_Name,Author,Genre,Availability from books order by {};".format(SortByBookOptionmenu.get()))
            data=cur.fetchall()
            value=[('Book ID','Book Name','Author','Genre','Availability')]
            for i in data:
                value.append(i)
            table = CTkTable(mainframe, row=len(data)+1, column=5, values=value, header_color="magenta", text_color=("white","black"), colors=["white", "white"])
            table.grid(row=2,column=1,pady=18,columnspan=6,sticky="nsew")

        #Function to search books
        def searchbook():
            key=SearchBook.get()
            cur.execute("Select Book_ID,Book_Name,Author,Genre,Availability from books where Book_ID like '%{}%' or Book_Name like '%{}%' or Author like '%{}%' order by {};".format(key,key,key,SortByBookOptionmenu.get()))
            data=cur.fetchall()
            cur.execute("select * from books;")
            data2=cur.fetchall()
            value=[('Book ID','Book Name','Author','Genre','Availability')]
            for i in data:
                value.append(i)
            table2 = CTkTable(mainframe, row=len(data2)+1, column=5, values=value, header_color="magenta", text_color=("white","black"), colors=["white", "white"])
            table2.grid(row=2,column=1,pady=18,columnspan=6,sticky="nsew")

        #Window Layout
        mainframe=ctk.CTkScrollableFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="black")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
        AddBookButton=ctk.CTkButton(mainframe,text="➕ Add Book",command=AddBook,fg_color="transparent", font=('Century Gothic', 16),hover_color="grey")
        AddBookButton.grid(row=0,column=1,padx=5,pady=4)
        DeleteBookButton=ctk.CTkButton(mainframe,text="🗑 Delete Book",command=DeleteBook,fg_color="transparent", font=('Century Gothic', 16),hover_color="grey")
        DeleteBookButton.grid(row=0,column=2,padx=5,pady=4)
        EditBookButton=ctk.CTkButton(mainframe,text="✏️ Edit Book",command=EditBook,fg_color="transparent", font=('Century Gothic', 16),hover_color="grey")
        EditBookButton.grid(row=0,column=3,padx=5,pady=4)
        l2=ctk.CTkLabel(master=mainframe, text="Sort By:", font=('Century Gothic', 16), text_color="white")
        l2.grid(row=0,column=4,padx=5,pady=4)
        sortbybook_var=ctk.StringVar(value="Book_ID")
        SortByBookOptionmenu=ctk.CTkOptionMenu(mainframe, values=["Book_ID", "Book_Name", "Author", "Genre"], variable=sortbybook_var,fg_color="#0E0F0F",button_color="#0E0F0F")
        SortByBookOptionmenu.grid(row=0,column=5,padx=5,pady=4)
        SortByBookButton=ctk.CTkButton(mainframe,text="Sort Results",command=booktable,fg_color="transparent", font=('Century Gothic', 16),hover_color="grey")
        SortByBookButton.grid(row=0,column=6,padx=5,pady=4)
        l3=ctk.CTkLabel(master=mainframe, text="All Books 📚:", font=('Century Gothic', 20), text_color="white")
        l3.grid(row=1,column=1,padx=25,pady=4)
        SearchBook = ctk.CTkEntry(mainframe, placeholder_text="Search Book", width=220,fg_color="transparent")
        SearchBook.grid(row=1,column=4,pady=4,columnspan=2)
        SearchBookButton=ctk.CTkButton(mainframe,text="Search",command=searchbook,fg_color="transparent", font=('Century Gothic', 16),hover_color="grey")
        SearchBookButton.grid(row=1,column=6,padx=5,pady=4)
        booktable()

    #Issue Book Function for admin
    def IssueBook():
        #Issue of Book
        def issueb():
            memid=IssueMemberID_Entry.get()
            bookid=IssueBookID_Entry.get()
            if memid!='' and bookid!='':
                cur.execute("select Name from members where Member_ID={};".format(memid))
                if cur.fetchone() is not None:
                    cur.execute("insert into transactions (Member_ID,Book_ID,Action) values ({},{},'Issue Book');".format(memid,bookid))
                    cur.execute("update books set Availability='FALSE' where Book_ID={};".format(bookid))
                    cur.execute("insert into issues (Member_ID,Book_ID) values ({},{});".format(memid,bookid))
                    mySQL.commit()
                    messagebox.showinfo("Success", "Book Issued Successfully.")
                    IssueBookWindow.destroy()
                    Transactions()
                else:
                    messagebox.showerror("Error", "Member ID And Name Doesn't Match.")
            else:
                messagebox.showerror("Error", "Enter All Data.") 

        #Window Layout
        IssueBookWindow=ctk.CTkToplevel()
        IssueBookWindow.title("Issue Book")
        IssueBookWindow.geometry('500x500')
        frame=ctk.CTkFrame(IssueBookWindow, width=320, height=400, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=frame, text="Issue Book", font=('Century Gothic', 20), text_color="white")
        l2.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        IssueMemberID_Entry = ctk.CTkEntry(frame, placeholder_text="Member ID", width=220)
        IssueMemberID_Entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        IssueMemberName_Entry = ctk.CTkEntry(frame, placeholder_text="Member Name", width=220)
        IssueMemberName_Entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        IssueBookID_Entry = ctk.CTkEntry(frame, placeholder_text="Book ID", width=220)
        IssueBookID_Entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        IssueBook_button=ctk.CTkButton(master=frame, command=issueb, width=20, text="Issue Book", corner_radius=10, cursor='hand2')
        IssueBook_button.place(x=100, y=350)

    #Return Book Function for admin
    def ReturnBook():
        #Return of Book
        def Returnb():
            memid=ReturnMemberID_Entry.get()
            bookid=ReturnBookID_Entry.get()
            if memid!='' and bookid!='':
                cur.execute("select Name from members where Member_ID={};".format(memid))
                if cur.fetchone() is not None:
                    cur.execute("insert into transactions (Member_ID,Book_ID,Action) values ({},{},'Return Book');".format(memid,bookid))
                    cur.execute("update books set Availability='TRUE' where Book_ID={};".format(bookid))
                    cur.execute("delete from issues where Member_ID={}".format(memid))
                    mySQL.commit()
                    messagebox.showinfo("Success", "Returned Book Successfully.")
                    ReturnBookWindow.destroy()
                    Transactions()
                else:
                    messagebox.showerror("Error", "Member ID And Name Doesn't Match.")
            else:
                messagebox.showerror("Error", "Enter All Data.") 

        #Window Layout
        ReturnBookWindow=ctk.CTkToplevel()
        ReturnBookWindow.title("Return Book")
        ReturnBookWindow.geometry('500x500')
        frame=ctk.CTkFrame(ReturnBookWindow, width=320, height=400, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=frame, text="Return Book", font=('Century Gothic', 20), text_color="white")
        l2.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        ReturnMemberID_Entry = ctk.CTkEntry(frame, placeholder_text="Member ID", width=220)
        ReturnMemberID_Entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        ReturnMemberName_Entry = ctk.CTkEntry(frame, placeholder_text="Member Name", width=220)
        ReturnMemberName_Entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        ReturnBookID_Entry = ctk.CTkEntry(frame, placeholder_text="Book ID", width=220)
        ReturnBookID_Entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        ReturnBook_button=ctk.CTkButton(master=frame, command=Returnb, width=20, text="Return Book", corner_radius=10, cursor='hand2')
        ReturnBook_button.place(x=100, y=350)

    #Funtion to add new member for admin
    def AddMember():
        #Saving member
        def SaveMember():
            MemberName=MemberName_entry.get()
            MemberUsername=MemberUsername_entry.get()
            MemberPassword=MemberPassword_entry.get()
            Age=Age_entry.get()
            Gender=Gender_optionmenu.get()
            Email=Email_entry.get()
            PhoneNumber=PhoneNumber_entry.get()
            if MemberUsername!='' and MemberPassword!='' and MemberName!='' and Age!='' and Gender!='' and Email!='' and PhoneNumber!='':
                cur.execute("Select username from users where username='{}';".format(MemberUsername))
                if cur.fetchone() is not None:
                    messagebox.showerror('Error', 'Username Already Exists.')
                else:
                    try:
                        cur.execute("Insert into members (Name,Age,Gender,Email,Phone_Number) values ('{}',{},'{}','{}',{});".format(MemberName,Age,Gender,Email,PhoneNumber))
                    except:
                        cur.execute("Insert into members (Name,Age,Gender,Email,Phone_Number) values ('{}',{},'{}','{}',{});".format(MemberName,Age,Gender,Email,PhoneNumber))
                    cur.execute("select Member_ID from members where Name='{}';".format(MemberName))
                    data=cur.fetchall()
                    memid=data[0][0]
                    cur.execute("Insert into users values ({},'{}','{}');".format(memid,MemberUsername,MemberPassword))
                    mySQL.commit()
                    messagebox.showinfo('Success', 'New Member Added Successfully.')
                    AddMemberWindow.destroy()
                    AllMembers()
            else:
                messagebox.showerror('Error', 'Enter All Data.')

        #Window Layout
        AddMemberWindow=ctk.CTkToplevel()
        AddMemberWindow.title("Add member")
        AddMemberWindow.geometry('800x600')
        frame=ctk.CTkFrame(AddMemberWindow, width=320, height=500, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=frame, text="Add Member", font=('Century Gothic', 20), text_color="white")
        l2.place(x=60, y=45)
        MemberName_entry=ctk.CTkEntry(master=frame, placeholder_text="Name", width=220)
        MemberName_entry.place(x=50, y=100)
        MemberUsername_entry=ctk.CTkEntry(master=frame, placeholder_text="Username", width=220)
        MemberUsername_entry.place(x=50, y=150)
        MemberPassword_entry=ctk.CTkEntry(master=frame, placeholder_text="Password", width=220, show="*")
        MemberPassword_entry.place(x=50, y=200)
        Age_entry=ctk.CTkEntry(master=frame, placeholder_text="Age", width=220)
        Age_entry.place(x=50, y=250)
        optionmenu_var = ctk.StringVar(value="Gender")
        Gender_optionmenu = ctk.CTkOptionMenu(frame, values=["Male", "Female"], variable=optionmenu_var)
        Gender_optionmenu.place(x=50, y=300)
        Email_entry=ctk.CTkEntry(master=frame, placeholder_text="Email", width=220)
        Email_entry.place(x=50, y=350)
        PhoneNumber_entry=ctk.CTkEntry(master=frame, placeholder_text="Phone Number", width=220)
        PhoneNumber_entry.place(x=50, y=400)
        SaveMember_button=ctk.CTkButton(master=frame, command=SaveMember, width=20, text="Save Member", corner_radius=10, cursor='hand2')
        SaveMember_button.place(x=100, y=450)
        mySQL.commit()

    #Function to delete a member for admin
    def DeleteMember():
        def Delete():
            mem=Delete_Entry.get()
            cur.execute("delete from users where Member_ID={};".format(mem))
            cur.execute("delete from members where Member_ID={};".format(mem))
            messagebox.showinfo("Success", "Deleted Member Successfully.")
            mySQL.commit()
            DeleteMemberWindow.destroy()
            AllMembers()
        DeleteMemberWindow=ctk.CTkToplevel()
        DeleteMemberWindow.title("Delete Member")
        DeleteMemberWindow.geometry('400x300')
        frame=ctk.CTkFrame(DeleteMemberWindow, width=300, height=250, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=frame, text="Delete Member", font=('Century Gothic', 20), text_color="white")
        l2.place(x=60, y=45)
        Delete_Entry = ctk.CTkEntry(frame, placeholder_text="Enter Member ID to be deleted", width=220)
        Delete_Entry.place(x=50, y=100)
        DeleteMember_button=ctk.CTkButton(master=frame, command=Delete, width=20, text="Delete Member", corner_radius=10, cursor='hand2')
        DeleteMember_button.place(x=100, y=170)

    #Edit Member function for admin
    def EditMember():
        #Member info load
        def loadinfo(self):
            #edit function
            def edit():
                MemberID=Edit_optionmenu.get()
                MemberName=MemberNameEdit_entry.get()
                MemberUsername=MemberUsernameEdit_entry.get()
                Age=AgeEdit_entry.get()
                Gender=GenderEdit_optionmenu.get()
                Email=EmailEdit_entry.get()
                PhoneNumber=PhoneNumberEdit_entry.get()
                if MemberUsername!='' and MemberName!='' and Age!='' and Gender!='' and Email!='' and PhoneNumber!='':
                    cur.execute("Select username from users where username='{}' and Member_ID!={};".format(MemberUsername,MemberID))
                    if cur.fetchone() is not None:
                        messagebox.showerror('Error', 'Username Already Exists.')
                    else:
                        cur.execute("update users set username='{}' where Member_ID={}".format(MemberUsername,MemberID))

                    cur.execute("update members set Name='{}' where Member_ID={}".format(MemberName,MemberID))

                    cur.execute("update members set Age='{}' where Member_ID={}".format(Age,MemberID))

                    cur.execute("update members set Gender='{}' where Member_ID={}".format(Gender,MemberID))

                    cur.execute("Select Email from members where Email='{}' and Member_ID!={};".format(Email,MemberID))
                    if cur.fetchone() is not None:
                        messagebox.showerror('Error', 'Email Already Exists.')
                    else:
                        cur.execute("update members set Email='{}' where Member_ID={}".format(Email,MemberID))

                    cur.execute("Select Phone_Number from members where Phone_Number='{}' and Member_ID!={};".format(PhoneNumber,MemberID))
                    if cur.fetchone() is not None:
                        messagebox.showerror('Error', 'Phone Number Already Exists.')
                    else:
                        cur.execute("update members set Phone_Number='{}' where Member_ID={}".format(PhoneNumber,MemberID))
                    
                    messagebox.showinfo("Success", "Edited Member Successfully.")
                    mySQL.commit()
                    EditMemberWindow.destroy()
                    AllMembers()
                else:
                    messagebox.showerror('Error', 'Enter All Data.')

            MemberID=Edit_optionmenu.get()
            cur.execute("Select * from members where Member_ID={};".format(MemberID))
            data=cur.fetchone()
            cur.execute("Select username from users where Member_ID={};".format(MemberID))
            data2=cur.fetchone()
            f=ctk.CTkFrame(frame, width=300, height=440, corner_radius=15, fg_color="white")
            f.place(relx=0.5, rely=0.52, anchor=tk.CENTER)

            MemberNameLabel=ctk.CTkLabel(master=f, text="Member Name:", font=('Century Gothic', 20), text_color="black")
            MemberNameLabel.place(x=40, y=10)
            membernamevar=ctk.StringVar(value=data[1])
            MemberNameEdit_entry=ctk.CTkEntry(master=f, textvariable=membernamevar, width=220)
            MemberNameEdit_entry.place(x=40, y=40)

            MemberUsernameLabel=ctk.CTkLabel(master=f, text="Username:", font=('Century Gothic', 20), text_color="black")
            MemberUsernameLabel.place(x=40, y=80)
            memberusernamevar=ctk.StringVar(value=data2[0])
            MemberUsernameEdit_entry=ctk.CTkEntry(master=f, textvariable=memberusernamevar, width=220)
            MemberUsernameEdit_entry.place(x=40, y=110)

            AgeLabel=ctk.CTkLabel(master=f, text="Age:", font=('Century Gothic', 20), text_color="black")
            AgeLabel.place(x=40, y=150)
            agevar=ctk.StringVar(value=data[2])
            AgeEdit_entry=ctk.CTkEntry(master=f, textvariable=agevar, width=220)
            AgeEdit_entry.place(x=40, y=180)

            GenderLabel=ctk.CTkLabel(master=f, text="Gender:", font=('Century Gothic', 20), text_color="black")
            GenderLabel.place(x=40, y=220)
            gendervar=ctk.StringVar(value=data[3])
            GenderEdit_optionmenu=ctk.CTkOptionMenu(master=f,values=["Male", "Female"], variable=gendervar)
            GenderEdit_optionmenu.place(x=40, y=250)

            EmailLabel=ctk.CTkLabel(master=f, text="Email:", font=('Century Gothic', 20), text_color="black")
            EmailLabel.place(x=40, y=290)
            emailvar=ctk.StringVar(value=data[4])
            EmailEdit_entry=ctk.CTkEntry(master=f, textvariable=emailvar, width=220)
            EmailEdit_entry.place(x=40, y=320)

            PhoneNumberLabel=ctk.CTkLabel(master=f, text="Phone Number:", font=('Century Gothic', 20), text_color="black")
            PhoneNumberLabel.place(x=40, y=360)
            phonevar=ctk.StringVar(value=data[5])
            PhoneNumberEdit_entry=ctk.CTkEntry(master=f, textvariable=phonevar, width=220)
            PhoneNumberEdit_entry.place(x=40, y=390)

            EditMember_button=ctk.CTkButton(master=frame, command=edit, width=20, text="Edit Member", corner_radius=10, cursor='hand2')
            EditMember_button.place(x=100, y=640)

        #Window Layout
        EditMemberWindow=ctk.CTkToplevel()
        EditMemberWindow.title("Edit Member")
        EditMemberWindow.geometry('800x700')
        frame=ctk.CTkFrame(EditMemberWindow, width=320, height=690, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=frame, text="Edit Member", font=('Century Gothic', 22), text_color="white")
        l2.place(x=50, y=45)
        optionmenu_var = ctk.StringVar(value="Enter Member ID")
        cur.execute("Select * from members;")
        data=cur.fetchall()
        value=[]
        for i in data:
            value.append(str(i[0]))
        Edit_optionmenu = ctk.CTkComboBox(frame, values=value, variable=optionmenu_var, command=loadinfo, width=220)
        Edit_optionmenu.place(x=50, y=100)
        mySQL.commit()

    #Function to edit book for admin
    def EditBook():
        #loading info about the book
        def loadinfob(self):
            #edit funtion
            def editb():
                BookID=Edit_optionmenu.get()
                BookName=BookNameEdit_entry.get()
                Author=AuthorEdit_entry.get()
                Genre=GenreEdit_optionmenu.get()
                cur.execute("update books set Book_Name='{}' where Book_ID={}".format(BookName,BookID))
                cur.execute("update books set Author='{}' where Book_ID={}".format(Author,BookID))
                cur.execute("update books set Genre='{}' where Book_ID={}".format(Genre,BookID))
                messagebox.showinfo("Success", "Edited Book Successfully.")
                mySQL.commit()
                EditBookWindow.destroy()
                AllBooks()

            BookID=Edit_optionmenu.get()
            cur.execute("Select * from books where Book_ID={};".format(BookID))
            data=cur.fetchone()
            f=ctk.CTkFrame(frame, width=300, height=300, corner_radius=15, fg_color="white")
            f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            BookNameLabel=ctk.CTkLabel(master=f, text="Book Name:", font=('Century Gothic', 20), text_color="black")
            BookNameLabel.place(x=40, y=10)
            booknamevar=ctk.StringVar(value=data[1])
            BookNameEdit_entry=ctk.CTkEntry(master=f, textvariable=booknamevar, width=220)
            BookNameEdit_entry.place(x=40, y=40)

            AuthorLabel=ctk.CTkLabel(master=f, text="Author:", font=('Century Gothic', 20), text_color="black")
            AuthorLabel.place(x=40, y=80)
            authorvar=ctk.StringVar(value=data[2])
            AuthorEdit_entry=ctk.CTkEntry(master=f, textvariable=authorvar, width=220)
            AuthorEdit_entry.place(x=40, y=110)

            GenreLabel=ctk.CTkLabel(master=f, text="Genre:", font=('Century Gothic', 20), text_color="black")
            GenreLabel.place(x=40, y=150)
            genrevar=ctk.StringVar(value=data[3])
            GenreEdit_optionmenu = ctk.CTkOptionMenu(f, values=["Fiction", "Science Fiction", "Finance", "Historical Fiction", "Mystery","Horror","Romance"], variable=genrevar)
            GenreEdit_optionmenu.place(x=40, y=180)

            DescLabel=ctk.CTkLabel(master=f, text="Description:", font=('Century Gothic', 20), text_color="black")
            DescLabel.place(x=40, y=210)
            bookdescvar=ctk.StringVar(value=data[4])
            DescEdit_entry=ctk.CTkEntry(master=f, textvariable=bookdescvar, width=220)
            DescEdit_entry.place(x=40, y=250)

            EditBook_button=ctk.CTkButton(master=frame, command=editb, width=20, text="Edit Book", corner_radius=10, cursor='hand2')
            EditBook_button.place(x=100, y=500)

        #Window Layout
        EditBookWindow=ctk.CTkToplevel()
        EditBookWindow.title("Edit Book")
        EditBookWindow.geometry('800x650')
        frame=ctk.CTkFrame(EditBookWindow, width=320, height=600, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=frame, text="Edit Book", font=('Century Gothic', 22), text_color="white")
        l2.place(x=50, y=45)
        optionmenu_var = ctk.StringVar(value="Enter Book ID")
        cur.execute("Select * from books;")
        data=cur.fetchall()
        value=[]
        for i in data:
            value.append(str(i[0]))
        Edit_optionmenu = ctk.CTkComboBox(frame, values=value, variable=optionmenu_var, command=loadinfob, width=220)
        Edit_optionmenu.place(x=50, y=100)
        mySQL.commit()

    #Funtion to add new book for admin
    def AddBook():
        #Saving book
        def SaveBook():
            BookName=BookName_entry.get()
            Author=Author_entry.get()
            Genre=Genre_optionmenu.get()
            Desc=Desc_text.get(1.0,'100.end')
            try:
                cur.execute("""insert into books (Book_Name,Author,Genre,Description) values ('{}','{}','{}',"{}");""".format(BookName,Author,Genre,Desc))
            except:
                cur.execute("""insert into books (Book_Name,Author,Genre,Description) values ('{}','{}','{}',"{}");""".format(BookName,Author,Genre,Desc))
            messagebox.showinfo("Success", "Added Book Successfully.")
            mySQL.commit()
            AddBookWindow.destroy()
            AllBooks()

        #Window Layout
        AddBookWindow=ctk.CTkToplevel()
        AddBookWindow.title("Add Book")
        AddBookWindow.geometry('800x650')
        frame=ctk.CTkFrame(AddBookWindow, width=320, height=600, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=frame, text="Add Book", font=('Century Gothic', 20), text_color="white")
        l2.place(x=60, y=45)
        BookName_entry=ctk.CTkEntry(master=frame, placeholder_text="Book Name", width=220)
        BookName_entry.place(x=50, y=100) 
        Author_entry=ctk.CTkEntry(master=frame, placeholder_text="Author", width=220)
        Author_entry.place(x=50, y=150)
        optionmenu_var = ctk.StringVar(value="Genre")
        Genre_optionmenu = ctk.CTkOptionMenu(frame, values=["Fiction", "Science Fiction", "Finance", "Historical Fiction", "Mystery","Horror","Romance","Crime","Thriller"], variable=optionmenu_var)
        Genre_optionmenu.place(x=50, y=200)
        l3=ctk.CTkLabel(master=frame, text="Description:", font=('Century Gothic', 16), text_color="white")
        l3.place(x=60, y=240)
        Desc_text=ctk.CTkTextbox(frame,width=220,height=250)
        Desc_text.place(x=50, y=270)
        SaveBook_button=ctk.CTkButton(master=frame, command=SaveBook, width=20, text="Save Book", corner_radius=10, cursor='hand2')
        SaveBook_button.place(x=100, y=540)
        mySQL.commit()

    #Function to delete book for admin
    def DeleteBook():
        #delete function
        def DeleteB():
            b=ID_entry.get()
            cur.execute("delete from books where Book_ID={};".format(b))
            messagebox.showinfo("Success", "Deleted Book Successfully.")
            DeleteBookWindow.destroy()
            AllBooks()

        #Window Layout
        DeleteBookWindow=ctk.CTkToplevel()
        DeleteBookWindow.title("Delete Book")
        DeleteBookWindow.geometry('400x300')
        frame=ctk.CTkFrame(DeleteBookWindow, width=300, height=250, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        l2=ctk.CTkLabel(master=frame, text="Delete Book", font=('Century Gothic', 20), text_color="white")
        l2.place(x=60, y=45)
        ID_entry=ctk.CTkEntry(master=frame, placeholder_text="Enter Book ID to be deleted", width=220)
        ID_entry.place(x=50, y=100)
        DeleteBook_button=ctk.CTkButton(master=frame, command=DeleteB, width=20, text="Delete Book", corner_radius=10, cursor='hand2')
        DeleteBook_button.place(x=100, y=170)
        mySQL.commit()

    #Transactions page for admin
    def Transactions():
        mainframe=ctk.CTkScrollableFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="black")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
        IssueBookButton=ctk.CTkButton(mainframe,text="📒 Issue Book",command=IssueBook,fg_color="transparent", font=('Tahoma', 16),hover_color="grey")
        IssueBookButton.grid(row=1,column=3,padx=15,pady=4)
        ReturnBookButton=ctk.CTkButton(mainframe,text="📔 Return Book",command=ReturnBook,fg_color="transparent", font=('Tahoma', 16),hover_color="grey")
        ReturnBookButton.grid(row=1,column=4,padx=15,pady=4)
        l3=ctk.CTkLabel(master=mainframe, text="All Transactions 📃:", font=('Century Gothic', 20), text_color="white")
        l3.grid(row=1,column=1,padx=25,pady=4)
        cur.execute("Select transactions.Member_ID,Name,Book_ID,Date,Time,Action from transactions,members where transactions.Member_ID=members.member_ID;")
        data=cur.fetchall()
        value=[('Member ID','Member Name','Book ID','Date','Time','Action')]
        for i in data:
            value.insert(1,i)
        table = CTkTable(mainframe, row=len(data)+1, column=6, values=value, header_color='#17DBD8', text_color=("white","black"), colors=["white", "white"])
        table.grid(row=2,column=1,pady=4,columnspan=5)

    #Status page for admin
    def Status():
        mainframe=ctk.CTkScrollableFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="black")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
        l2=ctk.CTkLabel(master=mainframe, text="Due Books 📗", font=('Century Gothic', 20), text_color="white")
        l2.grid(row=1,column=1,pady=4)
        cur.execute("select m.Member_ID,m.Name,b.Book_ID,Book_Name,Date,Time from issues i,books b,members m where b.Book_ID=i.Book_ID and i.Member_ID=m.Member_ID;")
        value=[('Member ID','Member Name','Book ID','Book Name','Date Issued','Time')]
        data=cur.fetchall()
        for i in data:
            value.append(i)
        table = CTkTable(mainframe, row=len(data)+1, column=6, values=value, header_color='#BA92F1', text_color=("white","black"), colors=["white", "white"])
        table.grid(row=2,column=1,pady=4,columnspan=5)

        l5=ctk.CTkLabel(master=mainframe, text="Due Books (Not returned after 10 days) 📕", font=('Century Gothic', 20), text_color="white")
        l5.grid(row=3,column=1,pady=4,columnspan=2)
        cur.execute("select m.Member_ID,Name,b.Book_ID,b.Book_Name,Date,(datediff(curdate(),Date)-10)*100 from members m,issues i,books b where i.Member_ID=m.Member_ID and i.Book_ID=b.Book_ID and datediff(curdate(),Date)>10;")
        value=[('Member ID','Member Name','Book ID','Book Name','Date Issued','Total Fine(In Rupees)')]
        data=cur.fetchall()
        for i in data:
            value.append(i)
        table = CTkTable(mainframe, row=len(data)+1, column=6, values=value, header_color='#FF0000', text_color=("white","black"), colors=["white", "white"])
        table.grid(row=4,column=1,pady=4,columnspan=5,sticky="NSEW")

    #Book info page for member
    def info(Self):
        infowindow=ctk.CTkToplevel()
        infowindow.title("Infomation")
        infowindow.geometry('500x600')
        frame=ctk.CTkFrame(infowindow, width=400, height=500, corner_radius=15, fg_color="black")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        head_var=ctk.StringVar(value=Self['value'])
        l2=ctk.CTkLabel(master=frame, textvariable=head_var, font=('Palatino', 30), text_color="white")
        l2.place(x=60, y=40)
        if Self['column']==0 and Self['row']!=0:
            cur.execute("select * from books where Book_ID={}".format(Self['value']))
            data=cur.fetchall()
            bn_var=ctk.StringVar(value="Book Name : "+data[0][1])
            la1=ctk.CTkLabel(master=frame, textvariable=bn_var, font=('Palatino', 20), text_color="white")
            la1.place(x=60, y=80)
            ba_var=ctk.StringVar(value="Author : "+data[0][2])
            la2=ctk.CTkLabel(master=frame, textvariable=ba_var, font=('Palatino', 20), text_color="white")
            la2.place(x=60, y=110)
            bg_var=ctk.StringVar(value="Genre : "+data[0][3])
            la3=ctk.CTkLabel(master=frame, textvariable=bg_var, font=('Palatino', 20), text_color="white")
            la3.place(x=60, y=140)
            la4=ctk.CTkLabel(master=frame, text="About Book:", font=('Palatino', 20), text_color="white")
            la4.place(x=60, y=170)
            la5=ctk.CTkTextbox(frame,wrap="word",width=280,height=280, font=('Arial', 15))
            la5.place(x=60, y=200)
            la5.insert("0.0",data[0][4])
            la5.configure(state="disabled")

        elif Self['column']==1 and Self['row']!=0:
            row=table.get_row(Self['row'])
            cur.execute("select * from books where Book_ID={}".format(row[0]))
            data=cur.fetchall()
            la4=ctk.CTkLabel(master=frame, text="About Book:", font=('Palatino', 20), text_color="white")
            la4.place(x=60, y=80)
            la5=ctk.CTkTextbox(frame,wrap="word",width=320,height=320, font=('Arial', 20))
            la5.place(x=40, y=120)
            la5.insert("0.0",data[0][4])
            la5.configure(state="disabled")

        elif Self['column']==2 and Self['row']!=0:
            cur.execute("select Book_Name from books where Author='{}'".format(Self['value']))
            data=cur.fetchall()
            s=[]
            for i in data:
                s.append(i[0])
                x="\n".join(s)
            la5=ctk.CTkTextbox(frame,wrap="word",width=320,height=320, font=('Palatino', 20))
            la5.place(x=40, y=120)
            la5.insert("0.0","All the books from the Author are: \n\n"+x)
            la5.configure(state="disabled")

        elif Self['column']==3 and Self['row']!=0:
            cur.execute("select Book_Name from books where Genre='{}'".format(Self['value']))
            data=cur.fetchall()
            s=[]
            for i in data:
                s.append(i[0])
                x="\n".join(s)
            la5=ctk.CTkTextbox(frame,wrap="word",width=320,height=320, font=('Palatino', 20))
            la5.place(x=40, y=120)
            la5.insert("0.0","All the books of this Genre are: \n\n"+x)
            la5.configure(state="disabled")

    #Available books page for member
    def AvailableBooks():
        #displaying available books table
        def booktable():
            global table
            cur.execute("select Book_ID,Book_Name,Author,Genre from books where Availability='TRUE' order by {};".format(SortByBookOptionmenu.get()))
            value=[('Book ID','Book Name','Author','Genre')]
            data=cur.fetchall()
            for i in data:
                value.append(i)
            table = CTkTable(mainframe, row=len(data)+1, column=4, values=value, width=230,header_color='magenta', text_color=("white","black"), colors=["white", "white"],command=info)
            table.grid(row=2,column=1,pady=4,columnspan=7,sticky="NSEW")
        
        #Searching a book
        def searchbook():
            key=SearchBook.get()
            cur.execute("select Book_ID,Book_Name,Author,Genre from books where Book_ID like '%{}%' or Book_Name like '%{}%' or Author like '%{}%' or Genre like '%{}%' and Availability='TRUE' order by {};".format(key,key,key,key,SortByBookOptionmenu.get()))
            value=[('Book ID','Book Name','Author','Genre')]
            data=cur.fetchall()
            cur.execute("select * from books;")
            data2=cur.fetchall()
            for i in data:
                value.append(i)
            table2 = CTkTable(mainframe, row=len(data2)+1, column=4, values=value, width=230,header_color="magenta", text_color=("white","black"), colors=["white", "white"],command=info)
            table2.grid(row=2,column=1,pady=4,columnspan=7,sticky="nsew")

        #Window layout
        mainframe=ctk.CTkScrollableFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="black")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
        l4=ctk.CTkLabel(master=mainframe, text="Available Books 📚", font=('Calibri', 25), text_color="white")
        l4.grid(row=0,column=1,pady=4,columnspan=2)
        l2=ctk.CTkLabel(master=mainframe, text="Sort By:", font=('Century Gothic', 16), text_color="white")
        l2.grid(row=1,column=4,padx=5,pady=4)
        sortbybook_var=ctk.StringVar(value="Book_ID")
        SortByBookOptionmenu=ctk.CTkOptionMenu(mainframe, values=["Book_ID", "Book_Name", "Author", "Genre"], variable=sortbybook_var,fg_color="#0E0F0F",button_color="#0E0F0F")
        SortByBookOptionmenu.grid(row=1,column=5,padx=5,pady=4)
        SortByBookButton=ctk.CTkButton(mainframe,text="Sort Results",command=booktable,fg_color="transparent", font=('Century Gothic', 16),hover_color="grey")
        SortByBookButton.grid(row=1,column=6,padx=5,pady=4)
        SearchBook = ctk.CTkEntry(mainframe, placeholder_text="Search Book", width=250,fg_color="transparent")
        SearchBook.grid(row=0,column=4,padx=6,pady=4,columnspan=2)
        SearchBookButton=ctk.CTkButton(mainframe,text="Search",command=searchbook,fg_color="transparent", font=('Century Gothic', 16),hover_color="grey")
        SearchBookButton.grid(row=0,column=6,padx=5,pady=4)
        booktable()

    #Member transactions page for member
    def YourTransactions():
        mainframe=ctk.CTkScrollableFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="black")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
        l3=ctk.CTkLabel(master=mainframe, text="All Your Transactions 📃:", font=('Century Gothic', 20), text_color="white")
        l3.grid(row=1,column=1,padx=10,pady=18)
        cur.execute("select Member_ID from users where username='{}';".format(username))
        da=cur.fetchall()
        cur.execute("Select transactions.Member_ID,Name,Book_ID,Date,Time,Action from transactions,members where transactions.Member_ID=members.Member_ID and transactions.Member_ID={};".format(da[0][0]))
        data=cur.fetchall()
        value=[('Member ID','Member Name','Book ID','Date','Time','Action')]
        for i in data:
            value.append(i)
        table = CTkTable(mainframe, row=len(data)+1, column=6, values=value, header_color='#17DBD8', text_color=("white","black"), colors=["white", "white"])
        table.grid(row=2,column=1,pady=4,columnspan=5)

    #Home page for member
    def HomeMem():
        mainframe=ctk.CTkFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="#504949")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
        cur.execute("select Name,m.member_id from members m,users u where u.member_id=m.member_id and u.username='{}';".format(username))
        data=cur.fetchall()
        m=ctk.StringVar(value="Welcome, "+data[0][0])
        MemberLabel=ctk.CTkLabel(mainframe, textvariable=m, font=('Palatino', 45), text_color="white")
        MemberLabel.pack(padx=5, pady=5, side=tk.TOP)

        def get_time():
            timeVar = time.strftime('%H:%M:%S %p \n %A \n %x')
            clock.configure(text=timeVar)
            clock.after(200,get_time)

        clock = ctk.CTkLabel(mainframe, font=("Palatino",45),bg_color="black",fg_color="#504949", text_color="white")
        clock.place(relx=0.69,rely=0.3)
        get_time()

        cur.execute("select count(*) from transactions t,users u where t.member_id=u.member_id and t.action='Issue Book' and u.username='{}';".format(username))
        data_tmem=cur.fetchall()
        tmem=ctk.StringVar(value="Total Books Borrowed till date : "+str(data_tmem[0][0]))
        MemLabel2=ctk.CTkLabel(mainframe, textvariable=tmem, font=('Palatino', 30), text_color="white")
        MemLabel2.place(relx=0.05,rely=0.2)

        cur.execute("select * from issues where Member_ID={};".format(data[0][1]))
        dat=cur.fetchall()
        if dat==[]:
            tmem=ctk.StringVar(value="Current Book : -NA-")
            MemLabel3=ctk.CTkLabel(mainframe, textvariable=tmem, font=('Palatino', 30), text_color="white")
            MemLabel3.place(relx=0.05,rely=0.4)
            tmem=ctk.StringVar(value="Book Due On : -NA-")
            MemLabel4=ctk.CTkLabel(mainframe, textvariable=tmem, font=('Palatino', 30), text_color="white")
            MemLabel4.place(relx=0.05,rely=0.6)
        else:
            cur.execute("select Book_Name from books b,issues i where b.book_id=i.book_id and i.member_id={};".format(format(data[0][1])))
            d=cur.fetchall()
            tmem=ctk.StringVar(value="Current Book : "+str(d[0][0]))
            MemLabel3=ctk.CTkLabel(mainframe, textvariable=tmem, font=('Palatino', 30), text_color="white")
            MemLabel3.place(relx=0.05,rely=0.4)
            cur.execute("select Date_add(date,interval 10 day) from issues where Member_ID={};".format(data[0][1]))
            da=cur.fetchall()
            tmem=ctk.StringVar(value="Book Due On : "+str(da[0][0]))
            MemLabel4=ctk.CTkLabel(mainframe, textvariable=tmem, font=('Palatino', 30), text_color="white")
            MemLabel4.place(relx=0.05,rely=0.6)


        current_time = datetime.datetime.now()
        c=ctk.StringVar(value="copyright © "+str(current_time.year)+" Bisista Shrestha")
        MemLabel5=ctk.CTkLabel(mainframe, textvariable=c, font=('Palatino', 20), text_color="white")
        MemLabel5.place(relx=0.4,rely=0.9)

    #Home page for admin
    def Home():
        mainframe=ctk.CTkFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="#4D4242")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")

        def get_time():
            timeVar = time.strftime('%H:%M:%S %p \n %A \n %x')
            clock.configure(text=timeVar)
            clock.after(200,get_time)

        clock = ctk.CTkLabel(mainframe, font=("Palatino",45),bg_color="black",fg_color="#4D4242", text_color="white")
        clock.place(relx=0.59,rely=0.32)
        get_time()

        AdminLabel=ctk.CTkLabel(mainframe, text="The Bisista Library", font=('Palatino', 50), text_color="white")
        AdminLabel.place(relx=0.25,rely=0.05)

        cur.execute("select count(*) from members;")
        data_tmem=cur.fetchall()
        tmem=ctk.StringVar(value="Total Members : "+str(data_tmem[0][0]))
        AdminLabel2=ctk.CTkLabel(mainframe, textvariable=tmem, font=('Palatino', 30), text_color="white")
        AdminLabel2.place(relx=0.09,rely=0.25)

        cur.execute("select count(*) from books;")
        data_tmem=cur.fetchall()
        tb=ctk.StringVar(value="Total Books : "+str(data_tmem[0][0]))
        AdminLabel3=ctk.CTkLabel(mainframe, textvariable=tb, font=('Palatino', 30), text_color="white")
        AdminLabel3.place(relx=0.09,rely=0.4)

        cur.execute("select count(*) from books where Availability='TRUE';")
        data_tmem=cur.fetchall()
        ab=ctk.StringVar(value="Available Books : "+str(data_tmem[0][0]))
        AdminLabel4=ctk.CTkLabel(mainframe, textvariable=ab, font=('Palatino', 30), text_color="white")
        AdminLabel4.place(relx=0.09,rely=0.55)

        cur.execute("select count(*) from issues;")
        data_tmem=cur.fetchall()
        db=ctk.StringVar(value="Due Books : "+str(data_tmem[0][0]))
        AdminLabel5=ctk.CTkLabel(mainframe, textvariable=db, font=('Palatino', 30), text_color="white")
        AdminLabel5.place(relx=0.09,rely=0.7)

        current_time = datetime.datetime.now()
        c=ctk.StringVar(value="copyright © "+str(current_time.year)+" Bisista Shrestha")
        AdminLabel6=ctk.CTkLabel(mainframe, textvariable=c, font=('Palatino', 20), text_color="white")
        AdminLabel6.place(relx=0.35,rely=0.9)

    #Your account page for member
    def youraccount():
        def changepw():
            def Ch():
                op=oldpw_entry.get()
                np=newpw_entry.get()
                cp=cnewpw_entry.get()
                if op!='' and np!='' and cp!='':
                    if data1[0][3]==op:
                        if np!=cp:
                            messagebox.showerror("Error", "New Password and Confirmation doesn't match.")
                        if op==np:
                            messagebox.showerror("Error", "Old and New Passwords Match.")
                        if np==cp and np!=op:
                            cur.execute("update users set password='{}' where member_id={};".format(np,data1[0][0]))
                            messagebox.showinfo("Success", "Changed Password Successfully.")
                    else:
                        messagebox.showinfo("Error", "Old Password Incorrect.")
                else:
                    messagebox.showinfo("Error", "Enter All Data.")
                ChpwWindow.destroy()
                mySQL.commit()
                youraccount()

            ChpwWindow=ctk.CTkToplevel()
            ChpwWindow.title("Change Password")
            ChpwWindow.geometry('800x600')
            frame=ctk.CTkFrame(ChpwWindow, width=320, height=500, corner_radius=15, fg_color="black")
            frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            l2=ctk.CTkLabel(master=frame, text="Change Password", font=('Century Gothic', 20), text_color="white")
            l2.place(x=60, y=45)
            oldpw_entry=ctk.CTkEntry(master=frame, placeholder_text="Enter Old Pasword", width=220)
            oldpw_entry.place(x=50, y=100)
            newpw_entry=ctk.CTkEntry(master=frame, placeholder_text="Enter New Pasword", width=220)
            newpw_entry.place(x=50, y=150)
            cnewpw_entry=ctk.CTkEntry(master=frame, placeholder_text="Confirm New Pasword", width=220)
            cnewpw_entry.place(x=50, y=200)
            DeleteBook_button=ctk.CTkButton(master=frame, command=Ch, width=20, text="Change Password", corner_radius=10, cursor='hand2')
            DeleteBook_button.place(x=100, y=250)

        mainframe=ctk.CTkFrame(master=home, width=1000, height=700, corner_radius=15, fg_color="#504949")
        mainframe.grid(row=0,column=1,pady=4,sticky="NSEW")
        cur.execute("select m.member_id,m.name,u.username,u.password,m.age,m.gender,m.email,m.phone_number from members m,users u where m.member_id=u.member_id and u.username='{}';".format(username))
        data1=cur.fetchall()
        acclabel=ctk.CTkLabel(mainframe, text="Your Account", font=('Palatino', 50), text_color="white")
        acclabel.place(relx=0.35,rely=0.02)
        var1=ctk.StringVar(value="Member ID : "+str(data1[0][0]))
        acclabel1=ctk.CTkLabel(mainframe, textvariable=var1, font=('Palatino', 30), text_color="white")
        acclabel1.place(relx=0.2,rely=0.2)
        var2=ctk.StringVar(value="Name : "+str(data1[0][1]))
        acclabel2=ctk.CTkLabel(mainframe, textvariable=var2, font=('Palatino', 30), text_color="white")
        acclabel2.place(relx=0.2,rely=0.3)
        var3=ctk.StringVar(value="Username : "+str(data1[0][2]))
        acclabel3=ctk.CTkLabel(mainframe, textvariable=var3, font=('Palatino', 30), text_color="white")
        acclabel3.place(relx=0.6,rely=0.2)
        var4=ctk.StringVar(value="Password : "+len(data1[0][3])*"*")
        acclabel4=ctk.CTkLabel(mainframe, textvariable=var4, font=('Palatino', 30), text_color="white")
        acclabel4.place(relx=0.6,rely=0.3)

        pwButton=ctk.CTkButton(mainframe,text="Change Password",command=changepw,height=50,fg_color="transparent", font=('Palatino', 20),hover_color="grey")
        pwButton.place(relx=0.65,rely=0.4)

        var5=ctk.StringVar(value="Age : "+str(data1[0][4]))
        acclabel5=ctk.CTkLabel(mainframe, textvariable=var5, font=('Palatino', 30), text_color="white")
        acclabel5.place(relx=0.2,rely=0.4)
        var6=ctk.StringVar(value="Gender : "+str(data1[0][5]))
        acclabel6=ctk.CTkLabel(mainframe, textvariable=var6, font=('Palatino', 30), text_color="white")
        acclabel6.place(relx=0.2,rely=0.5)
        var7=ctk.StringVar(value="Email : "+str(data1[0][6]))
        acclabel7=ctk.CTkLabel(mainframe, textvariable=var7, font=('Palatino', 30), text_color="white")
        acclabel7.place(relx=0.2,rely=0.6)
        var8=ctk.StringVar(value="Phone Number : "+str(data1[0][7]))
        acclabel8=ctk.CTkLabel(mainframe, textvariable=var8, font=('Palatino', 30), text_color="white")
        acclabel8.place(relx=0.2,rely=0.7)

    #logout function
    def logout():
        home.destroy()
        #os.execv(sys.executable, ['main.py'] + sys.argv)
        import subprocess
        subprocess.run(["python", "main.py"])

    if username=='Admin':
        Home()
        DashboardLabel=ctk.CTkLabel(dashboard_frame, text="👨🏻‍💻 Administrator", font=('Avenir', 25), text_color="white")
        DashboardLabel.grid(row=0,column=0,padx=15,pady=15)
        HomeButton=ctk.CTkButton(dashboard_frame,text="🏠 Home",command=Home,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        HomeButton.grid(row=1,column=0,sticky="NSEW")
        AllMembersButton=ctk.CTkButton(dashboard_frame,text="👤 All Members",command=AllMembers,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        AllMembersButton.grid(row=2,column=0,sticky="NSEW")
        AllBooksButton=ctk.CTkButton(dashboard_frame,text="📚 All Books",command=AllBooks,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        AllBooksButton.grid(row=3,column=0,sticky="NSEW")
        TransactionsButton=ctk.CTkButton(dashboard_frame,text="🧾 Transactions",command=Transactions,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        TransactionsButton.grid(row=4,column=0,sticky="NSEW")
        StatusButton=ctk.CTkButton(dashboard_frame,text="📊 Status",command=Status,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        StatusButton.grid(row=5,column=0,sticky="NSEW")
        LogoutButton=ctk.CTkButton(dashboard_frame,text="↪ Logout",command=logout,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        LogoutButton.grid(row=6,column=0,sticky="NSEW")

    else:
        HomeMem()
        DashboardLabel=ctk.CTkLabel(dashboard_frame, text="Dashboard", font=('Avenir', 25), text_color="white")
        DashboardLabel.grid(row=0,column=0,padx=15,pady=15)
        HomeButton=ctk.CTkButton(dashboard_frame,text="🏠 Home",command=HomeMem,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        HomeButton.grid(row=1,column=0,sticky="NSEW")
        AvailableBooksButton=ctk.CTkButton(dashboard_frame,text="📚 Available Books",command=AvailableBooks,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        AvailableBooksButton.grid(row=2,column=0,sticky="NSEW")
        TransactionsButton=ctk.CTkButton(dashboard_frame,text="🧾 Your Transactions",command=YourTransactions,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        TransactionsButton.grid(row=4,column=0,sticky="NSEW")
        AccountButton=ctk.CTkButton(dashboard_frame,text="🗒 Your Account",command=youraccount,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        AccountButton.grid(row=5,column=0,sticky="NSEW")
        LogoutButton=ctk.CTkButton(dashboard_frame,text="↪ Logout",command=logout,height=50,fg_color="transparent", font=('Avenir', 15),hover_color="grey")
        LogoutButton.grid(row=6,column=0,sticky="NSEW")


    home.mainloop()
    mySQL.commit()

#mysql interfacing
mySQL= mysql.connect(host='localhost',user='root',passwd='root')

cur=mySQL.cursor()

#Table Creation Codes
cur.execute("create database if not exists myproject;")
cur.execute("use myproject;")
cur.execute("""create table if not exists users(Member_ID int(4) not null references Member_ID(members), 
            username varchar(25) not null unique, 
            password varchar(25) not null);""")
cur.execute("""create table if not exists members (Member_ID int(4) DEFAULT (rand() * (9999 - 1000) + 1000) primary key,
            Name varchar(25) not null,
            Age int not null,
            Gender varchar(6) not null check (Gender in ('MALE','FEMALE')),
            Email varchar(25) not null unique,
            Phone_Number int not null unique check (Phone_Number like '__________'));""")
cur.execute("""create table if not exists books (Book_ID int(5) DEFAULT (rand() * (9999 - 1000) + 1000) primary key,
            Book_Name varchar(69) not null,
            Author varchar(25) not null,
            Genre varchar(25) not null,
            Description varchar(6690) not null,
            Availability varchar(5) default 'TRUE' not null check (Availability in ('TRUE','FALSE')));""")
cur.execute("""create table if not exists transactions (Member_ID int(4) not null references Member_ID(members),
            Book_ID int not null references Book_ID(books),
            Date DATE DEFAULT (CURRENT_DATE),
            Time TIME DEFAULT (CURRENT_TIME),
            Action varchar(11) not null check (Action in ('Issue Book','Return Book')));""")
cur.execute("""create table if not exists issues (Member_ID int(4) not null references Member_ID(members) on update cascade on delete cascade,
            Book_ID int not null references Book_ID(books),
            Date DATE DEFAULT (CURRENT_DATE) references Date(transactions),
            Time TIME DEFAULT (CURRENT_TIME) references Time(transactions));""")

mySQL.commit()

#Login
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

window=ctk.CTk()
window.title("Login")
window.geometry('900x600')

my_image = ctk.CTkImage(light_image=Image.open("lib.jpeg"), dark_image=Image.open("lib.jpeg"),size=(900,600))

image_label = ctk.CTkLabel(master=window, image=my_image, text="")
image_label.pack()

login()

window.mainloop()
mySQL.commit()
mySQL.close()