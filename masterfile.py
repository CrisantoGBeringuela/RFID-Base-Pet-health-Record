#MODULES
import time
import tkinter as tk

from click import command
from customtkinter import*
from tkcalendar import Calendar
from time import strftime
from tkinter import*
import pymysql     #IMPORT DATABASE
from tkinter import messagebox, ttk, filedialog
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from customtkinter import CTkButton, CTkFrame, CTkImage
from PIL import Image,ImageTk #to support jpeg format
import pandas   #FOR CSV
import customtkinter as ctk
import shutil
import io



selected_binary_data = None


#------------------------------------------------------------------------------------------------------------------
#MODULE CONFIGURATION
window=CTk()
window.geometry('1510x694+80+80')
window.resizable(False,False)
window.title('ADMINISTRATOR')
set_appearance_mode("light")
#------------------------------------------------------------------------------------------------------------------
#database for calendar
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="event_calendar"
        )
        if conn.is_connected():
            print("Successfully connected to the database.")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None
#CALENDAR (FUNCTION)
def add_event():
    selected_date_str = cal.get_date()  # Get date as string "yyyy-mm-dd"
    event = event_entry.get()

    if selected_date_str and event:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO events (event_date, event_description) VALUES (%s, %s)"
            cursor.execute(query, (selected_date_str, event))
            conn.commit()
            event_entry.delete(0, tk.END)
            update_event_list(selected_date_str)
            highlight_event_date(selected_date_str)  # Highlight the date with the event
        except Error as e:
            print(f"Error: {e}")


