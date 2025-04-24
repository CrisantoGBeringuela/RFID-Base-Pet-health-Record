from tkinter import Frame
from tkinter import*
from customtkinter import *
from tkinter import messagebox, ttk, filedialog
import mysql.connector
import pymysql
import pandas




window = CTk()
window.geometry('1500x500')

def show_pet_details():
    selected_item = information.focus()
    if selected_item:
        values = information.item(selected_item, 'values')

        # Clear the previous details
        for widget in details_frame.winfo_children():
            widget.destroy()

        if values:
            labels = ['I.D', 'RFID Number', 'Name', 'Address', 'Contact Number', 'Email address',
                      "Pet's Name", "Pet's Age", "Pet's Gender", 'Breed', 'Species']

            # Fetch diagnosis from tb_diagdate
            rfid_number = values[1]  # RFID number column from tb_customerinfo
            diag_query = 'SELECT diagnosis, date FROM tb_diagdate WHERE RFID_Number = %s'
            mycursor.execute(diag_query, (rfid_number,))
            diag_data = mycursor.fetchall()

            for i, value in enumerate(values):
                if i < len(labels):
                    title_label = CTkLabel(details_frame, text=f"{labels[i]}:", font=('Arial', 20, 'bold'), text_color='Red')
                    title_label.grid(row=i, column=0, sticky="w", padx=0, pady=5)
                    value_label = CTkLabel(details_frame, text=value, font=('Arial', 18, 'italic'), text_color='Black')
                    value_label.grid(row=i, column=1, sticky="w", padx=0, pady=5)

            # Add Diagnosis and Date details
            if diag_data:
                for j, (diagnosis, date) in enumerate(diag_data):
                    diag_label = CTkLabel(details_frame, text="Diagnosis:", font=('Arial', 20, 'bold'), text_color='Red')
                    diag_label.grid(row=len(labels) + j, column=0, sticky="w", padx=0, pady=5)
                    diag_value_label = CTkLabel(details_frame, text=diagnosis, font=('Arial', 18, 'italic'), text_color='Black')
                    diag_value_label.grid(row=len(labels) + j, column=1, sticky="w", padx=0, pady=5)

                    date_label = CTkLabel(details_frame, text="Date:", font=('Arial', 20, 'bold'), text_color='Red')
                    date_label.grid(row=len(labels) + j, column=2, sticky="w", padx=0, pady=5)
                    date_value_label = CTkLabel(details_frame, text=date, font=('Arial', 18, 'italic'), text_color='Black')
                    date_value_label.grid(row=len(labels) + j, column=3, sticky="w", padx=5, pady=5)



def addpetinfo():
    def add_data():
        if rfidinfoentry.get() == '' or diagnosisentry.get() == '':
            messagebox.showerror('Error', 'All fields are required', parent=addpet_window)
            return

        # Check if RFID Number exists in tb_customerinfo
        check_query = "SELECT * FROM tb_customerinfo WHERE RFID_Number = %s"
        mycursor.execute(check_query, (rfidinfoentry.get(),))
        result = mycursor.fetchone()

        if result is None:
            messagebox.showerror('Error', 'RFID Number does not exist in customer info.', parent=addpet_window)
            return

        try:
            # Insert data into tb_diagdate table with date
            query = '''
            INSERT INTO tb_diagdate (diagnosis, RFID_Number, `date`) 
            VALUES (%s, %s, CURDATE())
            '''
            mycursor.execute(query, (
                diagnosisentry.get(),  # Diagnosis
                rfidinfoentry.get(),   # RFID Number
            ))
            con.commit()  # Commit changes to the database
            messagebox.showinfo('Success', 'Diagnosis added successfully', parent=addpet_window)

            # Close the add window after successful insertion
            addpet_window.destroy()

            # Refresh the data in the treeview
            show_data()  # This will reload data, including new diagnosis

        except pymysql.Error as e:
            messagebox.showerror('Error', f"Error occurred: {e}")


    # Create a window for entering pet/owner's info
    addpet_window = CTkToplevel(window)
    addpet_window.title("ADD PET/OWNER'S DIAGNOSIS")
    addpet_window.resizable(False, False)
    addpet_window.grab_set()

    # Entry fields for RFID and Diagnosis
    rfidinfolabel = Label(addpet_window, text="RFID NUMBER : ", font=('Arial', 15, 'bold'))
    rfidinfolabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    rfidinfoentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    rfidinfoentry.grid(row=0, column=1, pady=15, padx=10)

    diagnosislabel = Label(addpet_window, text="DIAGNOSIS : ", font=('Arial', 15, 'bold'))
    diagnosislabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    diagnosisentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
    diagnosisentry.grid(row=1, column=1, pady=15, padx=10)

    submitbutton = CTkButton(addpet_window, text='Submit', command=add_data)
    submitbutton.grid(row=7, columnspan=2, pady=15, padx=10)

