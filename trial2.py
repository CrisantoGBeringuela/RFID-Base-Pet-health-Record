import customtkinter as ctk
import serial
import threading
import time

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Set your Arduino COM port and baud rate
arduino_port = 'COM3'  # Change to the actual port (e.g., 'COM4')
baud_rate = 9600

# Continuous RFID reading function
def read_rfid_continuous():
    try:
        with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
            rfid_entry.configure(state="normal")
            rfid_entry.delete(0, ctk.END)
            rfid_entry.insert(0, "Waiting for RFID card...")
            rfid_entry.configure(state="readonly")

            while True:
                if ser.in_waiting:
                    rfid_data = ser.readline().decode('utf-8').strip()
                    if rfid_data:
                        rfid_entry.configure(state="normal")
                        rfid_entry.delete(0, ctk.END)
                        rfid_entry.insert(0, rfid_data)
                        rfid_entry.configure(state="readonly")
                        break  # Stop after reading once
                time.sleep(0.1)
    except Exception as e:
        rfid_entry.configure(state="normal")
        rfid_entry.delete(0, ctk.END)
        rfid_entry.insert(0, f"Error: {e}")
        rfid_entry.configure(state="readonly")

# Start the RFID thread
def start_read_rfid_thread():
    threading.Thread(target=read_rfid_continuous, daemon=True).start()

# GUI Window
app = ctk.CTk()
app.title("RFID Reader")
app.geometry("400x200")

# Button to Read RFID
read_button = ctk.CTkButton(app, text="Read RFID Card", command=start_read_rfid_thread)
read_button.pack(pady=20)

# RFID Result Entry (Read-only)
rfid_entry = ctk.CTkEntry(app, width=300, font=ctk.CTkFont(size=14))
rfid_entry.insert(0, "Click the button to scan an RFID card.")
rfid_entry.configure(state="readonly")
rfid_entry.pack(pady=10)

# Run App
app.mainloop()
