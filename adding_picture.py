from tkinter import filedialog, messagebox, Scrollbar, Frame, VERTICAL, RIGHT, Y, BOTH, END
import customtkinter as ctk
from PIL import Image, ImageTk
import os

def show_pet_details():
    selected_item = information.focus()
    if selected_item:
        values = information.item(selected_item, 'values')

        if values:
            #TOPLEVEL FOR PET DETAILS
            details_window = ctk.CTkToplevel(window)
            details_window.title("Pet/Owner Details")
            details_window.geometry('900x800')
            details_window.resizable(False, False)
            details_window.grab_set()

            labels = ['I.D', 'RFID Number', 'Name', 'Address', 'Contact Number', 'Email address',
                      "Pet's Name", "Pet's Age", "Pet's Gender", 'Breed', 'Species', 'Image Path']  # Adding Image Path label

            # PET DETAIL DISPLAY INSIDE TOPLEVEL
            for i, value in enumerate(values):
                if i < len(labels) - 1:  # Skip Image Path for now (will handle it separately)
                    title_label = ctk.CTkLabel(details_window, text=f"{labels[i]}:", font=('Arial', 20, 'bold'),
                                               text_color='Red')
                    title_label.grid(row=i, column=0, sticky="w", padx=0, pady=5)

                    value_label = ctk.CTkLabel(details_window, text=value, font=('Arial', 18, 'italic'),
                                               text_color='Black')
                    value_label.grid(row=i, column=1, sticky="w", padx=0, pady=5)

            # Image Section
            if values[-1]:  # Assuming the last value contains the image path
                image_path = values[-1]
                if os.path.exists(image_path):  # Check if the image path exists
                    pet_image = Image.open(image_path)
                    pet_image = pet_image.resize((300, 300), Image.Resampling.LANCZOS)  # Resize for display
                    pet_image_tk = ImageTk.PhotoImage(pet_image)

                    # Create an image label to display the pet's image
                    image_label = ctk.CTkLabel(details_window, image=pet_image_tk, text="")
                    image_label.image = pet_image_tk  # Keep a reference to prevent garbage collection
                    image_label.grid(row=0, column=2, rowspan=10, padx=20, pady=5)  # Adjust row, column as needed
                else:
                    messagebox.showwarning("Image Not Found", "Image file not found. Please check the image path.")

            # Diagnosis and Date Table Section
            diagnosis_frame = ctk.CTkFrame(details_window, width=50, height=900)
            diagnosis_frame.place(x=400, y=0)

            diagnosis_label = ctk.CTkLabel(diagnosis_frame, text="Diagnosis History:", font=('Arial', 18, 'bold'))
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
                        full_diagnosis_window = ctk.CTkToplevel(details_window)
                        full_diagnosis_window.title("Full Diagnosis Details")
                        full_diagnosis_window.geometry('500x300')
                        full_diagnosis_window.grab_set()

                        # Display full diagnosis text
                        date_label = ctk.CTkLabel(full_diagnosis_window, text=f"Date: {diag_values[0]}",
                                                  font=('Arial', 18, 'bold'), text_color='Red')
                        date_label.pack(pady=10)

                        diagnosis_label = ctk.CTkLabel(full_diagnosis_window, text=f"Diagnosis: {diag_values[1]}",
                                                       font=('Arial', 18, 'italic'), text_color='Black',
                                                       wraplength=450)
                        diagnosis_label.pack(pady=10)

            # Bind the double-click event to the diagnosis table
            diagnosis_table.bind("<Double-1>", on_double_click)
