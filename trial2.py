from tkinter import Frame, Scrollbar
from tkinter import *
from customtkinter import *
from tkinter import messagebox, ttk, filedialog
import pymysql
import pandas

window = CTk()
window.geometry('1500x500')

# Global connection variables
mycursor = None
con = None

# Function to show all pet data in the treeview
def show_data():
    if mycursor:
        query = 'SELECT * FROM tb_customerinfo'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        information.delete(*information.get_children())  # Clear existing data
        for data in fetched_data:
            information.insert('', END, values=data)  # Insert each row into the treeview

# Function to show details of selected pet
def show_pet_details():
    selected_item = information.focus()
    if selected_item:
        values = information.item(selected_item, 'values')

        if values:
            # Create a new Toplevel window to show pet details
            details_window = CTkToplevel(window)
            details_window.title("Pet/Owner Details")
            details_window.geometry('500x400')
            details_window.grab_set()

            labels = ['I.D', 'RFID Number', 'Name', 'Address', 'Contact Number', 'Email address',
                      "Pet's Name", "Pet's Age", "Pet's Gender", 'Breed', 'Species']

            # Display the main pet details inside the Toplevel window
            for i, value in enumerate(values):
                if i < len(labels):
                    title_label = CTkLabel(details_window, text=f"{labels[i]}:", font=('Arial', 20, 'bold'), text_color='Red')
                    title_label.grid(row=i, column=0, sticky="w", padx=0, pady=5)

                    value_label = CTkLabel(details_window, text=value, font=('Arial', 18, 'italic'), text_color='Black')
                    value_label.grid(row=i, column=1, sticky="w", padx=0, pady=5)

            # Diagnosis and Date Table Section
            diagnosis_frame = CTkFrame(details_window, width=380, height=200)
            diagnosis_frame.grid(row=len(values), column=0, columnspan=2, pady=10)

            diagnosis_label = CTkLabel(diagnosis_frame, text="Diagnosis History:", font=('Arial', 18, 'bold'))
            diagnosis_label.grid(row=0, column=0, sticky="w")

            # Scrollable Table
            diagnosis_table_frame = Frame(diagnosis_frame)
            diagnosis_table_frame.grid(row=1, column=0, columnspan=2)

            scroll_y = Scrollbar(diagnosis_table_frame, orient=VERTICAL)

            diagnosis_table = ttk.Treeview(diagnosis_table_frame, columns=("date", "diagnosis"), show='headings',
                                           yscrollcommand=scroll_y.set, height=5)

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
def export_data():
    # Ask user for a save location
    url = filedialog.asksaveasfilename(defaultextension='.csv')

    # Fetch data by joining both tables based on RFID_Number
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

    # Create a list of column names for the CSV file
    columns = ['I.D', 'RFID Number', 'Name', 'Address', 'Contact Number', 'Email address',
               "Pet's Name", "Pet's Age", "Pet's Gender", 'Breed', 'Species', 'Date', 'Diagnosis']

    # Convert the fetched data to a pandas DataFrame
    table = pandas.DataFrame(fetched_data, columns=columns)

    # Save the data as a CSV file
    table.to_csv(url, index=False)

    # Display success message
    messagebox.showinfo('Success', 'Data is saved successfully')



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

#DONE
# Treeview and Layout Setup for Main Window
treeviewframe = Frame(window)
treeviewframe.place(x=15, y=0, width=500, height=400)
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
information.heading('cnum', text='Contact Number')
information.heading('emailadd', text='Email Address')
information.heading('Petname', text="Pet's Name")
information.heading('Pet_age', text="Pet's Age")
information.heading('Petgender', text="Pet's Gender")
information.heading('Breed', text='Breed')
information.heading('Species', text='Species')

# Connect Database Button
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


        add_petdiagnosis.configure(state=NORMAL)
        viewreport.configure(state=NORMAL)
        exportbutton.configure(state=NORMAL)
        view_button.configure(state=NORMAL)


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
    submitbutton.place(x=300, y=200)




#done
connectbutton = CTkButton(window, text='Connect to Database', command=connect_database)
connectbutton.place(x=530, y=20)

details_frame = CTkFrame(window, width=900, height=400)
details_frame.place(x=530, y=800)
#done
viewreport=CTkButton(window,text='VIEW ALL DATA',state=DISABLED,width=30,command=show_data)
viewreport.place(x=1200,y=400)
#done
exportbutton = CTkButton(window,text='Export Data',state=DISABLED,command=export_data,width=30)
exportbutton.place(x=600,y=400)
#done
add_petdiagnosis=CTkButton(window,text='Add PET DIAGNOSIS ',state=DISABLED,command=add_petdiagnosis)
add_petdiagnosis.place(x=400,y=400)

view_button = CTkButton(window, text="View Pet Details",state=DISABLED, command=show_pet_details,width=180,height=40,font=("arial",16,'bold'))
view_button.place(x=100,y=400)


# Show data when the window starts
window.after(100, show_data)  # Show data after the connection is made

window.mainloop()
