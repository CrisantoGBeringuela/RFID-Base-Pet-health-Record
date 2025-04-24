import time
import tkinter as tk
from customtkinter import*
from tkcalendar import Calendar
from time import strftime
from tkinter import*
import pymysql     #IMPORT DATABASE
from tkinter import messagebox, ttk, filedialog
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from customtkinter import CTkButton, CTkFrame, CTkImage, CTkEntry, CTk
from PIL import Image #to support jpeg format
import pandas   #FOR CSV




root = CTk()
root.geometry('1400x800+250+100')
root.resizable(False,False)
root.title('Login')
set_appearance_mode("light")

def login():
    if userentry.get() == '' or passentry.get() == '':
        messagebox.showerror('Error','Please fill in the box')
    elif userentry.get() == 'admin' and passentry.get() == 'password':
        messagebox.showinfo('Login','Login Successfully')
        root.destroy()
        open_rfid_window()

    elif userentry.get() == 'superuser' and passentry.get() == 'superpassword':
        messagebox.showinfo('Login', 'You are login as ADMINISTRATOR')
        root.destroy()
        import masterfile
    else:
        messagebox.showwarning('No user Found','Enter User Correctly')


def open_rfid_window():
    window=CTkToplevel()
    window.geometry('1500x800+80+80')
    window.resizable(False,False)
    window.title('ADMINISTRATOR')
    set_appearance_mode("light")

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

    # CALENDAR (FUNCTION)
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

    # CALENDAR (FUNCTION)
    def get_events(date):
        try:
            cursor = conn.cursor()
            query = "SELECT event_description FROM events WHERE event_date = %s"
            cursor.execute(query, (date,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []

    # CALENDAR (FUNCTION)
    def highlight_event_date(date_str):
        # Convert the string "yyyy-mm-dd" to a datetime.date object
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Create a calendar event using the date
        cal.calevent_create(date=event_date, text="Event", tags="event")  # Add calendar event with tag

        cal.tag_config('event', background='#A02334', foreground='white')

    # CALENDAR (FUNCTION)
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

    # CALENDAR (FUNCTION)
    def update_event_list(date):
        event_listbox.delete(0, tk.END)
        events = get_events(date)
        for event in events:
            event_listbox.insert(tk.END, event[0])

    # CALENDAR (FUNCTION)
    def on_date_select(event):
        selected_date = cal.get_date()  # Get selected date as string "yyyy-mm-dd"
        update_event_list(selected_date)

    # LOG OUT BUTTON (FUNCTION)
    def log_out():
        result = messagebox.askyesno('Confirm', 'Do you want to Log out?')
        if result:
            window.destroy()
            import userLogin
        else:
            pass

    # EXPORT BUTTON (FUNCTION)
    def export_data():
        # CHOOSE LOCALHOST
        url = filedialog.asksaveasfilename(defaultextension='.csv')

        # FETCHING THE DATA BY JOINING BOTH TABLES BASE SA RFID_NUMBER
        query = '''
        SELECT 
            c.ID, 
            c.RFID_Number, 
            c.Name, 
            c.Address, 
            c.cnum AS 'Contact Number', 
            c.emailadd AS 'Email address', 
            c.Petname AS "Pet's Name", 
            c.Pet_age AS "Pet's Age", 
            c.Petgender AS "Pet's Gender", 
            c.Breed, 
            c.Species, 
            d.date, 
            d.diagnosis 
        FROM 
            tb_customerinfo c 
        LEFT JOIN 
            tb_diagdate d 
        ON 
            c.RFID_Number = d.RFID_Number
        '''
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()

        # LIST COLUMN NAMES FOR CSV FILE FORMAT
        columns = ['I.D', 'RFID Number', 'Name', 'Address', 'Contact Number', 'Email address',
                   "Pet's Name", "Pet's Age", "Pet's Gender", 'Breed', 'Species', 'Date', 'Diagnosis']

        # Convert the fetched data to a pandas DataFrame
        table = pandas.DataFrame(fetched_data, columns=columns)

        # Save the data as a CSV file
        table.to_csv(url, index=False)

        # Display success message
        messagebox.showinfo('Success', 'Data is saved successfully')

    # UPDATE BUTTON (FUNCTION)
    def update_button():
        def save_data():
            query = ('UPDATE tb_customerinfo Name=%s, '
                     'address=%s, cnum=%s, '
                     'emailadd=%s, petname=%s, pet_age=%s, '
                     'petgender=%s, breed=%s, species=%s WHERE ID=%s')
            mycursor.execute(query, (
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
            messagebox.showinfo('Success', f'RFID No. {rfidinfoentry.get()} is edited sucessfully',
                                parent=update_window)
            update_window.destroy()
            show_data()

        def rfid_warning(event):
            messagebox.showwarning("Warning", "You cannot edit the RFID Number!", parent=update_window)

        # TOP LEVEL FOR EDITING INFORMATION
        update_window = CTkToplevel()
        update_window.title("EDIT INFORMATION")
        update_window.resizable(False, False)
        update_window.grab_set()

        # entry field
        rfidinfolabel = Label(update_window, text="RFID NUMBER : ", font=('Arial', 15, 'bold'))
        rfidinfolabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
        rfidinfoentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        rfidinfoentry.grid(row=0, column=1, pady=15, padx=10)

        rfidinfoentry.bind("<Button-1>", rfid_warning)

        parentinfolabel = Label(update_window, text="PARENT'S NAME : ", font=('Arial', 15, 'bold'))
        parentinfolabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
        parentinfoentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        parentinfoentry.grid(row=1, column=1, pady=15, padx=10)

        addresslabel = Label(update_window, text="Address : ", font=('Arial', 15, 'bold'))
        addresslabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
        addressentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        addressentry.grid(row=2, column=1, pady=15, padx=10)

        contactnumlabel = Label(update_window, text="Contact Number : ", font=('Arial', 15, 'bold'))
        contactnumlabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
        contactnumentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        contactnumentry.grid(row=3, column=1, pady=15, padx=10)

        emaillabel = Label(update_window, text="E-mail Address : ", font=('Arial', 15, 'bold'))
        emaillabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
        emailentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        emailentry.grid(row=4, column=1, pady=15, padx=10)

        petnamelabel = Label(update_window, text="Pet's Name : ", font=('Arial', 15, 'bold'))
        petnamelabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
        petnameentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        petnameentry.grid(row=5, column=1, pady=15, padx=10)

        petagelabel = Label(update_window, text="Pet's Age : ", font=('Arial', 15, 'bold'))
        petagelabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
        petageentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        petageentry.grid(row=6, column=1, pady=15, padx=10)

        petgenderlabel = Label(update_window, text="Pet's Gender : ", font=('Arial', 15, 'bold'))
        petgenderlabel.grid(row=7, column=0, padx=30, pady=15, sticky=W)
        petgenderentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        petgenderentry.grid(row=7, column=1, pady=15, padx=10)

        breedlabel = Label(update_window, text="Pet's Breed : ", font=('Arial', 15, 'bold'))
        breedlabel.grid(row=8, column=0, padx=30, pady=15, sticky=W)
        breedentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        breedentry.grid(row=8, column=1, pady=15, padx=10)

        specieslabel = Label(update_window, text="Pet's Species  : ", font=('Arial', 15, 'bold'))
        specieslabel.grid(row=9, column=0, padx=30, pady=15, sticky=W)
        speciesentry = Entry(update_window, font=('Arial', 15, 'italic'), width=24)
        speciesentry.grid(row=9, column=1, pady=15, padx=10)

        submitbutton = CTkButton(update_window, text='Submit', command=save_data)
        submitbutton.grid(row=10, columnspan=2, pady=15, padx=10)

        indexing = information.focus()
        content = information.item(indexing)
        listdata = content['values']

        rfidinfoentry.insert(0, listdata[1])
        parentinfoentry.insert(0, listdata[2])
        addressentry.insert(0, listdata[3])
        contactnumentry.insert(0, listdata[4])
        emailentry.insert(0, listdata[5])
        petnameentry.insert(0, listdata[6])
        petageentry.insert(0, listdata[7])
        petgenderentry.insert(0, listdata[8])
        breedentry.insert(0, listdata[9])
        speciesentry.insert(0, listdata[10])

        rfidinfoentry.config(state='readonly')

    # VIEW PET DETAILS BUTTON (FUNCTION)
    def show_pet_details():
        selected_item = information.focus()
        if selected_item:
            values = information.item(selected_item, 'values')

            if values:
                # TOPLEVEL FOR PET DETAILS
                details_window = CTkToplevel(window)
                details_window.title("Pet/Owner Details")
                details_window.geometry('900x800')
                details_window.resizable(False, False)
                details_window.grab_set()

                labels = ['I.D', 'RFID Number', 'Name', 'Address', 'Contact Number', 'Email address',
                          "Pet's Name", "Pet's Age", "Pet's Gender", 'Breed', 'Species']

                # PET DETAIL DISPLAY INSIDE TOPLEVEL
                for i, value in enumerate(values):
                    if i < len(labels):
                        title_label = CTkLabel(details_window, text=f"{labels[i]}:", font=('Arial', 20, 'bold'),
                                               text_color='Red')
                        title_label.grid(row=i, column=0, sticky="w", padx=0, pady=5)

                        value_label = CTkLabel(details_window, text=value, font=('Arial', 18, 'italic'),
                                               text_color='Black')
                        value_label.grid(row=i, column=1, sticky="w", padx=0, pady=5)

                # Diagnosis and Date Table Section
                diagnosis_frame = CTkFrame(details_window, width=50, height=900)
                diagnosis_frame.place(x=400, y=0)

                diagnosis_label = CTkLabel(diagnosis_frame, text="Diagnosis History:", font=('Arial', 18, 'bold'))
                diagnosis_label.grid(row=0, column=0, sticky="w")

                # Scrollable Table for Diagnosis History
                diagnosis_table_frame = Frame(diagnosis_frame)
                diagnosis_table_frame.grid(row=1, column=0, columnspan=2)

                scroll_y = Scrollbar(diagnosis_table_frame, orient=VERTICAL)

                diagnosis_table = ttk.Treeview(diagnosis_table_frame, columns=("date", "diagnosis"), show='headings',
                                               yscrollcommand=scroll_y.set, height=20)

                scroll_y.config(command=diagnosis_table.yview)
                scroll_y.pack(side=RIGHT, fill=Y)

                diagnosis_table.heading("date", text="Date")
                diagnosis_table.heading("diagnosis", text="Diagnosis")

                diagnosis_table.pack(fill=BOTH, expand=1)

                # Query the tb_diagdate table to get diagnosis history for this pet's RFID
                try:
                    query = "SELECT `date`, `diagnosis` FROM tb_diagdate WHERE RFID_Number = %s"
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
                            # Open a new window to show the full diagnosis and date
                            full_diagnosis_window = CTkToplevel(details_window)
                            full_diagnosis_window.title("Full Diagnosis Details")
                            full_diagnosis_window.geometry('500x300')
                            full_diagnosis_window.grab_set()

                            # Display full diagnosis text
                            date_label = CTkLabel(full_diagnosis_window, text=f"Date: {diag_values[0]}",
                                                  font=('Arial', 18, 'bold'), text_color='Red')
                            date_label.pack(pady=10)

                            diagnosis_label = CTkLabel(full_diagnosis_window, text=f"Diagnosis: {diag_values[1]}",
                                                       font=('Arial', 18, 'italic'), text_color='Black', wraplength=450)
                            diagnosis_label.pack(pady=10)

                # Bind the double-click event to the diagnosis table
                diagnosis_table.bind("<Double-1>", on_double_click)

    def show_data():
        if mycursor:
            query = 'SELECT * FROM tb_customerinfo'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            information.delete(*information.get_children())  # Clear existing data
            for data in fetched_data:
                information.insert('', END, values=data)  # Insert each row into the treeview

    def search_data():
        query = 'SELECT * FROM tb_customerinfo where RFID_Number = %s'
        mycursor.execute(query, (searchentry.get(),))
        information.delete(*information.get_children())
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            information.insert('', END, values=data)

    def fetch_data():
        query = 'SELECT * FROM tb_customerinfo'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        information.delete(*information.get_children())
        for data in fetched_data:
            information.insert('', END, values=data)

    def delete_data():
        indexing = information.focus()
        content = information.item(indexing)
        if not content['values']:
            messagebox.showerror('Error', 'No record selected')
            return

        content_id = content['values'][1]
        confirm = messagebox.askyesno('Confirm',
                                      f'Are you sure you want to delete the record with RFID no. {content_id}?')
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

    def addpetinfo():
        def add_data():
            if (rfidinfoentry.get() == '' or
                    parentinfoentry.get() == '' or
                    addressentry.get() == '' or
                    contactnumentry.get() == '' or
                    emailentry.get() == '' or
                    petnameentry.get() == '' or
                    petageentry.get() == '' or
                    petgenderentry.get() == '' or
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
                        result = messagebox.showinfo('Confirm',
                                                     'Data added successfully, Information added successfully',
                                                     parent=addpet_window)
                        if result:
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

        # window for entering pet/owner's info
        addpet_window = CTkToplevel(window)
        addpet_window.title("ADD PET/OWNER'S INFORMATION")
        addpet_window.resizable(False, False)
        addpet_window.grab_set()

        # entry field
        rfidinfolabel = Label(addpet_window, text="RFID NUMBER : ", font=('Arial', 15, 'bold'))
        rfidinfolabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
        rfidinfoentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        rfidinfoentry.grid(row=0, column=1, pady=15, padx=10)

        parentinfolabel = Label(addpet_window, text="PARENT'S NAME : ", font=('Arial', 15, 'bold'))
        parentinfolabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
        parentinfoentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        parentinfoentry.grid(row=1, column=1, pady=15, padx=10)

        addresslabel = Label(addpet_window, text="Address : ", font=('Arial', 15, 'bold'))
        addresslabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
        addressentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        addressentry.grid(row=2, column=1, pady=15, padx=10)

        contactnumlabel = Label(addpet_window, text="Contact Number : ", font=('Arial', 15, 'bold'))
        contactnumlabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
        contactnumentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        contactnumentry.grid(row=3, column=1, pady=15, padx=10)

        emaillabel = Label(addpet_window, text="E-mail Address : ", font=('Arial', 15, 'bold'))
        emaillabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
        emailentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        emailentry.grid(row=4, column=1, pady=15, padx=10)

        petnamelabel = Label(addpet_window, text="Pet's Name : ", font=('Arial', 15, 'bold'))
        petnamelabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
        petnameentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        petnameentry.grid(row=5, column=1, pady=15, padx=10)

        petagelabel = Label(addpet_window, text="Pet's Age : ", font=('Arial', 15, 'bold'))
        petagelabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
        petageentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        petageentry.grid(row=6, column=1, pady=15, padx=10)

        petgenderlabel = Label(addpet_window, text="Pet's Gender : ", font=('Arial', 15, 'bold'))
        petgenderlabel.grid(row=7, column=0, padx=30, pady=15, sticky=W)
        petgenderentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        petgenderentry.grid(row=7, column=1, pady=15, padx=10)

        breedlabel = Label(addpet_window, text="Pet's Breed : ", font=('Arial', 15, 'bold'))
        breedlabel.grid(row=8, column=0, padx=30, pady=15, sticky=W)
        breedentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        breedentry.grid(row=8, column=1, pady=15, padx=10)

        specieslabel = Label(addpet_window, text="Pet's Species  : ", font=('Arial', 15, 'bold'))
        specieslabel.grid(row=9, column=0, padx=30, pady=15, sticky=W)
        speciesentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        speciesentry.grid(row=9, column=1, pady=15, padx=10)

        submitbutton = CTkButton(addpet_window, text='Submit', command=add_data)
        submitbutton.grid(row=10, columnspan=2, pady=15, padx=10)

    # def calendarboard():
    #   window.destroy()
    #  import calendarWindow

    def add_petdiagnosis():
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
                # Insert data into tb_diagdate table with current date
                query = '''
                INSERT INTO tb_diagdate (diagnosis, RFID_Number, `date`) 
                VALUES (%s, %s, CURDATE())
                '''
                mycursor.execute(query, (
                    diagnosisentry.get(),  # Diagnosis
                    rfidinfoentry.get(),  # RFID Number
                ))
                con.commit()  # Commit changes to the database
                messagebox.showinfo('Success', 'Diagnosis added successfully', parent=addpet_window)

                # Close the add window after successful insertion
                addpet_window.destroy()

                # Refresh the data in the treeview
                show_data()  # This will reload data, including new diagnosis

            except pymysql.Error as e:
                messagebox.showerror('Error', f"Error occurred: {e}")

        # Window for entering pet/owner's info
        addpet_window = CTkToplevel(window)
        addpet_window.title("ADD PET/OWNER'S INFORMATION")
        addpet_window.resizable(False, False)
        addpet_window.grab_set()

        # Entry fields for RFID and Diagnosis
        rfidinfolabel = Label(addpet_window, text="RFID NUMBER: ", font=('Arial', 15, 'bold'))
        rfidinfolabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
        rfidinfoentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        rfidinfoentry.grid(row=0, column=1, pady=15, padx=10)

        diagnosislabel = Label(addpet_window, text="DIAGNOSIS: ", font=('Arial', 15, 'bold'))
        diagnosislabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
        diagnosisentry = Entry(addpet_window, font=('Arial', 15, 'italic'), width=24)
        diagnosisentry.grid(row=1, column=1, pady=15, padx=10)

        submitbutton = CTkButton(addpet_window, text='Submit', command=add_data)
        submitbutton.grid(row=7, columnspan=2, pady=15, padx=10)

    # function to connect to the database
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
            # calendarbutton.configure(state=NORMAL)
            view_button.configure(state=NORMAL)
            updatebutton.configure(state=NORMAL)

        connectwindow = CTkToplevel()
        connectwindow.geometry('470x250+730+230')
        connectwindow.title('Database Connection')
        connectwindow.grab_set()

        # Window fields for DB connection
        hostlabel = CTkLabel(connectwindow, text="HOST NAME: ", font=('Arial', 12))
        hostlabel.place(x=50, y=50)
        hostentry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'))
        hostentry.place(x=200, y=50)

        userlabel = CTkLabel(connectwindow, text="USER NAME: ", font=('Arial', 12))
        userlabel.place(x=50, y=100)
        userentry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'))
        userentry.place(x=200, y=100)

        passwlabel = CTkLabel(connectwindow, text="PASSWORD: ", font=('Arial', 12))
        passwlabel.place(x=50, y=150)
        passwentry = CTkEntry(connectwindow, font=('Arial', 12, 'italic'), show="*")
        passwentry.place(x=200, y=150)

        submitbutton = CTkButton(connectwindow, text='Submit', command=connect)
        submitbutton.place(x=200, y=200)

    # background picture
    bgpicture = CTkImage(dark_image=Image.open('bg1.jpg'), size=(1600, 800))
    bgpicturelabel = CTkLabel(window, image=bgpicture, text='')
    bgpicturelabel.place(x=0, y=0)

    # clock
    count = 0
    text = ''

    def clock():
        timex = strftime(' %I:%M:%S')
        date = strftime('   %B %d, %Y')
        currentimelabel.configure(text=f'{date}\n Time: {timex}', font=('times new roman', 25, 'bold'),
                                  bg_color='#C7DBB8')
        currentimelabel.after(1000, clock)

    currentimelabel = CTkLabel(window)
    currentimelabel.place(x=1280, y=10)
    clock()






    style = ttk.Style()
    style.theme_use("default")
    style.configure('Treeview.Heading',
                    background='#557C56',
                    foreground='#F4F6FF',
                    font=('Times new roman', 14, 'bold')
                    )
    style.map('Treeview.Heading', background=[('active', '#6A9C89')])
    style.configure("Treeview",
                    background='#C7DBB8',  # background sa treeview
                    # foreground='white', #text color
                    rowheight=30,  # nipis
                    fieldbackground='#C7DBB8',
                    fontstyle=('times new roman', 35)
                    )
    style.map('Treeview', background=[('selected', 'green')])  # selected row

    treeviewframe = Frame(window)
    treeviewframe.place(x=300, y=100, width=600, height=500)
    scrollbarX = Scrollbar(treeviewframe, orient=HORIZONTAL)
    scrollbarY = Scrollbar(treeviewframe, orient=VERTICAL)

    information = ttk.Treeview(treeviewframe,
                               columns=('ID', 'RFID_Number', 'Name', 'Address', 'cnum', 'emailadd', "Petname",
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

    leftside = CTkFrame(window, width=250, height=800, fg_color='#C1D8C3')
    leftside.place(x=0, y=0)

    # LEFT SIDE BUTTON


    adminpic = CTkImage(light_image=Image.open('man.png'), size=(75, 75))
    helloadmin = CTkLabel(window, text="  Hello ADMIN", image=adminpic, compound='left', fg_color='#C1D8C3',
                          font=('Times new roman', 25, 'bold', 'italic'))
    helloadmin.place(x=10, y=5)

    admintext = CTkLabel(window, text="Pet information", fg_color='#C1D8C3', font=('times new roman', 20, 'bold'),
                         text_color='#1A5319')
    admintext.place(x=0, y=100)

    addpetpic = CTkImage(light_image=Image.open('kitten.png'), size=(35, 35))
    addpetinfo = CTkButton(window, text='Add New Pet Information', image=addpetpic, compound='left', command=addpetinfo,
                           state=DISABLED, width=250, height=50, corner_radius=0, font=("arial", 14, 'bold'),
                           border_width=2, border_color='#1A5319', fg_color="#387478", hover_color='#729762')
    addpetinfo.place(x=0, y=130)

    diagpic = CTkImage(light_image=Image.open('medical-report.png'), size=(35, 35))
    add_petdiagnosis = CTkButton(window, text='Pet Diagnosis', image=diagpic, compound='left', command=add_petdiagnosis,
                                 state=DISABLED, width=250, height=45, corner_radius=0, font=("arial", 14, 'bold'),
                                 border_width=2, border_color='#1A5319', fg_color="#387478", hover_color='#729762')
    add_petdiagnosis.place(x=0, y=178)

    staffinfo = CTkButton(window, text='STAFF INFORMATION', state=DISABLED, width=250, height=45, corner_radius=0,
                          font=("arial", 14, 'bold'))
    staffinfo.place(x=0, y=600)

    addstaffinfo = CTkButton(window, text='ADD NEW STAFF INFO', state=DISABLED, width=250, height=45, corner_radius=0,
                             font=("arial", 14, 'bold'))
    addstaffinfo.place(x=0, y=550)

    viewreport = CTkButton(window, text='VIEW ALL DATA', state=DISABLED, command=show_data, width=250, height=45,
                           corner_radius=0, font=("arial", 14, 'bold'))
    viewreport.place(x=0, y=450)

    """calendarpic = CTkImage(light_image=Image.open('calendar.png'),size = (35,35))
    calendarbutton = CTkButton(window,text='View Calendar',image=calendarpic,state=DISABLED,command=calendarboard,width=250,height=45,corner_radius=0,compound='left',font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
    calendarbutton.place(x=0,y=220)"""

    searchentry = CTkEntry(window, placeholder_text='Search RFID Number')
    searchentry.place(x=300, y=60)
    searchbutton = CTkButton(window, text='Search', state=DISABLED, command=search_data, width=50)
    searchbutton.place(x=450, y=60)

    updatebutton = CTkButton(window, text='Update Data', state=DISABLED, command=update_button, width=180, height=40,
                             font=("arial", 16, 'bold'))
    updatebutton.place(x=680, y=630)

    deletebutton = CTkButton(window, text='Delete Data', state=DISABLED, command=delete_data, width=180, height=40,
                             font=("arial", 16, 'bold'))
    deletebutton.place(x=490, y=630)

    exportbutton = CTkButton(window, text='Export Data', state=DISABLED, command=export_data, width=250, height=45,
                             corner_radius=0, font=("arial", 14, 'bold'))
    exportbutton.place(x=0, y=350)

    logoutbutton = CTkButton(window, text='Log Out', width=250, height=45, corner_radius=0, font=("arial", 14, 'bold'),
                             command=log_out)
    logoutbutton.place(x=0, y=750)

    # SERVER BUTTON
    connectbutton = CTkButton(window, text='Connect to Server', command=connect_database, width=250, height=45,
                              corner_radius=0, font=("arial", 14, 'bold'))
    connectbutton.place(x=0, y=700)

    view_button = CTkButton(window, text="View Pet Details", command=show_pet_details, state=DISABLED, width=180, height=40,
                            font=("arial", 16, 'bold'))
    view_button.place(x=300, y=630)

    # CALENDAR
    conn = connect_db()
    if conn is None:
        print("Unable to connect to the database.")
        window.quit()

    # Calendar widget
    cal = Calendar(window, selectmode='day', date_pattern="yyyy-mm-dd",
                   font=("Arial", 25, 'italic'),
                   showweeknumbers=False,
                   showothermonthdays=False,
                   background='#90EE90',
                   selectbackground='#FFB6C1'
                   )
    cal.place(x=930, y=100)

    # Highlight existing event dates on calendar load
    highlight_existing_event_dates()

    # Event entry
    # event_label = CTkLabel(window, text="Event Description:")
    # event_label.place(x=930,y=440)
    event_entry = CTkEntry(window, width=300, placeholder_text="Event Description")
    event_entry.place(x=930, y=470)

    # Add event button
    add_event_btn = CTkButton(window, text="Add Event", command=add_event)
    add_event_btn.place(x=930, y=500)

    # Listbox to display events for selected date
    event_listbox_label = CTkLabel(window, text="Events on selected date:", bg_color='#C7DBB8')
    event_listbox_label.place(x=1090, y=505)
    event_listbox = tk.Listbox(window, width=60, height=15)
    event_listbox.place(x=1090, y=535)

    # Bind the date selection event to update the event list
    cal.bind("<<CalendarSelected>>", on_date_select)

    window.mainloop()
    if conn and conn.is_connected():
        conn.close()












bgpicture = CTkImage(dark_image=Image.open('bg1.jpg'),size=(1400,800))
bgpicturelabel = CTkLabel(root, image=bgpicture,text='')
bgpicturelabel.place (x=0,y=0)

#PET PICTURE FRAME AND LOGO
vetpicture = CTkImage(dark_image=Image.open('pic1.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=70,y=60)

vetpicture = CTkImage(dark_image=Image.open('pic2.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=275,y=60)

vetpicture = CTkImage(dark_image=Image.open('pic3.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=480,y=60)

vetpicture = CTkImage(dark_image=Image.open('pic4.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=70,y=265)

vetpicture = CTkImage(dark_image=Image.open('logo.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=275,y=265)

vetpicture = CTkImage(dark_image=Image.open('pic5.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=480,y=265)

vetpicture = CTkImage(dark_image=Image.open('pic6.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=70,y=470)

vetpicture = CTkImage(dark_image=Image.open('pic7.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=275,y=470)

vetpicture = CTkImage(dark_image=Image.open('pic8.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=480,y=470)


loginFrame = CTkFrame(root, width=350, height=480,fg_color="#F6F5F2",border_color='#798645',border_width=3)
loginFrame.place(x=830,y=100)


ctk_image = CTkImage(dark_image=Image.open('pawprint.png'), size=(100, 100))
image_label = CTkLabel(loginFrame, image=ctk_image, text="")
image_label.place(x=130,y=15)

welcometext=CTkLabel(loginFrame,text='Welcome',font=('Arial',45))
welcometext.place(x=80,y=120)


#user
#usernamepic = Image.open('id-card.png').resize((20,20)) image=CTkImage(dark_image=usernamepic)
username = CTkLabel(loginFrame,compound='left',text=" Username ",font=('Arial',15))
username.place(x=30,y=170)
userentry=CTkEntry(loginFrame,font=('times new roman',18),placeholder_text= 'Enter Username',width=280,height=45,border_color='#798645',corner_radius=15)
userentry.place(x=30,y=200)

#password
##passwordpic = Image.open('locked.png').resize((20,20)),image=CTkImage(dark_image=passwordpic)
password = CTkLabel(loginFrame,text=" Password ",compound='left',font=('Arial',15))
password.place(x=30,y=260)
passentry=CTkEntry(loginFrame,font=('times new roman',19),placeholder_text= 'Enter Password',width=280,height=40,show='*',border_color='#798645',corner_radius=15)
passentry.place(x=30,y=290)



loginpic = Image.open('enter1.png')
resized_loginpic = CTkImage(light_image=loginpic,size = (45,45))
Submit = CTkButton(loginFrame,text='LOGIN',
                   font=("arial",20,'bold'),
                   image=resized_loginpic,
                   compound='right',text_color='#FFEAC5',
                   corner_radius=10,
                   hover_color='#83c7ac' ,
                   fg_color= '#16423C',
                   border_color= '#16423C',
                   border_width=1, width=270,height=60,
                    command=login)
Submit.place(x=35,y=360)




















root.mainloop()