#CALENDAR (FUNCTION)
def get_events(date):
    try:
        cursor = conn.cursor()
        query = "SELECT event_description FROM events WHERE event_date = %s"
        cursor.execute(query, (date,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return []


#CALENDAR (FUNCTION)
def highlight_event_date(date_str):
    # Convert the string "yyyy-mm-dd" to a datetime.date object
    event_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Create a calendar event using the date
    cal.calevent_create(date=event_date, text="Event", tags="event")  # Add calendar event with tag

    cal.tag_config('event', background='#A02334', foreground='white')


#CALENDAR (FUNCTION)
def highlight_existing_event_dates():
    try:
        cursor = conn.cursor()
        query = "SELECT DISTINCT event_date FROM events"
        cursor.execute(query)
        event_dates = cursor.fetchall()
        for date_tuple in event_dates:
            highlight_event_date(str(date_tuple[0]))  # Convert date to string
    except Error as e:
        print(f"Error: {e}")

#CALENDAR (FUNCTION)
def update_event_list(date):
    event_listbox.delete(0, tk.END)
    events = get_events(date)
    for event in events:
        event_listbox.insert(tk.END, event[0])

#CALENDAR (FUNCTION)
def on_date_select(event):
    selected_date = cal.get_date()  # Get selected date as string "yyyy-mm-dd"
    update_event_list(selected_date)
#------------------------------------------------------------------------------------------------------------------
#LOG OUT BUTTON (FUNCTION)
def log_out():
    result = messagebox.askyesno('Confirm', 'Do you want to Log out?')
    if result:
        window.destroy()
        import userLogin
    else:
        pass
#------------------------------------------------------------------------------------------------------------------
#EXPORT BUTTON (FUNCTION)
def export_data():
    # Ask where to save the file
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    if not url:
        return

    # Get all selected rows
    selected_items = information.selection()
    if not selected_items:
        messagebox.showwarning("No selection", "Please select rows to export.")
        return

    export_rows = []

    # For each selected row in Treeview, get the values
    for item in selected_items:
        row_data = information.item(item, 'values')
        # Fetch diagnosis separately if needed
        rfid_number = row_data[1]  # Assuming index 1 is RFID_Number
        mycursor.execute("SELECT diag_date, diagnosis FROM tb_diagdate WHERE RFID_Number = %s", (rfid_number,))
        diag_rows = mycursor.fetchall()

        if diag_rows:
            for diag in diag_rows:
                export_rows.append(row_data + diag)
        else:
            export_rows.append(row_data + ("", ""))  # No diagnosis

    # Column headers
    columns = ['I.D', 'RFID Number', 'Name', 'Address', 'Contact Number', 'Email address',
               "Pet's Name", "Pet's Age", "Pet's Gender", 'Breed', 'Species', 'Date', 'Diagnosis']

    # Use pandas to export to CSV
    table = pandas.DataFrame(export_rows, columns=columns)
    table.to_csv(url, index=False)

    messagebox.showinfo('Success', 'Selected data has been exported.')

#------------------------------------------------------------------------------------------------------------------
#UPDATE BUTTON (FUNCTION)
def update_button():
    def save_data():
        query = ('UPDATE tb_customerinfo SET Name=%s, '
                 'address=%s, cnum=%s, '
                 'emailadd=%s, petname=%s, pet_age=%s, '
                 'petgender=%s, breed=%s, species=%s WHERE ID=%s')
        mycursor.execute(query,(
                        parentinfoentry.get(),
                        addressentry.get(),
                        contactnumentry.get(),
                        emailentry.get(),
                        petnameentry.get(),
                        petageentry.get(),
                        petgenderentry.get(),
                        breedentry.get(),
                        speciesentry.get(),
                                listdata[0]
                                ))
        con.commit()
        messagebox.showinfo('Success',f'RFID No. {rfidinfoentry.get()} is edited sucessfully',parent=update_window )
        update_window.destroy()
        show_data()

    def rfid_warning(event):
        messagebox.showwarning("Warning", "You cannot edit the RFID Number!", parent=update_window)



    #TOP LEVEL FOR EDITING INFORMATION
    update_window = CTkToplevel()
    update_window.title("EDIT INFORMATION")
    update_window.geometry('1440x490+80+90')
    update_window.resizable(False, False)
    update_window.grab_set()

    editpet_BG = CTkImage(dark_image=Image.open('bg1.jpg'), size=(1440, 800))
    edit_BGLabel = CTkLabel(update_window, image=editpet_BG, text='')
    edit_BGLabel.place(x=0, y=0)

    # for ownersFrame
    edit_addpetbackground = CTkFrame(update_window, fg_color='#C7DBB8', width=530, height=340, border_width=2,
                                border_color='green')
    edit_addpetbackground.place(x=50, y=50)
    # for petFrame
    edit_addpetFrame = CTkFrame(update_window, fg_color='#C7DBB8', width=790, height=340, border_width=2,
                           border_color='green')
    edit_addpetFrame.place(x=600, y=50)


    #UPDATE ================================================ OWNERS INFORMATION ===============================================
    parentinformation = Label(edit_addpetbackground, text="Owner's Information", font=('Arial', 15, 'bold'), bg='#C7DBB8')
    parentinformation.place(x=20, y=10)


    #1 UPDATE
    rfidinfolabel = Label(edit_addpetbackground, text="RFID Number      : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    rfidinfolabel.place(x=50,y=50)
    rfidinfoentry = Entry(edit_addpetbackground, font=('Arial', 13, 'italic'), width=30)
    rfidinfoentry.place(x=190,y=50)

    rfidinfoentry.bind("<Button-1>", rfid_warning)

    #2 UPDATE
    parentinfolabel = Label(edit_addpetbackground, text="Parent's Name    : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    parentinfolabel.place(x=50, y=100)
    parentinfoentry = Entry(edit_addpetbackground, font=('Arial', 13, 'italic'), width=30)
    parentinfoentry.place(x=190, y=100)

    p_i_instruction = Label(edit_addpetbackground, text="(  Surname , Given Name , Middle Initial  )",
                            font=('arial', 9, 'italic'), bg='#C7DBB8')
    p_i_instruction.place(x=200, y=129)

    #4 UPDATE
    addresslabel = Label(edit_addpetbackground, text="Address                : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    addresslabel.place(x=50, y=200)
    addressentry = Entry(edit_addpetbackground, font=('Arial', 13, 'italic'), width=30)
    addressentry.place(x=190, y=200)

    #3 UPDATE
    contactnumlabel = Label(edit_addpetbackground, text="Contact Number : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    contactnumlabel.place(x=50, y=150)
    contactnumentry = Entry(edit_addpetbackground, font=('Arial', 13, 'italic'), width=30)
    contactnumentry.place(x=190, y=150)

    #5 UPDATE
    emaillabel = Label(edit_addpetbackground, text="E-mail Address   : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    emaillabel.place(x=50, y=250)
    emailentry = Entry(edit_addpetbackground, font=('Arial', 13, 'italic'), width=30)
    emailentry.place(x=190, y=250)

    #UPDATE ================================================ PETS INFORMATION ===============================================
    petinformation = Label(edit_addpetFrame, text="Pet's Information", font=('Arial', 15, 'bold'), bg='#C7DBB8')
    petinformation.place(x=20, y=10)
    #1 UPDATE
    petnamelabel = Label(edit_addpetFrame, text="Pet's Name          : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    petnamelabel.place(x=50, y=50)
    petnameentry = Entry(edit_addpetFrame, font=('Arial', 13, 'italic'), width=30)
    petnameentry.place(x=190, y=50)
    #2 UPDATE
    petagelabel = Label(edit_addpetFrame, text="Pet's Age              : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    petagelabel.place(x=50, y=100)
    petageentry = Entry(edit_addpetFrame, font=('Arial', 13, 'italic'), width=30)
    petageentry.place(x=190, y=100)
    #3 UPDATE
    petgenderlabel = Label(edit_addpetFrame, text="Pet's Gender       : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    petgenderlabel.place(x=50, y=150)
    petgenderentry = Entry(edit_addpetFrame, font=('Arial', 13, 'italic'), width=30)
    petgenderentry.place(x=190, y=150)
    #4 UPDATE
    breedlabel = Label(edit_addpetFrame, text="Pet's Breed          : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    breedlabel.place(x=50, y=200)
    breedentry = Entry(edit_addpetFrame, font=('Arial', 13, 'italic'), width=30)
    breedentry.place(x=190, y=200)
    #5 UPDATE
    specieslabel = Label(edit_addpetFrame, text="Pet's Species      : ", font=('Arial', 12, 'bold'), bg='#C7DBB8')
    specieslabel.place(x=50, y=250)
    speciesentry = Entry(edit_addpetFrame, font=('Arial', 12, 'italic'), width=30)
    speciesentry.place(x=190, y=250)

    submitbutton = CTkButton(update_window, text='Submit',command=save_data, width=250, height=45,
                             font=("arial", 16, 'bold'), border_width=2, border_color='#1A5319', fg_color="#387478",
                             hover_color='#729762')
    submitbutton.place(x=1092, y=410)

    indexing= information.focus()
    content=information.item(indexing)
    listdata=content['values']

    rfidinfoentry.insert(0,listdata[1])
    parentinfoentry.insert(0,listdata[2])
    addressentry.insert(0,listdata[3])
    contactnumentry.insert(0,listdata[4])
    emailentry.insert(0,listdata[5])
    petnameentry.insert(0,listdata[6])
    petageentry.insert(0,listdata[7])
    petgenderentry.insert(0, listdata[8])
    breedentry.insert(0, listdata[9])
    speciesentry.insert(0, listdata[10])

    rfidinfoentry.config(state='readonly')
#------------------------------------------------------------------------------------------------------------------
def show_pet_details():
    selected_item = information.focus()
    if selected_item:
        values = information.item(selected_item, 'values')
        if values:
            selected_rfid = values[1]  # Assuming RFID_Number is at index 1

            # Fetch image associated with this RFID
            mycursor.execute('SELECT tb_PetImage FROM tb_picture WHERE RFID_Number = %s ORDER BY tb_id DESC LIMIT 1',
                             (selected_rfid,))
            result = mycursor.fetchone()

    # If an image is found, display it
    if result:
        selected_binary_data = result[0]
        img_data = io.BytesIO(selected_binary_data)
        img = Image.open(img_data)
        img = img.resize((300, 300))  # Resize image to fit within the window
        img_tk = CTkImage(light_image=img, size=(300, 300))  # Use CTkImage for display

        # Create a new window to display pet details
        selected_item = information.focus()
        if selected_item:
            values = information.item(selected_item, 'values')

            if values:
                # Create the details window
                details_window = CTkToplevel(window)
                details_window.title("Pet/Owner Details")
                details_window.geometry('1170x650')
                details_window.resizable(False, False)
                details_window.grab_set()

                details_windowBG = CTkImage(dark_image=Image.open('bg1.jpg'), size=(1170, 650))
                details_windowBGLabel = CTkLabel(details_window, image=details_windowBG, text='')
                details_windowBGLabel.place(x=0, y=0)

                mainframe = CTkFrame(details_window, width=1070, height=600, border_color='#6A9C89', border_width=2,
                                     fg_color='#C7DBB8')
                mainframe.place(x=45, y=10)

                details_windowFrame = CTkFrame(details_window, width=900, height=700, border_color='#C7DBB8',
                                               border_width=2, fg_color='#C7DBB8')
                details_windowFrame.place(x=50, y=15)

                # Initialize the viewPetPicture frame before using it
                viewPetPicture = CTkFrame(mainframe, width=350, height=350, fg_color='white', border_width=2,
                                          border_color='green')
                viewPetPicture.place(x=700, y=10)

                # Now you can place the image inside the frame
                label = CTkLabel(viewPetPicture, image=img_tk, text='')  # Use the frame here
                label.image = img_tk  # Keep reference to avoid garbage collection
                label.place(x=0, y=0)

                labels = ['I.D', 'RFID Number', 'Name', 'Address', 'Contact Number', 'Email address',
                          "Pet's Name", "Pet's Age", "Pet's Gender", 'Breed', 'Species']

                # Display pet details in the new window
                for i, value in enumerate(values):
                    if i < len(labels):
                        title_label = CTkLabel(details_windowFrame, text=f"{labels[i]}:", font=('Arial', 20, 'bold'),
                                               text_color='#557C56', fg_color='transparent')
                        title_label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

                        value_label = CTkLabel(details_windowFrame, text=value, font=('Arial', 18, 'italic'),
                                               text_color='Black')
                        value_label.grid(row=i, column=1, sticky="w", padx=15, pady=5)

                def fetch_data():
                    query = 'SELECT * FROM tb_diagdate'
                    mycursor.execute(query)
                    fetched_data = mycursor.fetchall()
                    diagnosis_table.delete(*diagnosis_table.get_children())
                    for data in fetched_data:
                        diagnosis_table.insert('', END, values=data)

                def delete_remarks():
                    indexing = diagnosis_table.focus()
                    content = diagnosis_table.item(indexing)
                    if not content['values']:
                        messagebox.showerror('Error', 'No record selected', parent=details_window)
                        return

                    diag_id = content['values'][0]
                    confirm = messagebox.askyesno('Confirm',f'Are you sure you want to delete the record ? ',parent=details_window)
                    if not confirm:
                        return
                    try:
                        query = 'DELETE FROM tb_diagdate WHERE diag_id = %s'
                        mycursor.execute(query, (diag_id,))
                        con.commit()

                        messagebox.showinfo('DELETED', f'The record was deleted successfully', parent=details_window)
                        fetch_data()
                    except Exception as e:
                        messagebox.showerror('Error', f'An error occurred: {e}', parent=details_window)


                # Scrollable table for diagnosis history
                diagnosis_frame = CTkFrame(details_window, width=80, height=15)
                diagnosis_frame.place(x=680, y=200)

                diagnosis_table_frame = Frame(diagnosis_frame)
                diagnosis_table_frame.grid(row=1, column=0, columnspan=2)

                scroll_y = Scrollbar(diagnosis_table_frame, orient=VERTICAL)
                diagnosis_table = ttk.Treeview(diagnosis_table_frame, columns=("diag_id","diag_date", "diagnosis"), show='headings',
                                               yscrollcommand=scroll_y.set, height=10)

                scroll_y.config(command=diagnosis_table.yview)
                scroll_y.pack(side=RIGHT, fill=Y)

                diagnosis_table.heading("diag_id", text="ID")
                diagnosis_table.column("diag_id", width=0, stretch=False)
                diagnosis_table.heading("diag_date", text="Date")
                diagnosis_table.heading("diagnosis", text="Diagnosis")

                diagnosis_table.pack(fill=BOTH, expand=1)

                # Fetch diagnosis data for the selected pet (using RFID number)
                try:
                    query = "SELECT `diag_id`,`diag_date`, `diagnosis` FROM tb_diagdate WHERE RFID_Number = %s"
                    mycursor.execute(query, (values[1],))  # Use RFID Number to fetch diagnosis history
                    diagnosis_data = mycursor.fetchall()

                    for diag in diagnosis_data:
                        diagnosis_table.insert("", END, values=diag)

                except pymysql.Error as e:
                    messagebox.showerror('Error', f"Error fetching diagnosis: {e}")

                # Event binding for double-click to show full diagnosis
                def on_double_click(event):
                    selected_diag_item = diagnosis_table.focus()
                    if selected_diag_item:
                        diag_values = diagnosis_table.item(selected_diag_item, 'values')
                        if diag_values:
                            full_diagnosis_window = CTkToplevel(details_window)
                            full_diagnosis_window.title("Full Diagnosis Details")
                            full_diagnosis_window.geometry('500x300')
                            full_diagnosis_window.grab_set()

                            date_label = CTkLabel(full_diagnosis_window, text=f"Date: {diag_values[0]}",
                                                  font=('Arial', 18, 'bold'), text_color='Red')
                            date_label.pack(pady=10)

                            diagnosis_label = CTkLabel(full_diagnosis_window, text=f"Diagnosis: {diag_values[1]}",
                                                       font=('Arial', 18, 'italic'), text_color='Black', wraplength=450)
                            diagnosis_label.pack(pady=10)

                diagnosis_table.bind("<Double-1>", on_double_click)

                # Buttons for editing and deleting diagnosis
                edit_details_Button = CTkButton(details_window, text='Edit Diagnosis', width=210, height=60,
                                                font=("arial", 16, 'bold'), border_width=2, corner_radius=0,
                                                border_color='#1A5319', fg_color="#387478", hover_color='#729762')
                edit_details_Button.place(x=680, y=528)

                delete_details_Button = CTkButton(details_window, text='Delete Diagnosis',command=delete_remarks, width=210, height=60,
                                                  font=("arial", 16, 'bold'), border_width=2, corner_radius=0,
                                                  border_color='#1A5319', fg_color="#387478", hover_color='#729762')
                delete_details_Button.place(x=885, y=528)


#------------------------------------------------------------------------------------------------------------------
#CUSTOMER INFO (SHOW DATA)
def show_data():
    if mycursor:
        query = 'SELECT * FROM tb_customerinfo'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        information.delete(*information.get_children())  # Clear existing data
        for data in fetched_data:
            information.insert('', END, values=data)  # Insert each row into the treeview
#------------------------------------------------------------------------------------------------------------------
#CUSTOMER INFO (SEARCH DATA)
def search_data():
    query = 'SELECT * FROM tb_customerinfo where RFID_Number = %s'
    mycursor.execute(query,(searchentry.get(),))
    information.delete(*information.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        information.insert('',END,values=data)
#------------------------------------------------------------------------------------------------------------------
#CUSTOMER INFO (FETCHING DATA)
def fetch_data():
    query = 'SELECT * FROM tb_customerinfo'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    information.delete(*information.get_children())
    for data in fetched_data:
        information.insert('', END, values=data)
#------------------------------------------------------------------------------------------------------------------
#CUSTOMER INFO (DELETE DATA)
def delete_data():
    indexing = information.focus()
    content = information.item(indexing)
    if not content['values']:
        messagebox.showerror('Error', 'No record selected')
        return


    content_id = content['values'][1]
    confirm = messagebox.askyesno('Confirm', f'Are you sure you want to delete the record with RFID no. {content_id}?')
    if not confirm:
        return
    try:
        query = 'DELETE FROM tb_customerinfo WHERE RFID_Number = %s'
        mycursor.execute(query, (content_id,))
        con.commit()

        messagebox.showinfo('DELETED', f'The record with RFID {content_id} was deleted successfully')
        fetch_data()
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

#------------------------------------------------------------------------------------------------------------------
#ADD PET INFORMATION

def addpetinfo():

    def add_data():
        global selected_binary_data
        if (rfidinfoentry.get() == '' or
                parentinfoentry.get() == '' or
                addressentry.get() == '' or
                contactnumentry.get() == '' or
                emailentry.get() == '' or
                petnameentry.get() == '' or
                petageentry.get() == '' or
                petgenderentry.get() == 'Select an option' or
                breedentry.get() == '' or
                speciesentry.get() == ''):
            messagebox.showerror('Error', 'All fields are required', parent=addpet_window)
        else:
            currentdate = time.strftime('%d/%m/%Y')
            try:
                query = '''
                INSERT INTO tb_customerinfo ( `RFID_Number`, `Name`, `address`, `cnum`, `emailadd`,
                      `petname`, `pet_age`, `petgender`, `breed`, `species`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                try:
                    mycursor.execute(query, (
                        rfidinfoentry.get(),
                        parentinfoentry.get(),
                        addressentry.get(),
                        contactnumentry.get(),
                        emailentry.get(),
                        petnameentry.get(),
                        petageentry.get(),
                        petgenderentry.get(),
                        breedentry.get(),
                        speciesentry.get()

                    ))
                    con.commit()  # Commit changes to the database
                    result = messagebox.showinfo('Confirm', 'Data added successfully, Information added successfully', parent=addpet_window)
                    if result:
                        if selected_binary_data:
                            try:
                                mycursor.execute(
                                    "INSERT INTO tb_picture (tb_PetImage, RFID_Number) VALUES (%s, %s) ",
                                    (selected_binary_data, rfidinfoentry.get())
                                )
                                con.commit()
                            except pymysql.Error as e:
                                messagebox.showwarning('Warning', 'Image not save', parent=addpet_window)



                        addpet_window.destroy()
                    else:
                        pass
                except pymysql.IntegrityError as e:
                    messagebox.showerror('Error', 'Error inserting data: RFID Number may already exist')
                    return

                # Refresh the information treeview
                query = 'SELECT * FROM tb_customerinfo'
                mycursor.execute(query)
                fetched_data = mycursor.fetchall()
                information.delete(*information.get_children())
                for data in fetched_data:
                    information.insert('', END, values=data)

            except pymysql.Error as e:
                messagebox.showerror('Error', f"Error occurred: {e}")

    def pet_uploadImage():
        global selected_binary_data
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            with open(file_path, 'rb') as f:
                selected_binary_data = f.read()
                # mycursor.execute("INSERT INTO tb_picture (tb_PetImage) values (%s) ", (binary_data,))
                # con.commit()

                img = Image.open(file_path)
                img = img.resize((235, 238))
                img_tk = CTkImage(light_image=img, size=(234, 234))

                label = CTkLabel(petpictureFrame, image=img_tk, text="")
                label.image = img_tk
                label.place(x=3, y=3)



    #window for entering pet/owner's info
    addpet_window = CTkToplevel(window)
    addpet_window.title("ADD PET/OWNER'S INFORMATION")
    addpet_window.geometry('1440x490+80+90')
    addpet_window.resizable(False, False)
    addpet_window.grab_set()

    addpet_BG = CTkImage(dark_image=Image.open('bgsample.jpg'),size=(1440,490))
    addpet_BGLabel = CTkLabel(addpet_window,image=addpet_BG,text='')
    addpet_BGLabel.place(x=0,y=0)
    #for ownersFrame
    #addpetbackground = CTkFrame (addpet_window,fg_color='#C7DBB8',width= 530, height=340,border_width=2,border_color='green' )
    #addpetbackground.place(x=50,y=50)
    #for petFrame
    #addpetFrame = CTkFrame (addpet_window,fg_color='#C7DBB8',width= 790, height=340,border_width=2,border_color='green' )
    #addpetFrame.place(x=600,y=50)
    # ================================================ PICTURE IMPORT ===============================================
    petpictureFrame = CTkFrame (addpet_window,fg_color='white',width=240, height=240,border_color='black',border_width=2)
    petpictureFrame.place(x=1080,y=130)

    petpictureButton = CTkButton (addpet_window,text='Add Photo',command=pet_uploadImage,font=("arial",16,'bold'),width=240,border_width=1,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
    petpictureButton.place(x=1080,y=380)


#================================================ OWNERS INFORMATION ===============================================
    #parentinformation = Label (addpet_window,text="Owner's Information",font=('Arial',15,'bold'),bg='#C7DBB8')
    #parentinformation.place(x=20,y=10)

    #1
    #rfidinfolabel = Label(addpet_window, text="RFID Number      : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #rfidinfolabel.place(x=50,y=50)
    rfidinfoentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=140,border_color='black')
    rfidinfoentry.place(x=260,y=157)
    #2
    #parentinfolabel = Label(addpet_window, text="Parent's Name    : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #parentinfolabel.place(x=50,y=100)
    parentinfoentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250,border_color='black')
    parentinfoentry.place(x=260,y=208)
    # 3
    # contactnumlabel = Label(addpet_window, text="Contact Number : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    # contactnumlabel.place(x=50,y=150)
    contactnumentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    contactnumentry.place(x=260, y=260)

    #4
    #addresslabel = Label(addpet_window, text="Address                : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #addresslabel.place(x=50,y=200)
    addressentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250,border_color='black')
    addressentry.place(x=260,y=311)

    #5
    #emaillabel = Label(addpet_window, text="E-mail Address   : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #emaillabel.place(x=50,y=250)
    emailentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250,border_color='black')
    emailentry.place(x=260,y=362)
# ================================================ PETS INFORMATION ===============================================
    #petinformation = Label(addpet_window, text="Pet's Information", font=('Arial', 15, 'bold'), bg='#C7DBB8')
    #petinformation.place(x=20, y=10)
    #1
    #petnamelabel = Label(addpet_window, text="Pet's Name          : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #petnamelabel.place(x=50,y=50)
    petnameentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'),width=250,border_color='black')
    petnameentry.place(x=800,y=157)
    #2
    #petagelabel = Label(addpet_window, text="Pet's Age              : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #petagelabel.place(x=50,y=100)
    petageentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'),width=250,border_color='black')
    petageentry.place(x=800,y=208)
    #3
    #petgenderlabel = Label(addpet_window, text="Pet's Gender       : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #petgenderlabel.place(x=50,y=150)
    #petgenderentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=150,border_color='black')
    #petgenderentry.place(x=800,y=260)
    genderChoices = ['Male', 'Female']
    petgenderentry = ctk.CTkComboBox(addpet_window, values=genderChoices)
    petgenderentry.place(x=800,y=260)
    petgenderentry.set('Select an option')
    #4
    #breedlabel = Label(addpet_window, text="Pet's Breed          : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #breedlabel.place(x=50,y=200)
    breedentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250,border_color='black')
    breedentry.place(x=800,y=311)
    #5
    #specieslabel = Label(addpet_window, text="Pet's Species      : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    #specieslabel.place(x=50,y=250)
    speciesentry = CTkEntry(addpet_window, font=('Arial', 12, 'italic'), width=250,border_color='black')
    speciesentry.place(x=800,y=362)

    submitbutton = CTkButton(addpet_window, text='Submit', command=add_data,width=240,height=45,font=("arial",16,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
    submitbutton.place(x=1080,y=428)

#def calendarboard():
 #   window.destroy()
  #  import calendarWindow
#------------------------------------------------------------------------------------------------------------------
#ADD PET DIAGNOSIS
def add_petdiagnosis():
    def add_data():

        rfid = rfidinfoentry.get().strip()
        diagnosis_text = diagnosisentry.get("1.0", "end").strip()

        if rfidinfoentry.get() == '' or diagnosis_text == '':
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
            # Insert data into tb_diagdate table with current date
            query = '''
               INSERT INTO tb_diagdate (diagnosis, RFID_Number, `diag_date`) 
               VALUES (%s, %s, CURDATE())
               '''
            mycursor.execute(query, (diagnosis_text, rfid))
            con.commit()
            messagebox.showinfo('Success', 'Diagnosis added successfully', parent=addpet_window)

            addpet_window.destroy()
            show_data()

        except pymysql.Error as e:
            messagebox.showerror('Error', f"Error occurred: {e}", parent=addpet_window)

    # Window for entering pet/owner's info
    addpet_window = CTkToplevel(window)
    addpet_window.title("ADD PET/OWNER'S INFORMATION")
    addpet_window.resizable(False, False)
    addpet_window.grab_set()
    addpet_window.geometry('870x400+80+80')



    addpetBG = CTkImage(dark_image=Image.open('rfidremarks.jpg'), size=(900, 400))
    addpetBGlabel = CTkLabel(addpet_window, image=addpetBG, text='')
    addpetBGlabel.place(x=0, y=0)

    #addpetframe = CTkFrame(addpet_window, width=370, height=300, border_color='#6A9C89', border_width=4,fg_color='#C7DBB8')
    #addpetframe.place(x=50, y=62)


    # Entry fields for RFID and Diagnosis
    #rfidinfolabel = CTkLabel(addpet_window, text="RFID Number: ", font=('Arial', 15, 'bold'),fg_color='#C7DBB8')
    #rfidinfolabel.place(x=80,y=100)
    rfidinfoentry = CTkEntry(addpet_window, font=('Arial', 15, 'italic'), width=150,border_color='black')
    rfidinfoentry.place(x=548,y=89)

    #diagnosislabel = CTkLabel(addpet_window, text="Remarks: ", font=('Arial', 15, 'bold'),fg_color='#C7DBB8')
    #diagnosislabel.place(x=80,y=170)
    diagnosisentry = CTkTextbox(addpet_window, font=('Arial', 12, 'italic'), width=337,height=142,border_color='black',border_width=2)
    diagnosisentry.place(x=435,y=171)



    submitbutton = CTkButton(addpet_window,text='SUBMIT', font=("Arial", 16, 'bold'), compound='right',
                             text_color='#FFEAC5', corner_radius=10, hover_color='#83c7ac', fg_color='#16423C',
                             border_color='#16423C', border_width=1, width=200, height=40,command=add_data)
    submitbutton.place(x=600,y=345)


def inventory_section():
    InventoryLevel = CTkToplevel(window)
    InventoryLevel.geometry('1000x900+300+150')
    InventoryLevel.title("STOCK ORDERING")
    InventoryLevel.resizable(False, False)
    InventoryLevel.grab_set()

    addpet_BG = CTkImage(dark_image=Image.open('bg2.jpg'), size=(1440, 900))
    addpet_BGLabel = CTkLabel(InventoryLevel, image=addpet_BG, text='')
    addpet_BGLabel.place(x=0, y=0)

    inventoryFrame = CTkFrame(InventoryLevel,width=600,height=500, border_color='#6A9C89', border_width=4,fg_color='#C7DBB8')
    inventoryFrame.place(x=0,y=0)


#------------------------------------------------------------------------------------------------------------------
#DATABASE (FUNCTION)
def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host='localhost',
                user='root',
                password='12345',
                database='vetclinicmanagementsystemnew'
            )
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Connection successful', parent=connectwindow)
            connectwindow.destroy()

        except pymysql.Error as e:
            messagebox.showerror('Error', f"Connection failed: {e}", parent=connectwindow)


        except pymysql.Error as e:
            messagebox.showerror('Error', f"Error creating database or table: {e}", parent=connectwindow)

        addpetinfo.configure(state=NORMAL)
        viewreport.configure(state=NORMAL)
        exportbutton.configure(state=NORMAL)
        view_button.configure(state=NORMAL)
        add_petdiagnosis.configure(state=NORMAL)
        searchbutton.configure(state=NORMAL)
        deletebutton.configure(state=NORMAL)
        addstaffinfo.configure(state=NORMAL)
        view_button.configure(state=NORMAL)
        updatebutton.configure(state=NORMAL)
        addstaffinfo.configure(state=NORMAL)
        staffinfo.configure(state=NORMAL)
        inventoryrecord.configure(state=NORMAL)

    connectwindow = CTkToplevel(window)
    connectwindow.geometry('390x350+730+230')
    connectwindow.title('Database Connection')
    connectwindow.grab_set()

    databaseBGpicture= CTkImage(dark_image=Image.open('database-management.png'), size=(80, 80))
    databaseBG = CTkLabel(connectwindow, image=databaseBGpicture, text='')
    databaseBG.place(x=170, y=30)


    # Window fields for DB connection
    hostlabel = CTkLabel(connectwindow, text="HOST NAME: ", font=('Arial', 12))
    hostlabel.place(x=50, y=150)
    hostentry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'),width=200)
    hostentry.place(x=140, y=150)

    userlabel = CTkLabel(connectwindow, text="USER NAME: ", font=('Arial', 12))
    userlabel.place(x=50, y=200)
    userentry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'),width=200)
    userentry.place(x=140, y=200)

    passwlabel = CTkLabel(connectwindow, text="PASSWORD: ", font=('Arial', 12))
    passwlabel.place(x=50, y=250)
    passwentry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'), show="*",width=200)
    passwentry.place(x=140, y=250)

    submitbutton = CTkButton(connectwindow, text='Submit', command=connect)
    submitbutton.place(x=150, y=300)
#------------------------------------------------------------------------------------------------------------------
#ADD EMPLOYEE (FUNCTION)
def addnewEmployee():
    def edit_employee():
        def open_edit_form(employee_data):
            addnewEmployee()  # Open the form
            addnewEmployee.edit_id = employee_data[0]  # Set the ID for update

            # Fill in the fields (this matches the entry order)
            fullnameentry.insert(0, employee_data[1])
            ageentry.insert(0, employee_data[2])
            addressentry.insert(0, employee_data[3])
            phonenumberentry.insert(0, employee_data[4])
            dropdownGender.set(employee_data[5])
            TINentry.insert(0, employee_data[6])
            SSSentry.insert(0, employee_data[7])
            PAG_IBIGentry.insert(0, employee_data[8])
            birthdateentry.insert(0, employee_data[9])

    def Submit():
        if (fullnameentry.get() == '' or
                ageentry.get() == '' or
                addressentry.get() == '' or
                phonenumberentry.get() == '' or
                dropdownGender.get() == 'Select an option' or
                TINentry.get() == '' or
                SSSentry.get() == '' or
                PAG_IBIGentry.get() == '' or
                birthdateentry.get() == ''):
            messagebox.showerror('Error', 'Fill all blanks', parent=addnewEmployee)
            return

        try:
            if not con or not mycursor:
                messagebox.showerror('Error', 'Database connection failed!', parent=addnewEmployee)
                return

            mycursor.execute("USE db_employeeRecord;")

            # Check if we're updating or inserting
            if hasattr(addnewEmployee, 'edit_id'):  # <-- This assumes you set this attribute when editing
                query = '''
                UPDATE tb_EmployeeInfo
                SET fullName=%s, age=%s, fullAddress=%s, phoneNum=%s, gender=%s,
                    tinNum=%s, sssNum=%s, pagibigNum=%s, birthDate=%s
                WHERE id=%s
                '''
                mycursor.execute(query, (
                    fullnameentry.get(),
                    ageentry.get(),
                    addressentry.get(),
                    phonenumberentry.get(),
                    dropdownGender.get(),
                    TINentry.get(),
                    SSSentry.get(),
                    PAG_IBIGentry.get(),
                    birthdateentry.get(),
                    addnewEmployee.edit_id  # <-- this should be set when loading edit data
                ))
            else:
                query = '''
                INSERT INTO tb_EmployeeInfo (fullName, age, fullAddress, phoneNum, gender, tinNum, sssNum, pagibigNum, birthDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                mycursor.execute(query, (
                    fullnameentry.get(),
                    ageentry.get(),
                    addressentry.get(),
                    phonenumberentry.get(),
                    dropdownGender.get(),
                    TINentry.get(),
                    SSSentry.get(),
                    PAG_IBIGentry.get(),
                    birthdateentry.get()
                ))

            con.commit()
            messagebox.showinfo('Success', 'Employee record saved successfully!', parent=addnewEmployee)
            addnewEmployee.destroy()

        except Exception as e:
            messagebox.showerror('Error', f'Failed to save employee data.\n{e}', parent=addnewEmployee)

    addnewEmployee = CTkToplevel(window)
    addnewEmployee.geometry('750x750+300+150')
    addnewEmployee.title("EMPLOYEE INFORMATION")
    addnewEmployee.resizable(False, False)
    addnewEmployee.grab_set()

    employeeBG = CTkImage(dark_image=Image.open('bg2.jpg'), size=(750, 750))
    employeeBGlabel = CTkLabel(addnewEmployee, image=employeeBG, text='')
    employeeBGlabel.place(x=0, y=0)

    employeeframe = CTkFrame(addnewEmployee, width=600, height=640, border_color='#6A9C89', border_width=4, fg_color='#C7DBB8')
    employeeframe.place(x=70, y=30)

    # FULL NAME
    fullnamelabel = CTkLabel(employeeframe, text="Name : ", font=('Arial', 18, 'bold', 'italic'))
    fullnamelabel.place(x=65, y=30)
    fullnameentry = CTkEntry(employeeframe, font=('Arial', 15), width=280, corner_radius=12)
    fullnameentry.place(x=80, y=60)
    username = CTkLabel(employeeframe, text="( Surname, Full Name, M.I )", font=('Arial', 11, 'italic'))
    username.place(x=95, y=90)

    # AGE
    agelabel = CTkLabel(employeeframe, text="Age : ", font=('Arial', 18, 'bold', 'italic'))
    agelabel.place(x=380, y=30)
    ageentry = CTkEntry(employeeframe, font=('Arial', 15), width=140, corner_radius=12)
    ageentry.place(x=390, y=60)

    # ADDRESS
    addresslabel = CTkLabel(employeeframe, text="Full Address : ", font=('Arial', 18, 'bold', 'italic'))
    addresslabel.place(x=65, y=120)
    addressentry = CTkEntry(employeeframe, font=('Arial', 15), width=450, corner_radius=12)
    addressentry.place(x=80, y=150)
    addressNote = CTkLabel(employeeframe, text="(Lot/Block, Street, Subdivision, Barangay, City, Province)", font=('Arial', 11, 'italic'))
    addressNote.place(x=95, y=180)

    # PHONE NUMBER
    phonenumberlabel = CTkLabel(employeeframe, text="Phone Number : ", font=('Arial', 18, 'bold', 'italic'))
    phonenumberlabel.place(x=65, y=210)
    phonenumberentry = CTkEntry(employeeframe, font=('Arial', 15), width=250, corner_radius=12, placeholder_text="09XX-XXX-XXXX")
    phonenumberentry.place(x=80, y=240)

    # GENDER
    genderlabel = CTkLabel(employeeframe, text="Gender: ", font=('Arial', 18, 'bold', 'italic'))
    genderlabel.place(x=380, y=210)
    genderChoices = ['Male', 'Female']
    dropdownGender = ctk.CTkComboBox(employeeframe, values=genderChoices)
    dropdownGender.place(x=390, y=240)
    dropdownGender.set('Select an option')

    # TIN
    TINlabel = CTkLabel(employeeframe, text="TIN Number : ", font=('Arial', 18, 'bold', 'italic'))
    TINlabel.place(x=65, y=270)
    TINentry = CTkEntry(employeeframe, font=('Arial', 15), width=250, corner_radius=12, placeholder_text="XXX-XXX-XXX")
    TINentry.place(x=80, y=300)

    # SSS
    SSSlabel = CTkLabel(employeeframe, text="SSS Number : ", font=('Arial', 18, 'bold', 'italic'))
    SSSlabel.place(x=65, y=330)
    SSSentry = CTkEntry(employeeframe, font=('Arial', 15), width=250, corner_radius=12, placeholder_text="XX-XXXXXXX-X")
    SSSentry.place(x=80, y=360)

    # PAG-IBIG
    PAG_IBIGlabel = CTkLabel(employeeframe, text="PAG-IBIG Number : ", font=('Arial', 18, 'bold', 'italic'))
    PAG_IBIGlabel.place(x=65, y=390)
    PAG_IBIGentry = CTkEntry(employeeframe, font=('Arial', 15), width=250, corner_radius=12, placeholder_text="XXXXXXXXXXXX")
    PAG_IBIGentry.place(x=80, y=420)

    # BIRTHDATE
    birthdatelabel = CTkLabel(employeeframe, text="Birthday : ", font=('Arial', 18, 'bold', 'italic'))
    birthdatelabel.place(x=380, y=270)
    birthdateentry = CTkEntry(employeeframe, font=('Arial', 15), width=140, corner_radius=12, placeholder_text="MM/DD/YYYY")
    birthdateentry.place(x=390, y=300)


    # SUBMIT BUTTON
    SubmitButton = CTkButton(employeeframe, text='SUBMIT', font=("Arial", 20, 'bold'), compound='right',
                             text_color='#FFEAC5', corner_radius=10, hover_color='#83c7ac', fg_color='#16423C',
                             border_color='#16423C', border_width=1, width=270, height=60,command=Submit)
    SubmitButton.place(x=170, y=490)
#------------------------------------------------------------------------------------------------------------------
#VIEW EMPLOYEE (FUNCTION)
def view_employeeRecord():
    # ------------------------------------------------------------------------------------------------------------------
    #UPDATE
    def update_employee_window():
        def save_data():


            query = ('UPDATE tb_employeeinfo SET '
                     'fullName=%s, age=%s, '
                     'fullAddress=%s, phoneNum=%s, gender=%s, '
                     'tinNum=%s, sssNum=%s, pagibigNum=%s,birthDate=%s WHERE id=%s')
            mycursor.execute(query, (
                edit_fullnameentry.get(),
                edit_ageentry.get(),
                edit_addressentry.get(),
                edit_phonenumberentry.get(),
                edit_dropdownGender.get(),
                edit_TINentry.get(),
                edit_SSSentry.get(),
                edit_PAG_IBIGentry.get(),
                edit_birthdateentry.get(),
                listdata[0]
            ))
            con.commit()
            messagebox.showinfo('Success', f'Employee {edit_fullnameentry.get()} is edited successfully',
                                parent=employeeRecord)
            edit_addnewEmployee.destroy()

            fetch_employeedata()

        edit_addnewEmployee = CTkToplevel(employeeRecord)
        edit_addnewEmployee.geometry('750x750+300+150')
        edit_addnewEmployee.title("EMPLOYEE INFORMATION EDIT")
        edit_addnewEmployee.resizable(False, False)
        edit_addnewEmployee.grab_set()

        employeeBG = CTkImage(dark_image=Image.open('bg2.jpg'), size=(750, 750))
        employeeBGlabel = CTkLabel(edit_addnewEmployee, image=employeeBG, text='')
        employeeBGlabel.place(x=0, y=0)

        edit_employeeframe = CTkFrame(edit_addnewEmployee, width=600, height=640, border_color='#6A9C89', border_width=4,
                                 fg_color='#C7DBB8')
        edit_employeeframe.place(x=70, y=30)

        # FULL NAME
        edit_fullnamelabel = CTkLabel(edit_employeeframe, text="Name : ", font=('Arial', 18, 'bold', 'italic'))
        edit_fullnamelabel.place(x=65, y=30)
        edit_fullnameentry = CTkEntry(edit_employeeframe, font=('Arial', 15), width=280, corner_radius=12)
        edit_fullnameentry.place(x=80, y=60)
        edit_username = CTkLabel(edit_employeeframe, text="( Surname, Full Name, M.I )", font=('Arial', 11, 'italic'))
        edit_username.place(x=95, y=90)

        # AGE
        edit_agelabel = CTkLabel(edit_employeeframe, text="Age : ", font=('Arial', 18, 'bold', 'italic'))
        edit_agelabel.place(x=380, y=30)
        edit_ageentry = CTkEntry(edit_employeeframe, font=('Arial', 15), width=140, corner_radius=12)
        edit_ageentry.place(x=390, y=60)

        # ADDRESS
        edit_addresslabel = CTkLabel(edit_employeeframe, text="Full Address : ", font=('Arial', 18, 'bold', 'italic'))
        edit_addresslabel.place(x=65, y=120)
        edit_addressentry = CTkEntry(edit_employeeframe, font=('Arial', 15), width=450, corner_radius=12)
        edit_addressentry.place(x=80, y=150)
        edit_addressNote = CTkLabel(edit_employeeframe, text="(Lot/Block, Street, Subdivision, Barangay, City, Province)",
                               font=('Arial', 11, 'italic'))
        edit_addressNote.place(x=95, y=180)

        # PHONE NUMBER
        edit_phonenumberlabel = CTkLabel(edit_employeeframe, text="Phone Number : ", font=('Arial', 18, 'bold', 'italic'))
        edit_phonenumberlabel.place(x=65, y=210)
        edit_phonenumberentry = CTkEntry(edit_employeeframe, font=('Arial', 15), width=250, corner_radius=12,
                                    placeholder_text="09XX-XXX-XXXX")
        edit_phonenumberentry.place(x=80, y=240)

        # GENDER
        edit_genderlabel = CTkLabel(edit_employeeframe, text="Gender: ", font=('Arial', 18, 'bold', 'italic'))
        edit_genderlabel.place(x=380, y=210)
        edit_genderChoices = ['Male', 'Female']
        edit_dropdownGender = ctk.CTkComboBox(edit_employeeframe, values=edit_genderChoices)
        edit_dropdownGender.place(x=390, y=240)
        edit_dropdownGender.set('Select an option')

        # TIN
        edit_TINlabel = CTkLabel(edit_employeeframe, text="TIN Number : ", font=('Arial', 18, 'bold', 'italic'))
        edit_TINlabel.place(x=65, y=270)
        edit_TINentry = CTkEntry(edit_employeeframe, font=('Arial', 15), width=250, corner_radius=12,
                            placeholder_text="XXX-XXX-XXX")
        edit_TINentry.place(x=80, y=300)

        # SSS
        edit_SSSlabel = CTkLabel(edit_employeeframe, text="SSS Number : ", font=('Arial', 18, 'bold', 'italic'))
        edit_SSSlabel.place(x=65, y=330)
        edit_SSSentry = CTkEntry(edit_employeeframe, font=('Arial', 15), width=250, corner_radius=12,
                            placeholder_text="XX-XXXXXXX-X")
        edit_SSSentry.place(x=80, y=360)

        # PAG-IBIG
        edit_PAG_IBIGlabel = CTkLabel(edit_employeeframe, text="PAG-IBIG Number : ", font=('Arial', 18, 'bold', 'italic'))
        edit_PAG_IBIGlabel.place(x=65, y=390)
        edit_PAG_IBIGentry = CTkEntry(edit_employeeframe, font=('Arial', 15), width=250, corner_radius=12,
                                 placeholder_text="XXXXXXXXXXXX")
        edit_PAG_IBIGentry.place(x=80, y=420)

        # BIRTHDATE
        edit_birthdatelabel = CTkLabel(edit_employeeframe, text="Birthday : ", font=('Arial', 18, 'bold', 'italic'))
        edit_birthdatelabel.place(x=380, y=270)
        edit_birthdateentry = CTkEntry(edit_employeeframe, font=('Arial', 15), width=140, corner_radius=12,
                                  placeholder_text="MM/DD/YYYY")
        edit_birthdateentry.place(x=390, y=300)

        # SUBMIT BUTTON
        edit_SubmitButton = CTkButton(edit_employeeframe, text='SUBMIT', font=("Arial", 20, 'bold'), compound='right',
                                 text_color='#FFEAC5', corner_radius=10, hover_color='#83c7ac', fg_color='#16423C',
                                 border_color='#16423C', border_width=1, width=270, height=60, command=save_data)
        edit_SubmitButton.place(x=170, y=490)

        indexing = header.focus()
        content = header.item(indexing)
        listdata = content['values']

        edit_fullnameentry.insert(0, listdata[1])
        edit_ageentry.insert(0, listdata[2])
        edit_addressentry.insert(0, listdata[3])
        edit_phonenumberentry.insert(0, listdata[4])
        edit_dropdownGender.set(listdata[5])
        edit_TINentry.insert(0, listdata[6])
        edit_SSSentry.insert(0, listdata[7])
        edit_PAG_IBIGentry.insert(0, listdata[8])
        edit_birthdateentry.insert(0, listdata[9])



    def fetch_employeedata():
        query = 'SELECT * FROM tb_EmployeeInfo'
        mycursor.execute(query)
        fetched_employeedata = mycursor.fetchall()
        header.delete(*header.get_children())
        for data in fetched_employeedata:
            header.insert('', END, values=data)

    def delete_employeedata():
        indexing = header.focus()
        content = header.item(indexing)
        if not content['values']:
            messagebox.showerror('Error', 'No record selected')
            return

        content_id = content['values'][0]
        confirm = messagebox.askyesno('Confirm',
                                      f'Are you sure you want to delete the record of Employee Named. {content_id}?')
        if not confirm:
            return
        try:
            query = 'DELETE FROM tb_employeeinfo WHERE id = %s'
            mycursor.execute(query, (content_id,))
            con.commit()

            messagebox.showinfo('DELETED', 'The record was deleted successfully')
            header.delete(indexing)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

    def display_employee_photo(photo_filename):
        if photo_filename:
            img_path = os.path.join("employee_images", photo_filename)
            if os.path.exists(img_path):
                img = Image.open(img_path).resize((100, 100))
                photo = CTkImage(light_image=img, dark_image=img, size=(100, 100))




    employeeRecord = CTkToplevel(window)
    employeeRecord.geometry('1000x480+300+150')
    employeeRecord.title("EMPLOYEE RECORD")
    employeeRecord.resizable(False, False)
    employeeRecord.grab_set()

    view_employeeBG = CTkImage(dark_image=Image.open('bg2.jpg'), size=(1100, 490))
    view_employeeBGlabel = CTkLabel(employeeRecord, image=view_employeeBG, text='')
    view_employeeBGlabel.place(x=0, y=0)

    inventorytext = CTkLabel(employeeRecord, text="EMPLOYEE'S RECORD", image=staffpic,
                             compound='left',
                             font=('times new roman', 17, 'bold'), text_color='#1A5319')
    inventorytext.place(x=5, y=0)

    view_employeeframe = CTkFrame(employeeRecord, width=750, height=420, border_color='#4DA1A9', border_width=4, fg_color="#B3C8CF")
    view_employeeframe.place(x=20, y=40)


    treeviewframe = Frame(view_employeeframe)
    treeviewframe.pack(fill=BOTH, expand=1)
    treeviewframe.place(x=0, y=0, width=750, height=420)
    scrollbarX = Scrollbar(treeviewframe, orient=HORIZONTAL)
    scrollbarY = Scrollbar(treeviewframe, orient=VERTICAL)

    header = ttk.Treeview(
        treeviewframe,
        columns=('id','fullName', 'age', 'fullAddress', 'phoneNum', 'gender', 'tinNum', 'sssNum', 'pagibigNum', 'birthDate','photo_filename'),
        xscrollcommand=scrollbarX.set,
        yscrollcommand=scrollbarY.set
    )

    scrollbarX.config(command=header.xview)
    scrollbarY.config(command=header.yview)

    scrollbarX.pack(side=BOTTOM, fill=X)
    scrollbarY.pack(side=RIGHT, fill=Y)
    header.pack(fill=BOTH, expand=1)


    header.config(show='headings')

    header.heading('id', text='')

    header.heading('fullName', text='Full Name')
    header.heading('age', text='Age')
    header.heading('fullAddress', text='Full Address')
    header.heading('phoneNum', text='Phone Number')
    header.heading('gender', text='Gender')
    header.heading('tinNum', text='TIN Number')
    header.heading('sssNum', text='SSS Number')
    header.heading('pagibigNum', text="Pag-Ibig Number")
    header.heading('birthDate', text="Birthday")

    try:
        mycursor.execute("USE db_employeeRecord;")
        mycursor.execute("SELECT * FROM tb_EmployeeInfo")
        rows = mycursor.fetchall()

        for item in header.get_children():
            header.delete(item)

        for row in rows:
            header.insert('', 'end', values=row);
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch employee records.\n{e}", parent=employeeRecord)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch employee records.\n{e}", parent=employeeRecord)


    for col in header['columns']:
        header.column(col, width=150, anchor='center',stretch=False)
        header.column('id', width=0, stretch=False)

    view_button = CTkButton(employeeRecord, text="UPDATE EMPLOYEE RECORD", command=update_employee_window, width=150,
                            height=150, font=("arial", 14, 'bold'), border_width=2, border_color='#1A5319',
                            fg_color="#387478", hover_color='#729762')
    view_button.place(x=780, y=80)

    view_button = CTkButton(employeeRecord, text="DELETE EMPLOYEE RECORD",width=150,
                            height=150, font=("arial", 14, 'bold'), border_width=2, border_color='#1A5319',
                            fg_color="#387478", hover_color='#729762',command=delete_employeedata)
    view_button.place(x=780, y=250)

#------------------------------------------------------------------------------------------------------------------
#BACKGROUND (MAIN)
bgpicture = CTkImage(dark_image=Image.open('bg1.jpg'), size=(1530, 800))
bgpicturelabel = CTkLabel(window, image=bgpicture, text='')
bgpicturelabel.place(x=0, y=0)
#------------------------------------------------------------------------------------------------------------------
#CLOCK (FUNCTION)
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
#------------------------------------------------------------------------------------------------------------------
#VIEW EMPLOYEE (FUNCTION)
#MAIN WINDOW
#slider
style = ttk.Style()
style.theme_use("default")
style.configure('Treeview.Heading',background='#557C56',foreground='#F4F6FF',font=('Times new roman',14,'bold'))
style.map('Treeview.Heading',background=[('active','#6A9C89')])
style.configure("Treeview",background='#C7DBB8',  #background sa treeview#foreground='white', #text color
                rowheight=30, #nipis
                fieldbackground='#C7DBB8',
                fontstyle=('times new roman',35)
                )
style.map('Treeview',background=[('selected','green')]) #selected row

treeviewframe = Frame(window)
treeviewframe.place(x=255, y=100, width=720, height=500)
scrollbarX = Scrollbar(treeviewframe, orient=HORIZONTAL)
scrollbarY = Scrollbar(treeviewframe, orient=VERTICAL)

information = ttk.Treeview(treeviewframe, columns=('ID', 'RFID_Number', 'Name', 'Address', 'cnum', 'emailadd', "Petname",
                                                   "Pet_age", "Petgender", "Breed", "Species"),
                           xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set)
scrollbarX.config(command=information.xview)
scrollbarY.config(command=information.yview)
scrollbarX.pack(side=BOTTOM, fill=X)
scrollbarY.pack(side=RIGHT, fill=Y)
information.pack(fill=BOTH, expand=1)

information.config(show='headings')
information.heading('ID', text='I.D')
information.heading('RFID_Number', text='RFID Number')
information.heading('Name', text='Name')
information.heading('Address', text='Address')
information.heading('cnum', text='Contact Number')
information.heading('emailadd', text='Email Address')
information.heading('Petname', text="Pet's Name")
information.heading('Pet_age', text="Pet's Age")
information.heading('Petgender', text="Pet's Gender")
information.heading('Breed', text='Breed')
information.heading('Species', text='Species')

for col in information['columns']:
    information.column(col, width=150, anchor='center', stretch=False)


leftside = CTkFrame(window,width=250,height=800,fg_color='#C1D8C3')
leftside.place(x=0,y=0)
#------------------------------------------------------------------------------------------------------------------
#LEFT SIDE BUTTON
adminpic = CTkImage(light_image=Image.open('lakeview.jpg'),size = (253,120))
helloadmin=CTkLabel(window,text="",image=adminpic)
helloadmin.place(x=0,y=0)

#------------------------------------------------------------------------------------------------------------------
#PET CARE TAB
addpetpic = CTkImage(light_image=Image.open('kitten.png'),size = (35,35))

petinfotabtext=CTkLabel(window,text=" PET CARE TAB",fg_color='#C1D8C3',image=addpetpic,compound='left',font=('times new roman',17,'bold'),text_color='#1A5319')
petinfotabtext.place(x=0,y=130)
addpetinfo=CTkButton(window,text='Add New Pet Information',command=addpetinfo,state=DISABLED,width=250,height=50,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
addpetinfo.place(x=0,y=173)
add_petdiagnosis=CTkButton(window,text='Pet Diagnosis',command=add_petdiagnosis,state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
add_petdiagnosis.place(x=0,y=212)
viewreport=CTkButton(window,text='View All Data',state=DISABLED,command=show_data,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
viewreport.place(x=0,y=251)
exportbutton = CTkButton(window,text='Export Data',state=DISABLED,command=export_data,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
exportbutton.place(x=0,y=290)

#------------------------------------------------------------------------------------------------------------------
#EMPLOYEE / STAFF TAB
staffpic = CTkImage(light_image=Image.open('staff.png'),size = (35,35))

employeetext=CTkLabel(window,text=" EMPLOYEE/STAFF",fg_color='#C1D8C3',image=staffpic,compound='left',font=('times new roman',17,'bold'),text_color='#1A5319')
employeetext.place(x=0,y=344)
addstaffinfo=CTkButton(window,text='Add New Employee',state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),command=addnewEmployee,border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
addstaffinfo.place(x=0,y=383)

staffinfo=CTkButton(window,text='View Employee Record',state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762',command=view_employeeRecord)
staffinfo.place(x=0,y=425)

#------------------------------------------------------------------------------------------------------------------
# INVENTORY TAB

inventorypic = CTkImage(light_image=Image.open('inventory.png'),size = (35,35))

inventorytext=CTkLabel(window,text=" INVENTORY SECTION",fg_color='#C1D8C3',image=inventorypic,compound='left',font=('times new roman',17,'bold'),text_color='#1A5319')
inventorytext.place(x=0,y=474)

inventoryrecord=CTkButton(window,text='Inventory Records',command=inventory_section,state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
inventoryrecord.place(x=0,y=515)
#------------------------------------------------------------------------------------------------------------------

# SERVER MANAGER TAB
managementpic = CTkImage(light_image=Image.open('management.png'),size = (35,35))
servertext=CTkLabel(window,text=" SERVER CONNECTION",fg_color='#C1D8C3',image=managementpic,compound='left',font=('times new roman',17,'bold'),text_color='#1A5319')
servertext.place(x=0,y=565)

connectbutton=CTkButton(window,text='Connect',command=connect_database,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
connectbutton.place(x=0,y=608)
logoutbutton = CTkButton(window,text='Log Out',width=250,height=45,corner_radius=0,font=("arial",14,'bold'),command=log_out,border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
logoutbutton.place(x=0,y=650)
#------------------------------------------------------------------------------------------------------------------



"""calendarpic = CTkImage(light_image=Image.open('calendar.png'),size = (35,35))
calendarbutton = CTkButton(window,text='View Calendar',image=calendarpic,state=DISABLED,command=calendarboard,width=250,height=45,corner_radius=0,compound='left',font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
calendarbutton.place(x=0,y=220)"""
#------------------------------------------------------------------------------------------------------------------
searchentry = CTkEntry(window,placeholder_text='Search RFID Number',width=200)
searchentry.place(x=260,y=60)
searchbutton = CTkButton(window,text='Search',state=DISABLED,command=search_data,width=150,border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
searchbutton.place(x=465,y=60)
#------------------------------------------------------------------------------------------------------------------
updatebutton = CTkButton(window,text='Update Data',state=DISABLED,command=update_button,width=180,height=40,font=("arial",16,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
updatebutton.place(x=680,y=630)
#------------------------------------------------------------------------------------------------------------------
deletebutton = CTkButton(window,text='Delete Data',state=DISABLED,command=delete_data,width=180,height=40,font=("arial",16,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
deletebutton.place(x=490,y=630)
#------------------------------------------------------------------------------------------------------------------

view_button = CTkButton(window, text="View Pet Details", command=show_pet_details,state=DISABLED,width=180,height=40,font=("arial",16,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
view_button.place(x=300,y=630)
#------------------------------------------------------------------------------------------------------------------
#CALENDAR ADD MEETING
conn = connect_db()
if conn is None:
    print("Unable to connect to the database.")
    window.quit()

# Calendar widget
cal = Calendar(window, selectmode='day', date_pattern="yyyy-mm-dd",
               font=("Arial", 25,'italic'),
               showweeknumbers=False,
               showothermonthdays=False,
               background = '#90EE90',
               selectbackground = '#FFB6C1'
               )
cal.place(x=980,y=100)

# Highlight existing event dates on calendar load
highlight_existing_event_dates()

# Event entry
#event_label = CTkLabel(window, text="Event Description:")
#event_label.place(x=930,y=440)
event_entry =  CTkEntry(window, width=182,height=100,placeholder_text="Add Event or Meeting Here")
event_entry.place(x=980,y=470)

# Add event button
add_event_btn = CTkButton(window, text="Add Event", command=add_event,width=180,height=40,border_width=2,font=("arial",16,'bold'),border_color='#1A5319',fg_color="#387478",hover_color='#729762')
add_event_btn.place(x=980,y=580)

# Listbox to display events for selected date
event_listbox_label =  CTkLabel(window, text="Meeting Description:",bg_color='#C7DBB8',font=('bold',16))
event_listbox_label.place(x=1176,y=440)
event_listbox = tk.Listbox(window, width=30, height=8,font=('arial',15,'italic'))
event_listbox.place(x=1168,y=470)




# Bind the date selection event to update the event list
cal.bind("<<CalendarSelected>>", on_date_select)


window.mainloop()
if conn and conn.is_connected():
    conn.close()