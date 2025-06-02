#MODULES
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
from customtkinter import CTkButton, CTkFrame, CTkImage
from PIL import Image, ImageDraw, ImageOps #to support jpeg format
import pandas   #FOR CSV
import customtkinter as ctk
import io
import serial
import threading
from tkinter import ttk
from ttkthemes import ThemedStyle



arduino_port = 'COM3 '
baud_rate = 9600
selected_binary_data = None


#------------------------------------------------------------------------------------------------------------------
#MODULE CONFIGURATION
window=CTk()
window.geometry('1510x694+10+80')
window.resizable(False,False)
window.title('ADMINISTRATOR')
set_appearance_mode("light")
style = ThemedStyle(window)
style.set_theme("breeze")
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
    selected_date_str = cal.get_date()
    event = event_entry.get()

    if selected_date_str and event:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO events (event_date, event_description) VALUES (%s, %s)"
            cursor.execute(query, (selected_date_str, event))
            conn.commit()
            event_entry.delete(0, tk.END)
            update_event_list(selected_date_str)
            highlight_event_date(selected_date_str)
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
    update_window.geometry('1180x490+80+90')
    update_window.resizable(False, False)
    update_window.grab_set()

    editpet_BG = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\edit_information.jpg'), size=(1440,490))
    edit_BGLabel = CTkLabel(update_window, image=editpet_BG, text='')
    edit_BGLabel.place(x=0, y=0)

    # for ownersFrame


    #UPDATE ================================================ OWNERS INFORMATION ===============================================
    #1 UPDATE
    rfidinfoentry = CTkEntry(update_window, font=('Arial', 13, 'italic'), width=140, border_color='black')
    rfidinfoentry.place(x=260, y=157)
    rfidinfoentry.bind("<Button-1>", rfid_warning)

    # 2
    parentinfoentry = CTkEntry(update_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    parentinfoentry.place(x=260, y=208)
    # 3
    # contactnumlabel = Label(addpet_window, text="Contact Number : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    # contactnumlabel.place(x=50,y=150)
    contactnumentry = CTkEntry(update_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    contactnumentry.place(x=260, y=260)

    # 4
    addressentry = CTkEntry(update_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    addressentry.place(x=260, y=311)

    # 5
    # emaillabel = Label(addpet_window, text="E-mail Address   : ", font=('Arial', 12, 'bold'),bg='#C7DBB8')
    # emaillabel.place(x=50,y=250)
    emailentry = CTkEntry(update_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    emailentry.place(x=260, y=362)
    # ================================================ PETS INFORMATION ===============================================
    # 1
    petnameentry = CTkEntry(update_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    petnameentry.place(x=800, y=157)
    # 2
    petageentry = CTkEntry(update_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    petageentry.place(x=800, y=208)
    #3 UPDATE
    genderChoices = ['Male', 'Female']
    petgenderentry = ctk.CTkComboBox(update_window, values=genderChoices, border_color='black')
    petgenderentry.place(x=800, y=260)
    petgenderentry.set('Select an option')
    #4 UPDATE
    breedentry = CTkEntry(update_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    breedentry.place(x=800, y=311)
    #5 UPDATE
    speciesentry = CTkEntry(update_window, font=('Arial', 12, 'italic'), width=250, border_color='black')
    speciesentry.place(x=800, y=362)

    submitbutton = CTkButton(update_window, text='Submit',command=save_data, width=250, height=45,
                             font=("arial", 16, 'bold'), border_width=2, border_color='#1A5319', fg_color="#387478",
                             hover_color='#729762')
    submitbutton.place(x=860, y=430)

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
    petgenderentry.set( listdata[8])
    breedentry.insert(0, listdata[9])
    speciesentry.insert(0, listdata[10])

    rfidinfoentry.configure(state='readonly')
#------------------------------------------------------------------------------------------------------------------
def show_pet_details():
    selected_item = information.focus()
    if selected_item:
        values = information.item(selected_item, 'values')
        if values:
            selected_rfid = values[1]  # Assuming RFID_Number is at index 1

            mycursor.execute('SELECT tb_PetImage FROM tb_picture WHERE RFID_Number = %s ORDER BY tb_id DESC LIMIT 1',
                             (selected_rfid,))
            result = mycursor.fetchone()

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
                details_window.title("PET & OWNER'S DETAIL")
                details_window.geometry('1255x650+250+130')
                details_window.resizable(False, False)
                details_window.grab_set()

                details_windowBG = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\petdetails.jpg'), size=(1400, 650))
                details_windowBGLabel = CTkLabel(details_window, image=details_windowBG, text='')
                details_windowBGLabel.place(x=0, y=0)

                # Create circular version of the image
                def create_circle_image(image_data, size=(200, 200)):
                    img = Image.open(io.BytesIO(image_data)).convert("RGBA")
                    img = img.resize(size, Image.Resampling.LANCZOS)

                    # Create a mask for the circle
                    mask = Image.new("L", size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0) + size, fill=255)

                    # Apply mask to the image
                    circular_img = ImageOps.fit(img, size, centering=(0.5, 0.5))
                    circular_img.putalpha(mask)

                    return circular_img

                # Load and process the image
                if result:
                    selected_binary_data = result[0]
                    circular_image = create_circle_image(selected_binary_data)
                    img_tk = CTkImage(light_image=circular_image, size=(180, 180))

                 #Initialize the viewPetPicture frame before using it
                viewPetPicture = CTkFrame(details_window, width=180, height=180, fg_color='white', border_width=0)
                viewPetPicture.place(x=36, y=250)

                label = CTkLabel(viewPetPicture, image=img_tk, text='')
                label.image = img_tk
                label.place(x=0, y=0)

                # Unpack values
                (
                    id, rfid, name, address, contact, email, petname,
                    pet_age, pet_gender, breed, species
                ) = values

                # Function to wrap address text every 5 words
                def wrap_address(text, max_words=5):
                    words = text.split()
                    return '\n'.join(' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words))

                # --- PET INFO SECTION ---
                CTkLabel(details_window, text=rfid, font=('Fredoka', 14,'bold'),text_color='#54321A',bg_color='white').place(x=315, y=312)
                CTkLabel(details_window, text=petname, font=('Fredoka', 43, 'bold','italic'),text_color='#54321A',bg_color='white').place(x=310, y=235)
                CTkLabel(details_window, text=pet_age,  font=('Fredoka', 14,'bold'),text_color='#54321A',bg_color='white').place(x=315, y=335)
                CTkLabel(details_window, text=breed, font=('Fredoka', 14,'bold'),text_color='#54321A',bg_color='white').place(x=315, y=356)
                CTkLabel(details_window, text=species, font=('Fredoka', 14,'bold'),text_color='#54321A',bg_color='white').place(x=315, y=383)

                # --- OWNER INFO SECTION ---

                CTkLabel(details_window, text=name, font=('Fredoka', 14,'bold'),text_color='#54321A',bg_color='white').place(x=525, y=300)
                CTkLabel(details_window, text=wrap_address(address),font=('Fredoka', 14,'bold'),text_color='#54321A',bg_color='white').place(x=525, y=384)
                CTkLabel(details_window, text=contact, font=('Fredoka', 14,'bold'),text_color='#54321A',bg_color='white').place(x=525, y=330)
                CTkLabel(details_window, text=email, font=('Fredoka', 14,'bold'),text_color='#54321A',bg_color='white').place(x=525, y=356)

                def fetch_data():
                    try:
                        # Clear existing rows
                        diagnosis_table.delete(*diagnosis_table.get_children())

                        # Fetch updated diagnosis data including diag_id
                        query = "SELECT diag_id, diag_date, diagnosis FROM tb_diagdate WHERE RFID_Number = %s"
                        mycursor.execute(query, (values[1],))  # Replace `values[1]` with current pet RFID if needed
                        fetched_data = mycursor.fetchall()

                        for data in fetched_data:
                            diagnosis_table.insert('', END, values=data)

                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to fetch data: {e}", parent=details_window)

                def delete_remarks():
                    indexing = diagnosis_table.focus()
                    content = diagnosis_table.item(indexing)
                    if not content['values']:
                        messagebox.showerror('Error', 'No record selected', parent=details_window)
                        return

                    diag_id = content['values'][0]  # Now this will be the correct diag_id
                    confirm = messagebox.askyesno('Confirm', 'Are you sure you want to delete the record?',
                                                  parent=details_window)
                    if not confirm:
                        return

                    try:
                        query = 'DELETE FROM tb_diagdate WHERE diag_id = %s'
                        mycursor.execute(query, (diag_id,))
                        con.commit()

                        messagebox.showinfo('DELETED', 'The record was deleted successfully', parent=details_window)
                        fetch_data()
                    except Exception as e:
                        messagebox.showerror('Error', f'An error occurred: {e}', parent=details_window)

                def edit_remarks():
                    selected = diagnosis_table.focus()
                    content = diagnosis_table.item(selected)

                    if not content['values']:
                        messagebox.showerror("Error", "No record selected", parent=details_window)
                        return

                    diag_id, current_date, current_diag = content['values']

                    edit_window = CTkToplevel(details_window)
                    edit_window.title("Edit Remarks")
                    edit_window.geometry("400x400+1270+360")
                    edit_window.grab_set()

                    edit_window_image = CTkImage(
                        dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\editremarks.jpg'), size=(400, 400))
                    edit_windowLabel = CTkLabel(edit_window,image=edit_window_image, text='')
                    edit_windowLabel.place(x=0, y=0)


                    # Date field
                    #date_label = CTkLabel(edit_window, text="Date (YYYY-MM-DD):", font=("Arial", 14))
                    #date_label.pack(pady=5)
                    date_entry = CTkEntry(edit_window, font=("Arial", 14),border_color='black',corner_radius=-1)
                    date_entry.insert(0, str(current_date))
                    date_entry.place(x=58,y=120)

                    # Diagnosis field

                    diagnosis_entry = CTkTextbox(edit_window, font=("Arial", 14), width=286,height=160,border_width=2,corner_radius=-1,border_color='black')
                    diagnosis_entry.insert("1.0", current_diag)
                    diagnosis_entry.place(x=58,y=170)

                    def save_changes():
                        new_date = date_entry.get()
                        new_diagnosis = diagnosis_entry.get("1.0", "end-1c")

                        if not new_date or not new_diagnosis:
                            messagebox.showerror("Error", "All fields are required", parent=edit_window)
                            return

                        try:
                            update_query = """
                            UPDATE tb_diagdate 
                            SET diag_date = %s, diagnosis = %s 
                            WHERE diag_id = %s
                            """
                            mycursor.execute(update_query, (new_date, new_diagnosis, diag_id))
                            con.commit()

                            messagebox.showinfo("Success", "Diagnosis updated successfully", parent=edit_window)
                            edit_window.destroy()
                            fetch_data()
                        except Exception as e:
                            messagebox.showerror("Error", f"Update failed: {e}", parent=edit_window)

                    save_button = CTkButton(edit_window, text="Save Changes", command=save_changes,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
                    save_button.place(x=215,y=357)

                # Scrollable table for diagnosis history
                diagnosis_frame = CTkFrame(details_window, width=90, height=18)
                diagnosis_frame.place(x=850, y=240)

                diagnosis_table_frame = Frame(diagnosis_frame)
                diagnosis_table_frame.grid(row=1, column=0, columnspan=2)

                scroll_y = Scrollbar(diagnosis_table_frame, orient=VERTICAL)
                diagnosis_table = ttk.Treeview(diagnosis_table_frame,columns=("diag_id", "date", "diagnosis"),show='headings',yscrollcommand=scroll_y.set,height=10)

                scroll_y.config(command=diagnosis_table.yview)
                scroll_y.pack(side=RIGHT, fill=Y)

                diagnosis_table.heading("diag_id", text="ID")
                diagnosis_table.heading("date", text="Date")
                diagnosis_table.heading("diagnosis", text="Remarks")
                diagnosis_table.column("diag_id", width=0, stretch=False)

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
                            full_diagnosis_window.geometry('500x300+530+380')
                            full_diagnosis_window.grab_set()

                            full_diagnosis_window_image = CTkImage(
                                dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\remarks&diagnosis.jpg'), size=(500, 300))
                            full_diagnosis_windowLabel = CTkLabel(full_diagnosis_window,
                                                                  image=full_diagnosis_window_image, text='')
                            full_diagnosis_windowLabel.place(x=0, y=0)

                            date_label = CTkLabel(full_diagnosis_window, text=f"{diag_values[1]}",
                                                  font=('Arial', 18, 'bold'), text_color='Red', fg_color='#ffffe3')
                            date_label.place(x=112, y=85)

                            diagnosis_label = CTkLabel(full_diagnosis_window, text=f"{diag_values[2]}",
                                                       font=('Arial', 12, 'italic'), text_color='Black', wraplength=300,
                                                       fg_color='#ffffe3')
                            diagnosis_label.place(x=112, y=145)

                diagnosis_table.bind("<Double-1>", on_double_click)

                # Buttons for editing and deleting diagnosis
                edit_details_Button = CTkButton(details_window, text='Edit Remarks',command=edit_remarks, width=172, height=60,
                                                font=("arial", 16, 'bold'), border_width=2, corner_radius=0,
                                                border_color='#1A5319', fg_color="#387478", hover_color='#729762')
                edit_details_Button.place(x=850, y=500)

                delete_details_Button = CTkButton(details_window, text='Delete Remarks',command=delete_remarks, width=170, height=60,
                                                  font=("arial", 16, 'bold'), border_width=2, corner_radius=0,
                                                  border_color='#1A5319', fg_color="#387478", hover_color='#729762')
                delete_details_Button.place(x=1020, y=500)


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
    query = 'SELECT * FROM tb_customerinfo where Name = %s'
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

                img = Image.open(file_path)
                img = img.resize((235, 238))
                img_tk = CTkImage(light_image=img, size=(234, 234))

                label = CTkLabel(petpictureFrame, image=img_tk, text="")
                label.image = img_tk
                label.place(x=3, y=3)

    def read_rfid_continuous():
        try:
            with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
                rfidinfoentry.configure(state="normal")
                rfidinfoentry.delete(0, ctk.END)
                rfidinfoentry.insert(0, "Waiting for RFID card...")
                rfidinfoentry.configure(state="readonly")

                while True:
                    if ser.in_waiting:
                        rfid_data = ser.readline().decode('utf-8').strip()
                        if rfid_data:
                            rfidinfoentry.configure(state="normal")
                            rfidinfoentry.delete(0, ctk.END)
                            rfidinfoentry.insert(0, rfid_data)
                            rfidinfoentry.configure(state="readonly")
                            break  # Stop after reading once
                    time.sleep(0.1)
        except Exception as e:
            rfidinfoentry.configure(state="normal")
            rfidinfoentry.delete(0, ctk.END)
            rfidinfoentry.insert(0, f"Error: {e}")
            rfidinfoentry.configure(state="readonly")

    # Start the RFID thread
    def start_read_rfid_thread():
        threading.Thread(target=read_rfid_continuous, daemon=True).start()


    #window for entering pet/owner's info
    addpet_window = CTkToplevel(window)
    addpet_window.title("ADD PET/OWNER'S INFORMATION")
    addpet_window.geometry('1420x490+80+150')
    addpet_window.resizable(False, False)
    addpet_window.grab_set()

    addpet_BG = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\bgsample.jpg'),size=(1440,490))
    addpet_BGLabel = CTkLabel(addpet_window,image=addpet_BG,text='')
    addpet_BGLabel.place(x=0,y=0)
    #for ownersFrame
    # ================================================ PICTURE IMPORT ===============================================
    petpictureFrame = CTkFrame(addpet_window, fg_color='white', width=240, height=240, border_color='black',
                               border_width=2)
    petpictureFrame.place(x=1080, y=130)

    petpictureButton = CTkButton(addpet_window, text='Add Photo', command=pet_uploadImage, font=("arial", 16, 'bold'),
                                 width=240, border_width=1, border_color='#1A5319', fg_color="#387478",
                                 hover_color='#729762')
    petpictureButton.place(x=1080, y=380)

    # ================================================ OWNERS INFORMATION ===============================================
    # 1
    rfidinfoentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=140, border_color='black')
    rfidinfoentry.place(x=260, y=157)
    rfidinfoentry.insert(0, "Scan RFID Card")
    rfidinfoentry.configure(state="readonly")
    read_button = CTkButton(addpet_window, text="Scan RFID", command=start_read_rfid_thread,width=100, border_width=2, border_color='#1A5319', fg_color="#387478",
                             hover_color='#729762')
    read_button.place(x=410, y=157)

    # 2
    parentinfoentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    parentinfoentry.place(x=260, y=208)
    # 3
    contactnumentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    contactnumentry.place(x=260, y=260)

    # 4
    addressentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    addressentry.place(x=260, y=311)

    # 5
    emailentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    emailentry.place(x=260, y=362)
    # ================================================ PETS INFORMATION ===============================================
    # 1
    petnameentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    petnameentry.place(x=800, y=157)
    # 2
    petageentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    petageentry.place(x=800, y=208)
    # 3
    genderChoices = ['Male', 'Female']
    petgenderentry = ctk.CTkComboBox(addpet_window, values=genderChoices,border_color='black')
    petgenderentry.place(x=800, y=260)
    petgenderentry.set('Select an option')
    # 4
    breedentry = CTkEntry(addpet_window, font=('Arial', 13, 'italic'), width=250, border_color='black')
    breedentry.place(x=800, y=311)
    # 5
    speciesentry = CTkEntry(addpet_window, font=('Arial', 12, 'italic'), width=250, border_color='black')
    speciesentry.place(x=800, y=362)
    submitbutton = CTkButton(addpet_window, text='Submit', command=add_data, width=240, height=45,
                             font=("arial", 16, 'bold'), border_width=2, border_color='#1A5319', fg_color="#387478",
                             hover_color='#729762')
    submitbutton.place(x=1080, y=428)

def inventory_section():
    def register_stock():
        # Get data from the entry widgets
        inventory_id = InventoryID.get()
        stock_name = StockName.get()
        item_description = description.get()
        unit_price = unitprice.get()
        reorder_level = reorderlevel.get()
        quantity = levelqty.get()

        # Validate inputs
        if not inventory_id or not stock_name or not item_description or not unit_price or not reorder_level or not quantity:
            messagebox.showwarning("Input Error", "Please fill in all fields.",parent=inventoryRecord)
            return

        try:
            # Convert inputs to the correct types
            inventory_id = int(inventory_id)
            unit_price = int(unit_price)
            reorder_level = int(reorder_level)
            quantity = int(quantity)

        except ValueError:
            messagebox.showwarning("Input Error",
                                   "Please enter valid numeric values for inventory ID, unit price, reorder level, and quantity.",parent=inventoryRecord)
            return

        cursor = conn.cursor()
        insert_query = """
                INSERT INTO tb_stockordering (InventoryID, ItemName, Description, Unit_Price, reorderlevel, qty)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

        # Execute the query with data
        cursor.execute(insert_query, (inventory_id, stock_name, item_description, unit_price, reorder_level, quantity))

        # Commit the changes to the database
        conn.commit()

        # Provide feedback to the user
        messagebox.showinfo("Success", "Stock item registered successfully!",parent=inventoryRecord)

        # Clear the entry fields after successful registration
        InventoryID.delete(0, 'end')
        StockName.delete(0, 'end')
        description.delete(0, 'end')
        unitprice.delete(0, 'end')
        reorderlevel.delete(0, 'end')
        levelqty.delete(0, 'end')

        cursor.close()

        fetch_data()

    def fetch_data():
        try:
            cursor = conn.cursor()
            cursor.execute("USE vetclinicmanagementsystemnew;")
            cursor.execute("SELECT * FROM tb_stockordering")
            rows = cursor.fetchall()
            cursor.close()

            header.delete(*header.get_children())
            for row in rows:
                header.insert('', 'end', values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=inventoryRecord)

    def delete_button():
        indexing = header.focus()
        content = header.item(indexing)
        if not content['values']:
            messagebox.showerror('Error', 'No record selected', parent=inventoryRecord)
            return

        content_id = content['values'][1]  # [1] is InventoryID

        confirm = messagebox.askyesno('Confirm',
                                      f'Are you sure you want to delete the record with Inventory ID {content_id}?',
                                      parent=inventoryRecord)
        if not confirm:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("USE vetclinicmanagementsystemnew;")
            query = 'DELETE FROM tb_stockordering WHERE InventoryID = %s'
            cursor.execute(query, (content_id,))
            conn.commit()
            cursor.close()

            messagebox.showinfo('DELETED', f'The record with Inventory ID {content_id} was deleted successfully',
                                parent=inventoryRecord)
            fetch_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}", parent=inventoryRecord)

    def export_to_excel():
        # Ask where to save the file
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        # Get selected rows
        selected_items = header.selection()
        if not selected_items:
            messagebox.showwarning("No selection", "Please select rows to export.")
            return

        export_rows = []

        for item in selected_items:
            row_data = header.item(item, 'values')
            inventory_id = row_data[1]  #
            export_rows.append(row_data)

        # Define column names based on your Treeview
        columns = ['id', 'InventoryID', 'Item Name', 'Description', 'Unit Price', 'Reorder Level', 'Quantity']

        table = pandas.DataFrame(export_rows, columns=columns)
        table.to_excel(file_path, index=False)

        messagebox.showinfo("Success", "Selected data has been exported.")

    selected_record_id = None  # Declare globally or at top of your function

    def update_stock():
        global selected_record_id
        if selected_record_id is None:
            messagebox.showerror("Error", "No record selected for update", parent=inventoryRecord)
            return

        # Get updated values from entries
        updated_data = (
            InventoryID.get(),
            StockName.get(),
            description.get(),
            unitprice.get(),
            reorderlevel.get(),
            levelqty.get()
        )

        # Basic validation
        if not all(updated_data):
            messagebox.showwarning("Input Error", "Please fill in all fields.", parent=inventoryRecord)
            return

        try:
            # Cast to correct types
            int(updated_data[0])  # InventoryID
            int(updated_data[3])  # Unit_Price
            int(updated_data[4])  # Reorder Level
            int(updated_data[5])  # Quantity
        except ValueError:
            messagebox.showwarning("Input Error", "Ensure numeric fields are valid numbers.", parent=inventoryRecord)
            return

        try:
            cursor = conn.cursor()
            update_query = """
                UPDATE tb_stockordering SET 
                    InventoryID = %s,
                    ItemName = %s,
                    Description = %s,
                    Unit_Price = %s,
                    reorderlevel = %s,
                    qty = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (*updated_data, selected_record_id))
            conn.commit()
            cursor.close()

            messagebox.showinfo("Success", "Stock record updated successfully.", parent=inventoryRecord)
            fetch_data()
            selected_record_id = None  # Clear after update

            # Clear entries
            for entry in (InventoryID, StockName, description, unitprice, reorderlevel, levelqty):
                entry.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=inventoryRecord)

    def on_treeview_double_click(event):
        global selected_record_id
        selected_item = header.focus()
        if not selected_item:
            return

        values = header.item(selected_item, 'values')
        if not values:
            return

        selected_record_id = values[0]  # Store the record's ID for the update

        # Populate entry fields
        InventoryID.delete(0, 'end')
        InventoryID.insert(0, values[1])

        StockName.delete(0, 'end')
        StockName.insert(0, values[2])

        description.delete(0, 'end')
        description.insert(0, values[3])

        unitprice.delete(0, 'end')
        unitprice.insert(0, values[4])

        reorderlevel.delete(0, 'end')
        reorderlevel.insert(0, values[5])

        levelqty.delete(0, 'end')
        levelqty.insert(0, values[6])

    inventoryRecord = CTkToplevel(window)
    inventoryRecord.geometry('1100x830+300+15')
    inventoryRecord.title("INVENTORY LIST")
    inventoryRecord.resizable(False, False)
    inventoryRecord.grab_set()

    view_inventory = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\stockordering.jpg'), size=(1100, 900))
    view_inventorylabel = CTkLabel(inventoryRecord, image=view_inventory, text='')
    view_inventorylabel.place(x=0, y=0)

    # Entry widgets for stock details
    InventoryID = CTkEntry(inventoryRecord, width=180, bg_color='white', height=24, corner_radius=-1, border_color='#cbcbcb')
    InventoryID.place(x=60, y=216)

    StockName = CTkEntry(inventoryRecord, width=200, bg_color='white', height=24, corner_radius=-1, border_color='#cbcbcb')
    StockName.place(x=60, y=270)

    description = CTkEntry(inventoryRecord, width=330, bg_color='white', height=24, corner_radius=-1, border_color='#cbcbcb')
    description.place(x=60, y=324)

    unitprice = CTkEntry(inventoryRecord, width=120, bg_color='white', height=24, corner_radius=-1, border_color='#cbcbcb')
    unitprice.place(x=60, y=378)

    reorderlevel = CTkEntry(inventoryRecord, width=120, bg_color='white', height=24, corner_radius=-1, border_color='#cbcbcb')
    reorderlevel.place(x=60, y=475)

    levelqty = CTkEntry(inventoryRecord, width=120, bg_color='white', height=24, corner_radius=-1, border_color='#cbcbcb')
    levelqty.place(x=243, y=475)

    # Register Button
    registerbutton = CTkButton(inventoryRecord, text="REGISTER", command=register_stock, width=200,
                               height=60, font=("arial", 14, 'bold'), border_width=2, border_color='white',
                               fg_color="#f2b62a", hover_color='#729762', bg_color='#303030', text_color='black')
    registerbutton.place(x=200, y=550)

    inventoryframe = CTkFrame(inventoryRecord, width=1500, height=1500, border_color='#4DA1A9', border_width=4, fg_color="#B3C8CF")
    inventoryframe.place(x=450, y=170)

    inv_treeviewframe = Frame(inventoryframe)
    inv_treeviewframe.pack(fill=BOTH, expand=1)
    inv_treeviewframe.place(x=0, y=0, width=1500, height=1500)
    scrollbarY = Scrollbar(inventoryframe, orient='vertical')

    header = ttk.Treeview(inventoryframe,
                          columns=('id', 'InventoryID', 'ItemName', 'Description', 'Unit_Price', 'reorderlevel', 'qty'),
                           yscrollcommand=scrollbarY.set,height=12)


    scrollbarY.config(command=header.yview)
    scrollbarY.pack(side='right', fill=Y)
    header.pack(fill=BOTH, expand=1)

    header.config(show='headings')
    header.heading('id', text='')
    header.heading('InventoryID', text='Category')
    header.heading('ItemName', text='Item Name')
    header.heading('Description', text='Description')
    header.heading('Unit_Price', text='Unit Price')
    header.heading('reorderlevel', text='Reorder Level')
    header.heading('qty', text='Quantity')

    header.bind('<Double-1>', on_treeview_double_click)
    fetch_data()

    for col in header['columns']:
        header.column(col, width=125, anchor='center', stretch=False)
    header.column('id', width=0, stretch=False)

    # Convert to Excel Button
    convertbutton = CTkButton(inventoryRecord, text="CONVERT TO EXCEL", command=export_to_excel,width=195,
                              height=60, font=("arial", 14, 'bold'), border_width=2, border_color='white',
                              fg_color="#f2b62a", hover_color='#729762', bg_color='#303030', text_color='black')
    convertbutton.place(x=870, y=570)


    deletebutton = CTkButton(inventoryRecord, text="DELETE", width=195,command=delete_button,
                             height=60, font=("arial", 14, 'bold'), border_width=2, border_color='white',
                             fg_color="#f2b62a", hover_color='#729762', bg_color='#303030', text_color='black')
    deletebutton.place(x=662, y=570)

    updatebutton = CTkButton(inventoryRecord, text="UPDATE", width=195, command=update_stock,
                             height=60, font=("arial", 14, 'bold'), border_width=2, border_color='white',
                             fg_color="#f2b62a", hover_color='#729762', bg_color='#303030', text_color='black')
    updatebutton.place(x=455, y=570)


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
    def read_rfid_continuous():
        try:
            with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
                rfidinfoentry.configure(state="normal")
                rfidinfoentry.delete(0, ctk.END)
                rfidinfoentry.insert(0, "Waiting for RFID card...")
                rfidinfoentry.configure(state="readonly")

                while True:
                    if ser.in_waiting:
                        rfid_data = ser.readline().decode('utf-8').strip()
                        if rfid_data:
                            rfidinfoentry.configure(state="normal")
                            rfidinfoentry.delete(0, ctk.END)
                            rfidinfoentry.insert(0, rfid_data)
                            rfidinfoentry.configure(state="readonly")
                            break  # Stop after reading once
                    time.sleep(0.1)
        except Exception as e:
            rfidinfoentry.configure(state="normal")
            rfidinfoentry.delete(0, ctk.END)
            rfidinfoentry.insert(0, f"Error: {e}")
            rfidinfoentry.configure(state="readonly")

    # Start the RFID thread
    def start_read_rfid_thread():
        threading.Thread(target=read_rfid_continuous, daemon=True).start()


    # Window for entering pet/owner's info
    addpet_window = CTkToplevel(window)
    addpet_window.title("PET REMARKS & DIAGNOSIS")
    addpet_window.resizable(False, False)
    addpet_window.grab_set()
    addpet_window.geometry('870x400+330+380')

    addpetBG = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\rfidremarks.jpg'), size=(900, 400))
    addpetBGlabel = CTkLabel(addpet_window, image=addpetBG, text='')
    addpetBGlabel.place(x=0, y=0)

    # Entry fields for RFID and Diagnosis
    rfidinfoentry = CTkEntry(addpet_window, font=('Arial', 15, 'italic'), width=150, border_color='black')
    rfidinfoentry.place(x=548, y=89)
    rfidinfoentry.insert(0, "Scan RFID Card")
    #rfidinfoentry.configure(state="readonly")
    read_button = CTkButton(addpet_window, text="Scan RFID", command=start_read_rfid_thread,width=95,border_width=2, border_color='#1A5319', fg_color="#387478",
                             hover_color='#729762')
    read_button.place(x=705, y=89)

    diagnosisentry = CTkTextbox(addpet_window, font=('Arial', 12, 'italic'), width=337, height=142,
                                border_color='black', border_width=2)
    diagnosisentry.place(x=435, y=171)

    submitbutton = CTkButton(addpet_window, text='SUBMIT', font=("Arial", 16, 'bold'), border_width=2, border_color='#1A5319', fg_color="#387478",
                             hover_color='#729762', width=200, height=40, command=add_data)
    submitbutton.place(x=600, y=345)


#------------------------------------------------------------------------------------------------------------------
#DATABASE (FUNCTION)
def connect_database():
    def connect():
        global con, mycursor
        if hostentry.get() == '' or userentry.get() == '' or passwentry.get() == '':
            messagebox.showwarning('Error','Field Cannot be Empty',parent=connectwindow)
            return
        try:
            con = pymysql.connect(
                host=hostentry.get(),
                user=userentry.get(),
                password=passwentry.get(),
                database='vetclinicmanagementsystemnew'  # Optional if not needed yet
            )
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Connection is successful', parent=connectwindow)

            # Enable buttons after successful connection
            addpetinfo.configure(state=NORMAL)
            viewreport.configure(state=NORMAL)
            exportbutton.configure(state=NORMAL)
            view_button.configure(state=NORMAL)
            add_petdiagnosis.configure(state=NORMAL)
            searchbutton.configure(state=NORMAL)
            deletebutton.configure(state=NORMAL)
            addstaffinfo.configure(state=NORMAL)
            updatebutton.configure(state=NORMAL)
            inventoryrecord.configure(state=NORMAL)
            staffinfo.configure(state=NORMAL)
            connectwindow.destroy()
        except Exception as e:
            if "caching_sha2_password" in str(e) or "cryptography" in str(e).lower():
                messagebox.showwarning("No User Found", "Please check your username or password", parent=connectwindow)
            else:
                messagebox.showerror("Error", f"Invalid Details\n{e}", parent=connectwindow)

    connectwindow = CTkToplevel(window)
    connectwindow.geometry('390x350+730+230')
    connectwindow.title('Database Connection')
    connectwindow.grab_set()

    databaseBGpicture= CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\logo\database-management.png'), size=(80, 80))
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
    addnewEmployee.geometry('750x680+500+90')
    addnewEmployee.title("EMPLOYEE INFORMATION")
    addnewEmployee.resizable(False, False)
    addnewEmployee.grab_set()

    employeeBG = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\employeeBG.jpg'), size=(750, 750))
    employeeBGlabel = CTkLabel(addnewEmployee, image=employeeBG, text='')
    employeeBGlabel.place(x=0, y=0)

    # FULL NAME
    fullnameentry = CTkEntry(addnewEmployee, font=('Arial', 15), width=300, bg_color='white', height=28,
                             corner_radius=-1, border_color='black')
    fullnameentry.place(x=28, y=135)

    # AGE
    ageentry = CTkEntry(addnewEmployee, font=('Arial', 15), width=140, bg_color='white', height=28, corner_radius=-1,
                        border_color='black')
    ageentry.place(x=417, y=272)

    # ADDRESS
    addressentry = CTkEntry(addnewEmployee, font=('Arial', 15), width=528, bg_color='white', height=28,
                            corner_radius=-1, border_color='black')
    addressentry.place(x=28, y=201)

    # PHONE NUMBER
    phonenumberentry = CTkEntry(addnewEmployee, font=('Arial', 15), width=250, placeholder_text="09XX-XXX-XXXX",
                                bg_color='white', height=28, corner_radius=-1, border_color='black')
    phonenumberentry.place(x=28, y=272)

    # GENDER
    genderChoices = ['Male', 'Female']
    dropdownGender = ctk.CTkComboBox(addnewEmployee, values=genderChoices, bg_color='white', height=28,
                                     corner_radius=-1, border_color='black')
    dropdownGender.place(x=417, y=340)
    dropdownGender.set('Select an option')

    # TIN
    TINentry = CTkEntry(addnewEmployee, font=('Arial', 15), width=250, bg_color='white', height=28, corner_radius=-1,
                        border_color='black', placeholder_text="XXX-XXX-XXX")
    TINentry.place(x=28, y=340)

    # SSS
    SSSentry = CTkEntry(addnewEmployee, font=('Arial', 15), width=250, bg_color='white', height=28, corner_radius=-1,
                        border_color='black', placeholder_text="XX-XXXXXXX-X")
    SSSentry.place(x=28, y=409)

    # PAG-IBIG
    PAG_IBIGentry = CTkEntry(addnewEmployee, font=('Arial', 15), width=250, bg_color='white', height=28,
                             corner_radius=-1, border_color='black', placeholder_text="XXXXXXXXXXXX")
    PAG_IBIGentry.place(x=28, y=477)

    # BIRTHDATE
    birthdateentry = CTkEntry(addnewEmployee, font=('Arial', 15), width=140, bg_color='white', height=28,
                              corner_radius=-1, border_color='black', placeholder_text="Month / Day / Year")
    birthdateentry.place(x=417, y=409)

    # SUBMIT BUTTON
    SubmitButton = CTkButton(addnewEmployee, text='SUBMIT', font=("Arial", 15, 'bold'), compound='right',
                             text_color='black', corner_radius=-1, hover_color='#83c7ac', fg_color='#faf3cd',
                             border_color='#16423C', border_width=1, width=180, height=50, command=Submit)
    SubmitButton.place(x=417, y=465)
#------------------------------------------------------------------------------------------------------------------
#VIEW EMPLOYEE (FUNCTION)

header_columns_map = {
    'fullName': 'Full Name',
    'age': 'Age',
    'fullAddress': 'Full Address',
    'phoneNum': 'Phone Number',
    'gender': 'Gender',
    'tinNum': 'TIN Number',
    'sssNum': 'SSS Number',
    'pagibigNum': 'Pag-Ibig Number',
    'birthDate': 'Birthday'
}

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
            messagebox.showinfo('Success', f'Employee {edit_fullnameentry.get()} is edited successfully',parent=employeeRecord)
            edit_addnewEmployee.destroy()

            fetch_employeedata()

        edit_addnewEmployee = CTkToplevel(employeeRecord)
        edit_addnewEmployee.geometry('750x680+500+90')
        edit_addnewEmployee.title("EDIT EMPLOYEE INFORMATION")
        edit_addnewEmployee.resizable(False, False)
        edit_addnewEmployee.grab_set()

        employeeBG = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\editemployeerecord.jpg'), size=(750, 750))
        employeeBGlabel = CTkLabel(edit_addnewEmployee, image=employeeBG, text='')
        employeeBGlabel.place(x=0, y=0)

        # FULL NAME
        edit_fullnameentry = CTkEntry(edit_addnewEmployee, font=('Arial', 15), width=300, bg_color='white', height=28,corner_radius=-1, border_color='black')
        edit_fullnameentry.place(x=28, y=135)

        # AGE
        edit_ageentry = CTkEntry(edit_addnewEmployee, font=('Arial', 15), width=140, bg_color='white', height=28,corner_radius=-1,border_color='black')
        edit_ageentry.place(x=417, y=272)

        # ADDRESS
        edit_addressentry = CTkEntry(edit_addnewEmployee, font=('Arial', 15), width=528, bg_color='white', height=28,corner_radius=-1, border_color='black')
        edit_addressentry.place(x=28, y=201)

        # PHONE NUMBER
        edit_phonenumberentry = CTkEntry(edit_addnewEmployee, font=('Arial', 15), width=250, placeholder_text="09XX-XXX-XXXX",bg_color='white', height=28, corner_radius=-1, border_color='black')
        edit_phonenumberentry.place(x=28, y=272)

        # GENDER
        edit_genderChoices = ['Male', 'Female']
        edit_dropdownGender = ctk.CTkComboBox(edit_addnewEmployee, values=edit_genderChoices, bg_color='white', height=28,corner_radius=-1, border_color='black')
        edit_dropdownGender.place(x=417, y=340)
        edit_dropdownGender.set('Select an option')

        # TIN
        edit_TINentry = CTkEntry(edit_addnewEmployee, font=('Arial', 15), width=250, bg_color='white', height=28,corner_radius=-1,border_color='black', placeholder_text="XXX-XXX-XXX")
        edit_TINentry.place(x=28, y=340)
        # SSS
        edit_SSSentry = CTkEntry(edit_addnewEmployee, font=('Arial', 15), width=250, bg_color='white', height=28,corner_radius=-1,border_color='black', placeholder_text="XX-XXXXXXX-X")
        edit_SSSentry.place(x=28, y=409)
        # PAG-IBIG
        edit_PAG_IBIGentry = CTkEntry(edit_addnewEmployee, font=('Arial', 15), width=250, bg_color='white', height=28,corner_radius=-1, border_color='black', placeholder_text="XXXXXXXXXXXX")
        edit_PAG_IBIGentry.place(x=28, y=477)
        # BIRTHDATE
        edit_birthdateentry = CTkEntry(edit_addnewEmployee, font=('Arial', 15), width=140, bg_color='white', height=28,corner_radius=-1, border_color='black', placeholder_text="MM/DD/YYYY")
        edit_birthdateentry.place(x=417, y=409)

        # SUBMIT BUTTON
        edit_SubmitButton = CTkButton(edit_addnewEmployee,  text='SUBMIT', font=("Arial", 15, 'bold'), compound='right',
                             text_color='black', corner_radius=-1, hover_color='#83c7ac', fg_color='#faf3cd',
                             border_color='#16423C', border_width=1, width=180, height=50, command=save_data)
        edit_SubmitButton.place(x=417, y=465)

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

    def open_employee_details(data):
        details_window = CTkToplevel(employeeRecord)
        details_window.geometry("650x500+600+200")
        details_window.title("EMPLOYEE FULL DETAILS")
        details_window.resizable(False, False)
        details_window.grab_set()

        full_employeeBG = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\fullemployeeinformation.jpg'), size=(650, 500))
        full_employeeBGlabel = CTkLabel(details_window, image=full_employeeBG, text='')
        full_employeeBGlabel.place(x=0, y=0)

        # Full Name
        CTkLabel(details_window, text=data[1], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=125,y=130)
        # Age
        CTkLabel(details_window, text=data[2], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=420,y=130)
        # Full Address
        CTkLabel(details_window, text=data[3], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=125,y=185)
        # Phone Number
        CTkLabel(details_window, text=data[4], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=260,y=237)
        # Gender
        CTkLabel(details_window, text=data[5], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=100,y=237)
        # TIN Number
        CTkLabel(details_window, text=data[6], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=190,y=269)
        # SSS Number
        CTkLabel(details_window, text=data[7], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=190,y=295)
        # Pag-IBIG Number
        CTkLabel(details_window, text=data[8], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=190,y=325)
        # Birthday
        CTkLabel(details_window, text=data[9], font=('Arial', 14), text_color='#54321A', bg_color='white').place(x=470,y=237)

    def on_row_double_click(event):
        selected_item = header.focus()
        if not selected_item:
            return
        data = header.item(selected_item)['values']
        if data:
            open_employee_details(data)

    employeeRecord = CTkToplevel(window)
    employeeRecord.geometry('500x500+500+95')
    employeeRecord.title("EMPLOYEE RECORD")
    employeeRecord.resizable(False, False)
    employeeRecord.grab_set()

    view_employeeBG = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\employee_list.jpg'), size=(500, 500))
    view_employeeBGlabel = CTkLabel(employeeRecord, image=view_employeeBG, text='')
    view_employeeBGlabel.place(x=0, y=0)


    treeviewframe = Frame(employeeRecord)
    treeviewframe.pack(fill=BOTH, expand=1)
    treeviewframe.place(x=20, y=60, width=568, height=420)
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
    header.bind("<Double-1>", on_row_double_click)

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

    view_button = CTkButton(employeeRecord, text="UPDATE RECORD", command=update_employee_window,font=("Arial", 15, 'bold'), compound='right',
                             text_color='black', corner_radius=-1, hover_color='#83c7ac', fg_color='#faf3cd',
                             border_color='#16423C', border_width=1, width=180, height=50)
    view_button.place(x=220, y=400)

    delete_button = CTkButton(employeeRecord, text="DELETE RECORD",font=("Arial", 15, 'bold'), compound='right',
                             text_color='black', corner_radius=-1, hover_color='#83c7ac', fg_color='#faf3cd',
                             border_color='#16423C', border_width=1, width=180, height=50, command=delete_employeedata)
    delete_button.place(x=15, y=400)

def fetch_events_for_selected_date():
    event_listbox.delete(0, tk.END)  # Clear current list

    raw_date = cal.get_date()  # Get date from calendar
    print(f"[DEBUG] Raw date from calendar: {raw_date}")

    try:
        selected_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
    except ValueError:
        try:
            selected_date = datetime.strptime(raw_date, "%m/%d/%y").date()
        except ValueError:
            messagebox.showerror("Date Error", "Unrecognized date format from calendar.")
            return

    print(f"[DEBUG] Parsed selected date: {selected_date}")

    try:
        conn = connect_db()
        cursor = conn.cursor()

        fetch_query = "SELECT event_description FROM events WHERE event_date = %s"
        cursor.execute(fetch_query, (str(selected_date),))
        events = cursor.fetchall()

        print(f"[DEBUG] Events fetched from DB: {events}")

        for event in events:
            event_listbox.insert(tk.END, event[0])

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch events:\n{e}")

def delete_events():
    selected_date = cal.get_date()
    selected_event = event_listbox.get(tk.ACTIVE)  # Get selected event in the Listbox

    if not selected_event:
        messagebox.showwarning("No Selection", "Please select an event to delete.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Delete the event with matching date and description
        delete_query = "DELETE FROM events WHERE event_date = %s AND event_description = %s"
        cursor.execute(delete_query, (selected_date, selected_event))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Event deleted successfully.")
        else:
            messagebox.showwarning("Not Found", "Event not found in database.")

        cursor.close()
        conn.close()

        fetch_events_for_selected_date()  # Refresh list after deletion

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


def show_event_details(event):
    try:
        # Get the selected item
        selection = event_listbox.curselection()
        if not selection:
            return
        selected_text = event_listbox.get(selection[0])

        # Assume event description is shown, so query the DB to get full details
        selected_date = cal.get_date()

        cursor = conn.cursor()
        query = "SELECT event_description FROM events WHERE event_date = %s AND event_description = %s"
        cursor.execute(query, (selected_date, selected_text))
        result = cursor.fetchone()

        if result:
            full_description = result[0]

            # Create the new popup window
            detail_win = CTkToplevel(window)
            detail_win.title("Appointment Details")
            detail_win.geometry("400x400+800+400")
            detail_win.grab_set()

            detailimage = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\todo.jpg'), size=(400,400))
            detailimageLabel = CTkLabel(detail_win, image=detailimage, text='')
            detailimageLabel.place(x=0, y=0)


            CTkLabel(detail_win, text=selected_date,font=('Arial', 18, 'bold'), text_color='Red', fg_color='#ffffe3').place(x=150,y=120)


            # Format the description to wrap after every 10 words
            def wrap_text_by_words(text, words_per_line=10):
                words = text.split()
                lines = [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]
                return '\n'.join(lines)

            wrapped_description = wrap_text_by_words(full_description)

            CTkLabel(detail_win, text=wrapped_description,font=('Arial', 18), fg_color='#ffffe3', justify="left").place(x=90,y=180)

        else:
            messagebox.showinfo("Not Found", "Event details could not be found.")

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch event details.\n{e}")





#------------------------------------------------------------------------------------------------------------------
#BACKGROUND (MAIN)
bgpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\main_background.jpg'), size=(1510, 694))
bgpicturelabel = CTkLabel(window, image=bgpicture, text='')
bgpicturelabel.place(x=0, y=0)
#------------------------------------------------------------------------------------------------------------------
#CLOCK (FUNCTION)
count=0
text=''

def clock():
    timex=strftime(' %I:%M:%S')
    date=strftime('   %B %d, %Y')
    currentimelabel.configure(text=f'{date}\n Time: {timex}',font=('times new roman',21,'bold'),bg_color='#c8d9bd')
    currentimelabel.after(1000,clock)

currentimelabel=CTkLabel(window)
currentimelabel.place(x=1340,y=8)
clock()
#------------------------------------------------------------------------------------------------------------------
#VIEW EMPLOYEE (FUNCTION)
#MAIN WINDOW
#slider
style = ttk.Style()
style.theme_use("clearlooks")
style.configure("Treeview",background='white',rowheight=35,fieldbackground='white')
style.map('Treeview',background=[('selected','#387478')]) #selected row

treeviewframe = Frame(window)
treeviewframe.place(x=320, y=150, width=825, height=600)
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
information.heading('RFID_Number', text='RFID NUMBER')
information.heading('Name', text="OWNER'S NAME")
information.heading('Address', text='ADDRESS')
information.heading('cnum', text='CONTACT NUMBER')
information.heading('emailadd', text='EMAIL ADDRESS')
information.heading('Petname', text="PET'S NAME")
information.heading('Pet_age', text="PET'S AGE")
information.heading('Petgender', text="PET'S GENDER")
information.heading('Breed', text='BREED')
information.heading('Species', text='SPECIES')

for col in information['columns']:
    information.column(col, width=150, anchor='center', stretch=False)


leftside = CTkFrame(window,width=250,height=800,fg_color='#C1D8C3')     
leftside.place(x=0,y=0)
#------------------------------------------------------------------------------------------------------------------
#LEFT SIDE BUTTON
adminpic = CTkImage(light_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\lakeview.jpg'),size = (253,120))
helloadmin=CTkLabel(window,text="",image=adminpic)
helloadmin.place(x=0,y=0)

#------------------------------------------------------------------------------------------------------------------
#PET CARE TAB
addpetpic = CTkImage(light_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\logo\kitten.png'),size = (35,35))

petinfotabtext=CTkLabel(window,text=" PET CARE TAB",fg_color='#C1D8C3',image=addpetpic,compound='left',font=('times new roman',17,'bold'),text_color='#1A5319')
petinfotabtext.place(x=0,y=130)
addpetinfo=CTkButton(window,text='Add New Records',command=addpetinfo,state=DISABLED,width=250,height=50,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
addpetinfo.place(x=0,y=173)
add_petdiagnosis=CTkButton(window,text="Pet's Assesment",command=add_petdiagnosis,state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
add_petdiagnosis.place(x=0,y=212)
viewreport=CTkButton(window,text="Client's Directory",state=DISABLED,command=show_data,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
viewreport.place(x=0,y=251)
exportbutton = CTkButton(window,text='Export to Excel',state=DISABLED,command=export_data,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
exportbutton.place(x=0,y=290)

#------------------------------------------------------------------------------------------------------------------
#EMPLOYEE / STAFF TAB
staffpic = CTkImage(light_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\logo\staff.png'),size = (35,35))

employeetext=CTkLabel(window,text=" EMPLOYEE/STAFF",fg_color='#C1D8C3',image=staffpic,compound='left',font=('times new roman',17,'bold'),text_color='#1A5319')
employeetext.place(x=0,y=344)
addstaffinfo=CTkButton(window,text='Add New Employee',state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),command=addnewEmployee,border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
addstaffinfo.place(x=0,y=383)

staffinfo=CTkButton(window,text='View Employee Record',state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762',command=view_employeeRecord)
staffinfo.place(x=0,y=425)

#------------------------------------------------------------------------------------------------------------------
# INVENTORY TAB

inventorypic = CTkImage(light_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\logo\inventory.png'),size = (35,35))

inventorytext=CTkLabel(window,text=" INVENTORY SECTION",fg_color='#C1D8C3',image=inventorypic,compound='left',font=('times new roman',17,'bold'),text_color='#1A5319')
inventorytext.place(x=0,y=474)

inventoryrecord=CTkButton(window,text='Stock Ordering',command= inventory_section,state=DISABLED,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
inventoryrecord.place(x=0,y=515)
#------------------------------------------------------------------------------------------------------------------

# SERVER MANAGER TAB
managementpic = CTkImage(light_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\logo\management.png'),size = (35,35))
servertext=CTkLabel(window,text=" SERVER CONNECTION",fg_color='#C1D8C3',image=managementpic,compound='left',font=('times new roman',17,'bold'),text_color='#1A5319')
servertext.place(x=0,y=565)

connectbutton=CTkButton(window,text='Connect',command=connect_database,width=250,height=45,corner_radius=0,font=("arial",14,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
connectbutton.place(x=0,y=608)
logoutbutton = CTkButton(window,text='Log Out',width=250,height=45,corner_radius=0,font=("arial",14,'bold'),command=log_out,border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
logoutbutton.place(x=0,y=650)
#------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------
searchentry = CTkEntry(window,placeholder_text="Search Owner's Name",width=180)
searchentry.place(x=570,y=80)
searchbutton = CTkButton(window,text='Search',state=DISABLED,command=search_data,width=150,border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
searchbutton.place(x=765,y=80)
#------------------------------------------------------------------------------------------------------------------
updatebutton = CTkButton(window,text='Update',state=DISABLED,command=update_button,width=180,height=40,font=("arial",16,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
updatebutton.place(x=680,y=630)
#------------------------------------------------------------------------------------------------------------------
deletebutton = CTkButton(window,text='Delete',state=DISABLED,command=delete_data,width=180,height=40,font=("arial",16,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
deletebutton.place(x=490,y=630)
#------------------------------------------------------------------------------------------------------------------

view_button = CTkButton(window, text="View", command=show_pet_details,state=DISABLED,width=180,height=40,font=("arial",16,'bold'),border_width=2,border_color='#1A5319',fg_color="#387478",hover_color='#729762')
view_button.place(x=300,y=630)
#------------------------------------------------------------------------------------------------------------------
#CALENDAR ADD MEETING
conn = connect_db()
if conn is None:
    print("Unable to connect to the database.")
    window.quit()

# Calendar widget
cal = Calendar(window, selectmode='day', date_pattern="yyyy-mm-dd",font=("Arial", 23,'italic'),showweeknumbers=False,showothermonthdays=False,background = '#abb9a0',selectbackground = '#9c6436')
cal.place(x=1170,y=184)

# Highlight existing event dates on calendar load
highlight_existing_event_dates()

# Event entry
event_entry =  CTkEntry(window, width=230,height=40,placeholder_text="Add Appointment Here",bg_color='#ffffe3')
event_entry.place(x=960,y=570)

# Add event button
add_event_btn = CTkButton(window, text="Add", bg_color='#ffffe3',command=add_event,width=110,height=35,border_width=2,font=("arial",15,'bold'),border_color='#1A5319',fg_color="#387478",hover_color='#729762')
add_event_btn.place(x=960,y=615)

delete_event_btn = CTkButton(window, text="Delete",bg_color='#ffffe3', command=delete_events,width=110,height=35,border_width=2,font=("arial",14,'bold'),border_color='#1A5319',fg_color="#387478",hover_color='#729762')
delete_event_btn.place(x=1080,y=615)

# Listbox to display events for selected date
event_listbox = tk.Listbox(window, width=26, height=7,font=('arial',16,'italic'))
event_listbox.place(x=1531,y=631)
event_entry =  CTkEntry(window, width=230,height=40,placeholder_text="Add Appointment Here",bg_color='#ffffe3')
event_entry.place(x=960,y=570)

# Add event button
add_event_btn = CTkButton(window, text="Add", bg_color='#ffffe3',command=add_event,width=110,height=35,border_width=2,font=("arial",15,'bold'),border_color='#1A5319',fg_color="#387478",hover_color='#729762')
add_event_btn.place(x=960,y=615)

delete_event_btn = CTkButton(window, text="Delete",bg_color='#ffffe3', command=delete_events,width=110,height=35,border_width=2,font=("arial",14,'bold'),border_color='#1A5319',fg_color="#387478",hover_color='#729762')
delete_event_btn.place(x=1080,y=615)

# Listbox to display events for selected date
event_listbox = tk.Listbox(window, width=26, height=7,font=('arial',16,'italic'))
event_listbox.bind("<Double-1>", show_event_details)
event_listbox.place(x=1531,y=631)



cal.bind("<<CalendarSelected>>", on_date_select)


window.mainloop()
if conn and conn.is_connected():
    conn.close()