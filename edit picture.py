import tkinter as tk
from tkinter import ttk


def show_pet_details():
    # Get selected row data
    selected_item = petinfotable.focus()  # Get the selected item
    if selected_item:
        values = petinfotable.item(selected_item, 'values')

        # Create a new window (or frame)
        details_window = tk.Toplevel(root)
        details_window.title("Pet Details")

        # Display the pet information in the new window
        labels = ['I.D', "Parent's Name", "Pet's Name", 'Type of Species', 'Type of Breed', 'Age', 'Diagnosis', 'Date']
        for i, value in enumerate(values):
            label = tk.Label(details_window, text=f"{labels[i]}: {value}")
            label.pack(anchor="w", padx=10, pady=5)


root = tk.Tk()
root.geometry("800x600")

highFrame = tk.Frame(root)
highFrame.pack(fill=tk.BOTH, expand=1)

scrollbarX = tk.Scrollbar(highFrame, orient=tk.HORIZONTAL)
scrollbarY = tk.Scrollbar(highFrame, orient=tk.VERTICAL)

petinfotable = ttk.Treeview(highFrame,
                            columns=('ID', 'parentname', "petname", 'species', 'breed', 'age', 'diagnosis', 'date'),
                            xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set)

scrollbarX.config(command=petinfotable.xview)
scrollbarY.config(command=petinfotable.yview)
scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)
scrollbarY.pack(side=tk.RIGHT, fill=tk.Y)
petinfotable.pack(fill=tk.BOTH, expand=1)

petinfotable.heading('ID', text='I.D')
petinfotable.heading('parentname', text="Parent's Name")
petinfotable.heading('petname', text="Pet's Name")
petinfotable.heading('species', text='Type of Species')
petinfotable.heading('breed', text='Type of Breed')
petinfotable.heading('age', text='AGE')
petinfotable.heading('diagnosis', text='Diagnosis')
petinfotable.heading('date', text='Date')

petinfotable.config(show="headings")

# Add dummy data for testing
petinfotable.insert('', 'end',
                    values=('001', 'John Doe', 'Fluffy', 'Dog', 'Golden Retriever', '5', 'Healthy', '2024-01-01'))

# Button to view details
view_button = tk.Button(root, text="View Pet Details", command=show_pet_details)
view_button.pack(pady=10)

root.mainloop()