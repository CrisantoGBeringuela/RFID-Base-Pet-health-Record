import customtkinter
from customtkinter import *
from PIL import Image
from tkinter import messagebox
from customtkinter import CTkEntry, CTkButton, CTk, CTkImage
import sys
import os
import subprocess



root = CTk()
root.geometry('1400x800+100+80')
root.resizable(False,False)
root.title('Login')
set_appearance_mode("light")



import subprocess
import sys
import os


def login():
    if userentry.get() == '' or passentry.get() == '':
        messagebox.showerror('Error', 'Please fill in the box')
    elif userentry.get() == 'superuser' and passentry.get() == 'superpassword':
        messagebox.showinfo('Login', 'You are login as ADMINISTRATOR')
        root.destroy()

        # Determine the path to masterfile.exe depending on whether running in PyInstaller bundle or not
        if hasattr(sys, '_MEIPASS'):
            # Running from bundled exe, _MEIPASS is temp folder path
            base_path = sys._MEIPASS
        else:
            # Running from script, current folder
            base_path = os.path.abspath(".")

        masterfile_exe_path = os.path.join(base_path, "masterfile.exe")

        try:
            subprocess.Popen(masterfile_exe_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch masterfile.exe:\n{e}")

    else:
        messagebox.showwarning('No user Found', 'Enter User Correctly')


bgpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\masterfilepicture\bg1.jpg'), size=(1400,800))
bgpicturelabel = CTkLabel(root, image=bgpicture,text='')
bgpicturelabel.place (x=0,y=0)

#PET PICTURE FRAME AND LOGO
vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\pic1.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=70,y=60)

vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\pic2.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=275,y=60)

vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\pic3.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=480,y=60)

vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\pic4.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=70,y=265)

vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\logo.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=275,y=265)

vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\pic5.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=480,y=265)

vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\pic6.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=70,y=470)
vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\pic7.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=275,y=470)

vetpicture = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\petsample\pic8.png'),size=(200,200))
vetpicturelabel = CTkLabel(root, image=vetpicture,text='')
vetpicturelabel.place (x=480,y=470)


loginFrame = CTkFrame(root, width=350, height=480,fg_color="#F6F5F2",border_color='#798645',border_width=3)
loginFrame.place(x=830,y=100)


ctk_image = CTkImage(dark_image=Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\logo\pawprint.png'), size=(100, 100))
image_label = CTkLabel(loginFrame, image=ctk_image, text="")
image_label.place(x=130,y=15)

welcometext=CTkLabel(loginFrame,text='Welcome',font=('Arial',45))
welcometext.place(x=80,y=120)


#user
username = CTkLabel(loginFrame,compound='left',text=" Username ",font=('Arial',15))
username.place(x=30,y=170)
userentry=CTkEntry(loginFrame,font=('times new roman',18),placeholder_text= 'Enter Username',width=280,height=45,border_color='#798645',corner_radius=15)
userentry.place(x=30,y=200)

#password
password = CTkLabel(loginFrame,text=" Password ",compound='left',font=('Arial',15))
password.place(x=30,y=260)
passentry=CTkEntry(loginFrame,font=('times new roman',19),placeholder_text= 'Enter Password',width=280,height=40,show='*',border_color='#798645',corner_radius=15)
passentry.place(x=30,y=290)



loginpic = Image.open(r'D:\Python\RFID-Base-Pet-health-Record-main\logo\enter1.png')
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