def show_data():
    query = 'SELECT * FROM tb_customerinfo'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    information.delete(*information.get_children())
    for data in fetched_data:
        information.insert('', END, values=data)



def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=information.get_children()
    newlist= []
    for index in indexing:
        content=information.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['I.D','Name','Address','Contact Number','Email address',"Pet's Name","Pet's Age","Pet's Gender" ,'Breed','Species'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved succesfully')





treeviewframe = Frame(window)
treeviewframe.place(x=15,y=0, width=500, height=400)
scrollbarX=Scrollbar(treeviewframe,orient=HORIZONTAL)
scrollbarY=Scrollbar(treeviewframe,orient=VERTICAL)

information = ttk.Treeview(treeviewframe,columns=('ID','RFID_Number','Name','Address','cnum','emailadd',"Petname",
                                                  "Pet_age","Petgender","Breed","Species"),
                           xscrollcommand=scrollbarX,yscrollcommand=scrollbarY)
scrollbarX.config(command=information.xview)
scrollbarY.config(command=information.yview)
scrollbarX.pack(side=BOTTOM,fill=X)
scrollbarY.pack(side=RIGHT,fill=Y)
information.pack(fill=BOTH,expand=1)


information.config(show='headings')
information.heading('ID',text='I.D')        #'I.D','Name','Contact Number','Email address',"Pet's Name","Pet's Age","Pet's Gender" ,'Breed','Species'
information.heading('RFID_Number',text='RFID Number')
information.heading('Name',text='Name')
information.heading('cnum',text='Contact Number')
information.heading('emailadd',text='Email Address')
information.heading('Petname',text="Pet's Name")
information.heading('Pet_age',text="Pet's Age")
information.heading('Petgender',text="Pet's Gender")
information.heading('Breed',text='Breed')
information.heading('Species',text='Species')

def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='12345',
                database = 'vetclinicmanagementsystemnew'

                # host=hostentry.get(),
                # user=userentry.get(),
                # password=passwentry.get()
            )
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Connection successful', parent=connectwindow)
            print("Connected to the database")
            connectwindow.destroy()

        except pymysql.Error as e:
            messagebox.showerror('Error', f"Connection failed: {e}", parent=connectwindow)
            print(f"Connection failed: {e}")
            return

        con.commit()

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


viewreport=CTkButton(window,text='VIEW ALL DATA',width=30,command=show_data)
viewreport.place(x=1200,y=400)

connectbutton=CTkButton(window,text='Connect to Server',command=connect_database)
connectbutton.place(x=800,y=400)
exportbutton = CTkButton(window,text='Export Data',command=export_data,width=30)
exportbutton.place(x=600,y=400)

addpetinfo=CTkButton(window,text='Add New Pet Information',command=addpetinfo)
addpetinfo.place(x=400,y=400)

view_button = CTkButton(window, text="View Pet Details", command=show_pet_details,width=180,height=40,font=("arial",16,'bold'))
view_button.place(x=100,y=400)

details_frame = CTkFrame(window,width=430,height=380)
details_frame.place(x=900,y= 5)



window.mainloop()
