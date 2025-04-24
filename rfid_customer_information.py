from tkinter.messagebox import showinfo
from PIL import ImageTk
from tkinter import*
import time

infoWindow = Tk()

infoWindow.geometry('700x500+650+150')
infoWindow.resizable(0,0)
infoWindow.title('Customer Information')

text=''
count= 0
def clock():
    date=time.strftime('%B %d, %Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimelabel.config(text=f' {date}\nTime: {currenttime}')
    datetimelabel.after(1000,clock)
def slider():
    global text, count
    if count == len(sms):
        count = 0
        text= ''
    text=text+sms[count]
    sliderlabel.config(text=text)
    count += 1
    sliderlabel.after(300,slider)





def addclient():
    showinfo('Add Client','Make Sure to get the client Information Accurately')
    clientframe=Toplevel(infoWindow)
    clientframe.geometry('250x250+700+300')
    clientframe.title('New Client Information')
    clientframe.resizable(0,0)

    idnumber_inclient = Label (clientframe,text= "I.D Number: ")
    idnumber_inclient.grid(row=0,column=0)
    idnumber_entry = Entry (clientframe)
    idnumber_entry.grid (row=0, column=1, pady=8)

    addName_inclient = Label(clientframe, text="Pet's Name: ")
    addName_inclient.grid(row=1, column=0)
    addnameclient_entry = Entry(clientframe)
    addnameclient_entry.grid(row=1, column=1, pady=8)

    breed_inclient = Label(clientframe, text="Pet's Breed: ")
    breed_inclient.grid(row=2, column=0)
    breed_entry = Entry(clientframe)
    breed_entry.grid(row=2, column=1, pady=8)

    petAge_inclient = Label(clientframe, text="Pet's Age: ")
    petAge_inclient.grid(row=3, column=0)
    petAge_entry = Entry(clientframe)
    petAge_entry.grid(row=3, column=1, pady=8)

    ownerName_inclient = Label(clientframe, text="Owner's Name: ")
    ownerName_inclient.grid(row=5, column=0)
    ownernameclient_entry = Entry(clientframe)
    ownernameclient_entry.grid(row=5, column=1, pady=8)

    addclient_button = Button (clientframe,text="SUBMIT")
    addclient_button.grid(row=6,columnspan=2,pady=5)


windowframe = Frame (infoWindow,bg='red')
windowframe.place(x=50,y=50,height=350,width=600)
#sample picture ng pet
samplepic=ImageTk.PhotoImage(file='pic1.jpg')
imagepic=Label(windowframe,image = samplepic)
imagepic.place(x=380,y=30)

#INFORMATION FROM DATABASE AFTER ISWIPE UNG RFID
InfoLabel = Label (windowframe,text="PET's INFORMATION  ",font=('Arial',15,'bold'),bg='red')
InfoLabel.grid(column=1,row=0)

NameLabel = Label (windowframe,text='NAME : ',font=('Arial',12,'bold','italic'),bg='red',fg='Yellow')
NameLabel.grid(column=0,row=1)
Namedtb = Label (windowframe,text='Trevor',font=('Arial',15,'bold'),bg='red',fg='White')
Namedtb.grid(column=1,row=1)

ageLabel = Label (windowframe,text='AGE : ',font=('Arial',12,'bold','italic'),bg='red',fg='Yellow')
ageLabel.grid(column=0,row=2)
agedtb = Label (windowframe,text='Lorem Ipsum Dolor',font=('Arial',15,'bold'),bg='red',fg='White')
agedtb.grid(column=1,row=2)


ageLabel = Label (windowframe,text='BREED : ',font=('Arial',12,'bold','italic'),bg='red',fg='Yellow')
ageLabel.grid(column=0,row=3)
agedtb = Label (windowframe,text='Lorem Ipsum Dolor',font=('Arial',15,'bold'),bg='red',fg='White')
agedtb.grid(column=1,row=3)

ageLabel = Label (windowframe,text='PET I.D NUMBER : ',font=('Arial',12,'bold','italic'),bg='red',fg='Yellow')
ageLabel.grid(column=0,row=4)
agedtb = Label (windowframe,text='Lorem Ipsum Dolor',font=('Arial',15,'bold'),bg='red',fg='White')
agedtb.grid(column=1,row=4)


addclient = Button (infoWindow,text='Add Client',command=addclient)
addclient.place (x=100,y=420)




sms='VET CLINIC NAME'
sliderlabel=Label(infoWindow,text=sms,font=('Times New Roman',26,'bold','italic'))
sliderlabel.place (x=200,y=0)
slider()


datetimelabel=Label(infoWindow,font=('times new roman',12,'italic bold'))
datetimelabel.place(x=550,y=430)
clock()







infoWindow.mainloop()