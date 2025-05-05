import customtkinter as ctk
import serial
import threading

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Configure serial port (Change 'COM3' to your Arduino port)
arduino_port = 'COM3'  # Or '/dev/ttyUSB0' on Linux
baud_rate = 9600

# Read RFID Function
def read_rfid():
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=2)
        if ser.is_open:
            rfid_data = ser.readline().decode('utf-8').strip()
            if rfid_data:
                result_label.configure(text=f"RFID Card Read: {rfid_data}")
            else:
                result_label.configure(text="No card detected.")
            ser.close()
    except Exception as e:
        result_label.configure(text=f"Error: {e}")

# To prevent freezing GUI, use threading
def start_read_rfid_thread():
    threading.Thread(target=read_rfid, daemon=True).start()

# GUI Window
app = ctk.CTk()
app.title("RFID Reader")
app.geometry("400x200")

# Button to Read RFID
read_button = ctk.CTkButton(app, text="Read RFID Card", command=start_read_rfid_thread)
read_button.pack(pady=20)

# Result Label
result_label = ctk.CTkLabel(app, text="Waiting for RFID...", font=ctk.CTkFont(size=14))
result_label.pack(pady=10)

# Run App
app.mainloop()
