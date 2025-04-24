#MODULES
import time
from calendar import calendar

from customtkinter import*
from time import strftime
from tkinter import*
import pymysql
from tkinter import messagebox, ttk, filedialog
import mysql.connector
from customtkinter import CTkButton, CTkFrame, CTkImage
from PIL import Image
import pandas

#MODULE CONFIGURATION
window=CTk()
window.geometry('1500x800+80+80')
window.resizable(False,False)
window.title('ADMINISTRATOR')
set_appearance_mode("light")




def log_out():
    result = messagebox.askyesno('Confirm', 'Do you want to Log out?')
    if result:
        window.destroy()
        import userLogin
    else:
        pass



def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=petinfotable.get_children()
    newlist= []
    for index in indexing:
        content=petinfotable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['ID','RFID Number','Parent Name','Pet Name','Species','Breed','Age','Diagnosis','Date'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved succesfully')

def update_button():
    def save_data():
        query = 'UPDATE vetdetails set rfid=%s,parentname=%s, petname=%s, species=%s, breed=%s, age=%s, diagnosis=%s WHERE ID=%s'
        mycursor.execute(query,(rfidinfoentry.get(),
                                parentinfoentry.get(),
                                petinfoentry.get(),
                                speciesentry.get(),
                                breedentry.get(),
                                agepetentry.get(),
                                petdiagnosisentry.get(),
                                listdata[0]
                                ))
        con.commit()
        messagebox.showinfo('Success',f'RFID No. {rfidinfoentry.get()} is edited sucessfully',parent=update_window )
        update_window.destroy()
        show_data()


    update_window = CTkToplevel()
    update_window.title("EDIT INFORMATION")
    update_window.resizable(False, False)
    update_window.grab_set()


    # entry field
    rfidinfolabel = Label(update_window, text="RFID NUMBER : ", font=('Arial', 15, 'bold'))
    rfidinfolabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    rfidinfoentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
    rfidinfoentry.grid(row=0, column=1, pady=15, padx=10)

    parentinfolabel = Label(update_window, text="PARENT'S NAME : ", font=('Arial', 15, 'bold'))
    parentinfolabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    parentinfoentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
    parentinfoentry.grid(row=1, column=1, pady=15, padx=10)

    petinfolabel = Label(update_window, text="PET'S NAME : ", font=('Arial', 15, 'bold'))
    petinfolabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    petinfoentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
    petinfoentry.grid(row=2, column=1, pady=15, padx=10)

    specieslabel = Label(update_window, text="TYPE OF SPECIES : ", font=('Arial', 15, 'bold'))
    specieslabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    speciesentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
    speciesentry.grid(row=3, column=1, pady=15, padx=10)

    breedlabel = Label(update_window, text="BREED TYPE : ", font=('Arial', 15, 'bold'))
    breedlabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    breedentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
    breedentry.grid(row=4, column=1, pady=15, padx=10)

    agepetlabel = Label(update_window, text="PET'S AGE : ", font=('Arial', 15, 'bold'))
    agepetlabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    agepetentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
    agepetentry.grid(row=5, column=1, pady=15, padx=10)

    petdiagnosislabel = Label(update_window, text="DIAGNOSIS : ", font=('Arial', 15, 'bold'))
    petdiagnosislabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    petdiagnosisentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
    petdiagnosisentry.grid(row=6, column=1, pady=15, padx=10)

    submitbutton = CTkButton(update_window, text='SAVE', command=save_data)
    submitbutton.grid(row=7, columnspan=2, pady=15, padx=10)

    indexing= petinfotable.focus()
    content=petinfotable.item(indexing)
    listdata=content['values']
    rfidinfoentry.insert(0,listdata[1])
    parentinfoentry.insert(0,listdata[2])
    petinfoentry.insert(0,listdata[3])
    speciesentry.insert(0,listdata[4])
    breedentry.insert(0,listdata[5])
    agepetentry.insert(0,listdata[6])
    petdiagnosisentry.insert(0,listdata[7])


def show_pet_details():
    selected_item = petinfotable.focus()
    if selected_item:
        values = petinfotable.item(selected_item, 'values')


        for widget in details_frame.winfo_children():
            widget.destroy()

        if values:
            labels = ['I.D',
                      "RFID Number",
                      "Parent's Name",
                      "Pet's Name",
                      'Type of Species',
                      'Type of Breed',
                      'Age',
                      'Diagnosis',
                      'Date']


            diag_date_row = None

            for i, value in enumerate(values):
                if i < len(labels):
                    if labels[i] == 'Diagnosis':
                        diag_date_row = i

                        diag_title_label = CTkLabel(details_frame, text="Diagnosis:", font=('Arial', 20, 'bold'), text_color='Red')
                        diag_title_label.grid(row=diag_date_row, column=0, sticky="w", padx=0, pady=5)
                        diag_value_label = CTkLabel(details_frame, text=value, font=('Arial', 18, 'italic'), text_color='Black')
                        diag_value_label.grid(row=diag_date_row, column=1, sticky="w", padx=0, pady=5)

                    elif labels[i] == 'Date' and diag_date_row is not None:
                        date_title_label = CTkLabel(details_frame, text="Date:", font=('Arial', 20, 'bold'), text_color='Red')
                        date_title_label.grid(row=diag_date_row, column=2, sticky="w", padx=0, pady=5)
                        date_value_label = CTkLabel(details_frame, text=value, font=('Arial', 18, 'italic'), text_color='Black')
                        date_value_label.grid(row=diag_date_row, column=3, sticky="w", padx=5, pady=5)

                    else:

                        title_label = CTkLabel(details_frame, text=f"{labels[i]}:", font=('Arial', 20, 'bold'), text_color='Red')
                        title_label.grid(row=i, column=0, sticky="w", padx=0, pady=5)

                        value_label = CTkLabel(details_frame, text=value, font=('Arial', 18, 'italic'), text_color='Black')
                        value_label.grid(row=i, column=1, sticky="w", padx=0, pady=5)

def show_data():
    query = 'SELECT * FROM vetdetails'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    petinfotable.delete(*petinfotable.get_children())
    for data in fetched_data:
        petinfotable.insert('', END, values=data)


def search_data():
    query = 'SELECT * FROM vetdetails where rfid = %s'
    mycursor.execute(query,(searchentry.get(),))
    petinfotable.delete(*petinfotable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        petinfotable.insert('',END,values=data)

def fetch_data():
    query = 'SELECT * FROM vetdetails'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    petinfotable.delete(*petinfotable.get_children())
    for data in fetched_data:
        petinfotable.insert('', END, values=data)

def delete_data():
    indexing = petinfotable.focus()
    content = petinfotable.item(indexing)
    if not content['values']:
        messagebox.showerror('Error', 'No record selected')
        return


    content_id = content['values'][1]
    confirm = messagebox.askyesno('Confirm', f'Are you sure you want to delete the record with RFID no. {content_id}?')
    if not confirm:
        return
    try:
        query = 'DELETE FROM vetdetails WHERE rfid = %s'
        mycursor.execute(query, (content_id,))
        con.commit()

        messagebox.showinfo('DELETED', f'The record with RFID {content_id} was deleted successfully')
        fetch_data()
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')



def addpetinfo():
    def add_data():
        if (parentinfoentry.get() == '' or
                petinfoentry.get() == '' or
                speciesentry.get() == '' or
                breedentry.get() == '' or
                agepetentry.get() == '' or
                petdiagnosisentry.get() == ''):
            messagebox.showerror('Error', 'All fields are required',parent=addpet_window)
        else:
            currentdate = time.strftime('%d/%m/%Y')
            try:
                query = '''
                INSERT INTO vetdetails (rfid,parentname, petname, species, breed, age, diagnosis, date) 
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
                '''
                try:
                    mycursor.execute(query, (
                        rfidinfoentry.get(),
                        parentinfoentry.get(),
                        petinfoentry.get(),
                        speciesentry.get(),
                        breedentry.get(),
                        agepetentry.get(),
                        petdiagnosisentry.get(),
                        currentdate
                    ))
                    con.commit()  # Commit changes to the database
                    result = messagebox.showinfo('Confirm', 'Data added successfully, Information added successfully',parent=addpet_window)
                    if result:
                        addpet_window.destroy()
                    else:
                        pass
                except:
                    messagebox.showerror('Error','I.D Cannot be repeated')
                    return

                query = 'select * from vetdetails'
                mycursor.execute(query)
                fetched_data = mycursor.fetchall()
                petinfotable.delete(*petinfotable.get_children())
                for data in fetched_data:
                    petinfotable.insert('',END, values=data)


            except pymysql.Error as e:
                messagebox.showerror('Error', f"Error occurred: {e}")

    #window for entering pet/owner's info
    addpet_window = CTkToplevel(window)
    addpet_window.title("ADD PET/OWNER'S INFORMATION")
    addpet_window.resizable(False, False)
    addpet_window.grab_set()



    #entry field
    rfidinfolabel = Label(addpet_window, text="RFID NUMBER : ", font=('Arial', 15, 'bold'))
    rfidinfolabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    rfidinfoentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    rfidinfoentry.grid(row=0, column=1, pady=15, padx=10)

    parentinfolabel = Label(addpet_window, text="PARENT'S NAME : ", font=('Arial', 15, 'bold'))
    parentinfolabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    parentinfoentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    parentinfoentry.grid(row=1, column=1, pady=15, padx=10)

    petinfolabel = Label(addpet_window, text="PET'S NAME : ", font=('Arial', 15, 'bold'))
    petinfolabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    petinfoentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    petinfoentry.grid(row=2, column=1, pady=15, padx=10)

    specieslabel = Label(addpet_window, text="TYPE OF SPECIES : ", font=('Arial', 15, 'bold'))
    specieslabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    speciesentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    speciesentry.grid(row=3, column=1, pady=15, padx=10)

    breedlabel = Label(addpet_window, text="BREED TYPE : ", font=('Arial', 15, 'bold'))
    breedlabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    breedentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    breedentry.grid(row=4, column=1, pady=15, padx=10)

    agepetlabel = Label(addpet_window, text="PET'S AGE : ", font=('Arial', 15, 'bold'))
    agepetlabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    agepetentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    agepetentry.grid(row=5, column=1, pady=15, padx=10)

    petdiagnosislabel = Label(addpet_window, text="DIAGNOSIS : ", font=('Arial', 15, 'bold'))
    petdiagnosislabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    petdiagnosisentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    petdiagnosisentry.grid(row=6, column=1, pady=15, padx=10)


    submitbutton = CTkButton(addpet_window, text='Submit', command=add_data)
    submitbutton.grid(row=7, columnspan=2, pady=15, padx=10)

def calendarboard():
    window.destroy()
    import calendarWindow




#function to connect to the database
def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='12345'


               #host=hostentry.get(),
                #user=userentry.get(),
                #password=passwentry.get()
            )
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Connection successful', parent=connectwindow)
            connectwindow.destroy()

        except pymysql.Error as e:
            messagebox.showerror('Error', f"Connection failed: {e}", parent=connectwindow)
            return


        try:
            query = 'CREATE DATABASE IF NOT EXISTS vetclinicmanagementsystem'
            mycursor.execute(query)
            mycursor.execute('USE vetclinicmanagementsystem')
            query = '''
                CREATE TABLE IF NOT EXISTS vetdetails (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    rfid VARCHAR(50),
                    parentname VARCHAR(50),
                    petname VARCHAR(50),
                    species VARCHAR(50),
                    breed VARCHAR(50),
                    age VARCHAR(10),
                    diagnosis VARCHAR(50),
                    date VARCHAR(50)
                )
            '''
            mycursor.execute(query)
            addpetinfo.configure(state=NORMAL)
            searchpetdiag.configure(state=NORMAL)
            staffinfo.configure(state=NORMAL)
            addstaffinfo.configure(state=NORMAL)
            viewreport.configure(state=NORMAL)
            deletebutton.configure(state=NORMAL)
            searchbutton.configure(state=NORMAL)
            updatebutton.configure(state=NORMAL)
            exportbutton.configure(state=NORMAL)


        except pymysql.Error as e:
            messagebox.showerror('Error', f"Error creating database or table: {e}", parent=connectwindow)

        con.commit()



#DATABASE WINDOW
    connectwindow = CTkToplevel()
    connectwindow.geometry('470x250+730+230')
    connectwindow.title('Database Connection')
    connectwindow.grab_set()
    #for HOST ENTRY
    hostlabel = CTkLabel (connectwindow, text ="HOST NAME : ", font=('Arial', 12))
    hostlabel.place(x=50, y=50)
    hostentry = CTkEntry (connectwindow,font=('Arial',12,'italic'))
    hostentry.place(x=200,y= 50)
    # for USERNAME ENTRY
    usernlabel = CTkLabel(connectwindow, text="USERNAME : ", font=('Arial', 12))
    usernlabel.place(x=50, y=100)
    userentry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'))
    userentry.place(x=200, y=100)
    # for PASSWORD ENTRY
    passwlabel = CTkLabel(connectwindow, text="PASSWORD : ", font=('Arial', 12))
    passwlabel.place(x=50, y=150)
    passwentry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'))
    passwentry.place(x=200, y=150)

    windowbut = CTkButton (connectwindow,text="Submit",command=connect)
    windowbut.place(x=250, y= 200)





#background picture
bgpicture = CTkImage(dark_image=Image.open('bg1.jpg'), size=(1600, 800))
bgpicturelabel = CTkLabel(window, image=bgpicture, text='')
bgpicturelabel.place(x=0, y=0)

#clock
count=0
text=''

def clock():
    timex=strftime(' %I:%M:%S')
    date=strftime('   %B %d, %Y')
    currentimelabel.configure(text=f'{date}\n Time: {timex}',font=('times new roman',25,'bold'),bg_color='#C7DBB8')
    currentimelabel.after(1000,clock)

currentimelabel=CTkLabel(window)
currentimelabel.place(x=1280,y=10)
clock()





#MAIN WINDOW
#slider
highFrame=Frame(window)
highFrame.place(x=300,y=100, width=730, height=510)
scrollbarX=Scrollbar(highFrame,orient=HORIZONTAL)
scrollbarY=Scrollbar(highFrame,orient=VERTICAL)
#Treeview
petinfotable=ttk.Treeview(highFrame,columns=('ID', 'rfid','parentname', "petname", 'species', 'breed', 'age', 'diagnosis', 'date'),
                            xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set)
scrollbarX.config(command=petinfotable.xview)
scrollbarY.config(command=petinfotable.yview)
scrollbarX.pack(side=BOTTOM,fill=X)
scrollbarY.pack(side=RIGHT,fill=Y)
petinfotable.pack(fill=BOTH,expand=1)

#header
petinfotable.heading('ID', text='I.D')
petinfotable.heading('rfid', text='RFID Number')
petinfotable.heading('parentname', text="Parent's Name")
petinfotable.heading('petname', text="Pet's Name")
petinfotable.heading('species', text='Type of Species')
petinfotable.heading('breed', text='Type of Breed')
petinfotable.heading('age', text='Age')
petinfotable.heading('diagnosis', text='Diagnosis')
petinfotable.heading('date', text='Date')

petinfotable.config(show="headings")


leftside = CTkFrame(window,width=250,height=800,fg_color='#C1D8C3')
leftside.place(x=0,y=0)

#LEFT SIDE BUTTON



adminpic = CTkImage(light_image=Image.open('man.png'),size = (75,75))
helloadmin=CTkLabel(window,text="  Hello ADMIN",image=adminpic,compound='left',fg_color='#C1D8C3',font=('Times new roman',25,'bold','italic'))
helloadmin.place(x=10,y=5)

addpetpic = CTkImage(light_image=Image.open('kitten.png'),size = (35,35))
addpetinfo=CTkButton(window,text='Add New Pet Information',image=addpetpic,compound='left',command=addpetinfo,state=DISABLED,width=250,height=50,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
addpetinfo.place(x=0,y=130)

diagpic = CTkImage(light_image=Image.open('medical-report.png'),size = (35,35))
searchpetdiag=CTkButton(window,text='Pet Diagnosis',image=diagpic,compound='left',state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
searchpetdiag.place(x=0,y=178)

staffinfo=CTkButton(window,text='STAFF INFORMATION',state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'))
staffinfo.place(x=0,y=600)

addstaffinfo=CTkButton(window,text='ADD NEW STAFF INFO',state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'))
addstaffinfo.place(x=0,y=550)

viewreport=CTkButton(window,text='VIEW ALL DATA',state=DISABLED,command=show_data,width=250,height=45,corner_radius=0,font=("arial",14,'bold'))
viewreport.place(x=0,y=450)

calendarpic = CTkImage(light_image=Image.open('calendar.png'),size = (35,35))
calendarbutton = CTkButton(window,text='View Calendar',image=calendarpic,command=calendarboard,width=250,height=45,corner_radius=0,compound='left',font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
calendarbutton.place(x=0,y=220)

searchentry = CTkEntry(window,placeholder_text='Search RFID Number')
searchentry.place(x=300,y=60)
searchbutton = CTkButton(window,text='Search',state=DISABLED,command=search_data,width=50)
searchbutton.place(x=450,y=60)

updatebutton = CTkButton(window,text='Update Data',state=DISABLED,command=update_button,width=180,height=40,font=("arial",16,'bold'))
updatebutton.place(x=680,y=630)

deletebutton = CTkButton(window,text='Delete Data',state=DISABLED,command=delete_data,width=180,height=40,font=("arial",16,'bold'))
deletebutton.place(x=490,y=630)

exportbutton = CTkButton(window,text='Export Data',state=DISABLED,command=export_data,width=250,height=45,corner_radius=0,font=("arial",14,'bold'))
exportbutton.place(x=0,y=350)

logoutbutton = CTkButton(window,text='Log Out',width=250,height=45,corner_radius=0,font=("arial",14,'bold'),command=log_out)
logoutbutton.place(x=0,y=750)

#SERVER BUTTON
connectbutton=CTkButton(window,text='Connect to Server',command=connect_database)
connectbutton.place(x=0,y=700)

view_button = CTkButton(window, text="View Pet Details", command=show_pet_details,width=180,height=40,font=("arial",16,'bold'))
view_button.place(x=300,y=630)

#frame sa information
details_frame = CTkFrame(window,width=430,height=510)
details_frame.place(x=1050,y= 100)





window.mainloop()
