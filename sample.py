from customtkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import mysql.connector
import io

from customtkinter import CTkImage



root = CTk()
root.title ("Image Upload & View")

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '12345',
    database = 'ImportingImageSample'
)

cursor = db.cursor()

def upload_image():
    top = CTkToplevel(root)
    top.title("Upload Image")

    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        with open(file_path, 'rb') as f:  #passing the variable name sa f.
            binary_data = f.read()
            cursor.execute("INSERT INTO tb_image (ImportedImage) values (%s)",(binary_data,))
            db.commit()

        img = Image.open(file_path)
        img = img.resize((300,300))
        img_tk = CTkImage(light_image=img, size=(300,300))


        label = CTkLabel(top, image=img_tk, text= "")
        label.image = img_tk
        label.pack(padx=10,pady=10)

def view_image():
    cursor.execute("Select importedImage From tb_image ORDER by id DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        top = CTkToplevel(root)
        top.title ("view Image")


        binary_data = result[0]
        img_data = io.BytesIO(binary_data)
        img = Image.open(img_data)
        img = img.resize((300,300))
        img_tk = CTkImage(light_image=img, size=(300,300))

        label = CTkLabel(top, image=img_tk,text="")
        label.image = img_tk
        label.pack(padx=10,pady=10)






upload_btn = CTkButton(root, text="Upload Image", command=upload_image)
upload_btn.pack(padx=20, pady= 10)

view_btn = CTkButton(root, text="View Latest Image", command=view_image)
view_btn.pack(padx=20,pady=10)

root.mainloop()
