from customtkinter import*
from PIL import Image
from tkinter import messagebox
from customtkinter import CTkEntry, CTkButton, CTk,CTkImage,CTkLabel
import time
from time import strftime
import pymysql
from tkinter import ttk
import mysql.connector



window = CTk()
window.geometry('500x500+650+150')
window.resizable(False,False)
window.title('Login')
set_appearance_mode("dark")


def rfid_admin():
    rfid_window = CTkToplevel()
    rfid_window.geometry('1500x900+200+80')
    rfid_window.resizable(False, False)
    rfid_window.title('ADMINISTRATOR')

    def addpetinfo():
        # Nested function to add data to the database
        def add_data():
            if (parentinfoentry.get() == '' or
                    petinfoentry.get() == '' or
                    speciesentry.get() == '' or
                    breedentry.get() == '' or
                    agepetentry.get() == '' or
                    petdiagnosisentry.get() == ''):
                messagebox.showerror('Error', 'All fields are required')
            else:
                currentdate = time.strftime('%d/%m/%Y')  # Get current date
                query = '''
                INSERT INTO vetdetails (parentname, petname, species, breed, age, diagnosis1, date1) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
                try:
                    mycursor.execute(query, (
                        parentinfoentry.get(),
                        petinfoentry.get(),
                        speciesentry.get(),
                        breedentry.get(),
                        agepetentry.get(),
                        petdiagnosisentry.get(),
                        currentdate
                    ))
                    con.commit()  # Commit changes to the database
                    result = messagebox.askyesno('Confirm', 'Data added successfully, Do you want to clear the form?')
                    if result:
                        parentinfoentry.delete(0, END)
                        petinfoentry.delete(0, END)
                        speciesentry.delete(0, END)
                        breedentry.delete(0, END)
                        agepetentry.delete(0, END)
                        petdiagnosisentry.delete(0, END)
                except pymysql.Error as e:
                    messagebox.showerror('Error', f"Error occurred: {e}")

        # Create a window for entering pet/owner's info
        addpet_window = CTkToplevel()
        addpet_window.title("ADD PET/OWNER'S INFORMATION")
        addpet_window.resizable(False, False)
        addpet_window.grab_set()

        # Create labels and entry fields
        parentinfolabel = CTkLabel(addpet_window, text="PARENT'S NAME : ", font=('Arial', 15, 'bold'))
        parentinfolabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
        parentinfoentry = CTkEntry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        parentinfoentry.grid(row=0, column=1, pady=15, padx=10)

        petinfolabel = CTkLabel(addpet_window, text="PET'S NAME : ", font=('Arial', 15, 'bold'))
        petinfolabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
        petinfoentry = CTkEntry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        petinfoentry.grid(row=1, column=1, pady=15, padx=10)

        specieslabel = CTkLabel(addpet_window, text="TYPE OF SPECIES : ", font=('Arial', 15, 'bold'))
        specieslabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
        speciesentry = CTkEntry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        speciesentry.grid(row=2, column=1, pady=15, padx=10)

        breedlabel = CTkLabel(addpet_window, text="BREED TYPE : ", font=('Arial', 15, 'bold'))
        breedlabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
        breedentry = CTkEntry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        breedentry.grid(row=3, column=1, pady=15, padx=10)

        agepetlabel = CTkLabel(addpet_window, text="PET'S AGE : ", font=('Arial', 15, 'bold'))
        agepetlabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
        agepetentry = CTkEntry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        agepetentry.grid(row=4, column=1, pady=15, padx=10)

        petdiagnosislabel = CTkLabel(addpet_window, text="DIAGNOSIS : ", font=('Arial', 15, 'bold'))
        petdiagnosislabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
        petdiagnosisentry = CTkEntry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        petdiagnosisentry.grid(row=5, column=1, pady=15, padx=10)

        submitbutton = ttk.Button(addpet_window, text='Submit', command=add_data)
        submitbutton.grid(row=6, columnspan=2, pady=15, padx=10)

    # Define the function to connect to the database
    def connect_database():
        def connect():
            global mycursor, con
            try:
                con = pymysql.connect(
                    host=hostEntry.get(),
                    user=usernEntry.get(),
                    password=passwEntry.get()
                )
                mycursor = con.cursor()
                messagebox.showinfo('Success', 'Connection successful', parent=connectwindow)
            except pymysql.Error as e:
                messagebox.showerror('Error', f"Connection failed: {e}", parent=connectwindow)
                return

            # Create database and table
            try:
                query = 'CREATE DATABASE IF NOT EXISTS vetclinicmanagementsystem'
                mycursor.execute(query)
                mycursor.execute('USE vetclinicmanagementsystem')
                query = '''
                    CREATE TABLE IF NOT EXISTS vetdetails (
                        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        parentname VARCHAR(50),
                        petname VARCHAR(50),
                        species VARCHAR(50),
                        breed VARCHAR(50),
                        age VARCHAR(10),
                        diagnosis1 VARCHAR(50),
                        date1 VARCHAR(50)
                    )
                '''
                mycursor.execute(query)
            except pymysql.Error as e:
                messagebox.showerror('Error', f"Error creating database or table: {e}", parent=connectwindow)

            con.commit()

        connectwindow = CTkToplevel()
        connectwindow.geometry('470x250+730+230')
        connectwindow.title('Database Connection')
        connectwindow.grab_set()
        # for HOST ENTRY
        hostlabel = CTkLabel(connectwindow, text="HOST NAME : ", font=('Arial', 12))
        hostlabel.place(x=50, y=50)
        hostEntry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'))
        hostEntry.place(x=200, y=50)
        # for USERNAME ENTRY
        usernlabel = CTkLabel(connectwindow, text="USERNAME : ", font=('Arial', 12))
        usernlabel.place(x=50, y=100)
        usernEntry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'))
        usernEntry.place(x=200, y=100)
        # for PASSWORD ENTRY
        passwlabel = CTkLabel(connectwindow, text="PASSWORD : ", font=('Arial', 12))
        passwlabel.place(x=50, y=150)
        passwEntry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'))
        passwEntry.place(x=200, y=150)

        windowbut = ttk.Button(connectwindow, text="Submit", command=connect)
        windowbut.place(x=250, y=200)

    count = 0
    text = ''

    def clock():
        timex = strftime(' %I : %M : %S')
        date = strftime(' %B %d, %Y')
        currentimelabel.config(text=f'{date}\n Time: {timex}', font=('times new roman', 20, 'bold'))
        currentimelabel.after(1000, clock)

    currentimelabel = CTkLabel(window)
    currentimelabel.place(x=1250, y=800)
    clock()

    # SERVER BUTTON
    connectbutton = ttk.Button(window, text='Connect to Server', command=connect_database)
    connectbutton.place(x=1320, y=10)

    # SLIDER
    highFrame = CTkFrame(window, bg='red')
    highFrame.place(x=320, y=80, width=1175, height=600)
    scrollbarX = ttk.Scrollbar(highFrame, orient=HORIZONTAL)
    scrollbarY = ttk.Scrollbar(highFrame, orient=VERTICAL)

    petinfotable = ttk.Treeview(highFrame, columns=('ID', 'parentname', "petname", 'species', 'breed',
                                                    'age', 'diagnosis', 'date'), xscrollcommand=scrollbarX.set,
                                yscrollcommand=scrollbarY.set)

    scrollbarX.config(command=petinfotable.xview)
    scrollbarY.config(command=petinfotable.yview)
    scrollbarX.pack(side=BOTTOM, fill=X)
    scrollbarY.pack(side=RIGHT, fill=Y)
    petinfotable.pack(fill=BOTH, expand=1)

    petinfotable.heading('ID', text='I.D')
    petinfotable.heading('parentname', text="Parent's Name")
    petinfotable.heading('petname', text="Pet's Name")
    petinfotable.heading('species', text='Type of Species')
    petinfotable.heading('breed', text='Type of Bread')
    petinfotable.heading('age', text='AGE')
    petinfotable.heading('diagnosis', text='Diagnosis')
    petinfotable.heading('date', text='Date')

    petinfotable.config(show="headings")

    # BUTTONS
    leftFrame = CTkFrame(window)
    leftFrame.place(x=20, y=100, width=290, height=530)

    addpetinfo = ttk.Button(leftFrame, text='ADD NEW PET INFORMATION', width=30, command=addpetinfo)
    addpetinfo.grid(column=1, row=1, pady=15)

    searchpetdiag = ttk.Button(leftFrame, text='ADD PET DIAGNOSTIC', width=30)
    searchpetdiag.grid(column=1, row=2, pady=15)

    staffinfo = ttk.Button(leftFrame, text='STAFF INFORMATION', width=30)
    staffinfo.grid(column=1, row=3, pady=15)

    addstaffinfo = ttk.Button(leftFrame, text='ADD NEW STAFF INFO', width=30)
    addstaffinfo.grid(column=1, row=4, pady=15)

    viewreport = ttk.Button(leftFrame, text='VIEW REPORT', width=30)
    viewreport.grid(column=1, row=5, pady=15)

    delinfo = ttk.Button(leftFrame, text='DELETE INFORMATION', width=30)
    delinfo.grid(column=1, row=6, padx=5, pady=15)












def login():
    if userentry.get() == '' or passentry.get() == '':
        messagebox.showerror('Error','Please fill in the box')
    elif userentry.get() == 'admin' and passentry.get() == 'password':
        messagebox.showinfo('Login','Login Successfully')
        window.withdraw()


    elif userentry.get() == 'superuser' and passentry.get() == 'superpassword':
        messagebox.showinfo('Login', 'You are login as ADMINISTRATOR')
        window.withdraw()
        rfid_admin()
    else:
        messagebox.showwarning('No user Found','Enter User Correctly')



#loginFrame=CTkFrame(window,bg_color='#3C3D37')
#loginFrame.place(x=120,y=200)

image_path = ('pic1.png')
loaded_image = Image.open(image_path)
ctk_image = CTkImage(dark_image=Image.open(image_path), size=(100, 100))
image_label = CTkLabel(window, image=ctk_image, text="", width=100, height=220)
image_label.pack(pady=20)


#user
usernamepic = Image.open('id-card.png').resize((20,20))
username = CTkLabel(window,image=CTkImage(dark_image=usernamepic),compound='left',text=" USERNAME: ",font=('Arial',18))
username.place(x=90,y=200)
userentry=CTkEntry(window,font=('times new roman',15),placeholder_text= 'Enter Username',width=170)
userentry.place(x=230,y=200)

#password
passwordpic = Image.open('locked.png').resize((20,20))
password = CTkLabel(window,text=" PASSWORD: ",image=CTkImage(dark_image=passwordpic),compound='left',font=('Arial',18))
password.place(x=90,y=240)
passentry=CTkEntry(window,font=('times new roman',15),placeholder_text= 'Enter Password',width=170,show='*')
passentry.place(x=230,y=240)



loginpic = Image.open('enter.png').resize((20,20))
Submit = CTkButton(window,text='LOGIN',
                   font=("arial",15,'bold'),
                   image=CTkImage(light_image=loginpic),
                   compound='right',text_color='#FFEAC5',
                   corner_radius=5,
                   hover_color='#6A9C89' ,
                   fg_color= '#16423C',
                   border_color= '#16423C',
                   border_width=1,
                    command=login)
Submit.place(x=180,y=290)



window.mainloop()