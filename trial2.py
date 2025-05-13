import customtkinter as ctk
import serial
import threading
import time

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Set your Arduino COM port and baud rate
arduino_port = 'COM3'  # Replace with your actual port (e.g., 'COM4' or '/dev/ttyUSB0')
baud_rate = 9600

# Continuous RFID reading function
def read_rfid_continuous():
    try:
        with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
            result_label.configure(text="Waiting for RFID card...")
            while True:
                if ser.in_waiting:
                    rfid_data = ser.readline().decode('utf-8').strip()
                    if rfid_data:
                        result_label.configure(text=f"RFID Card Read: {rfid_data}")
                        break  # Stop after reading one card
                time.sleep(0.1)
    except Exception as e:
        result_label.configure(text=f"Error: {e}")

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

# Result Label
result_label = ctk.CTkEntry(app, placeholder_text="Click the button to scan an RFID card.", font=ctk.CTkFont(size=14))
result_label.pack(pady=10)

# Run App
app.mainloop()
