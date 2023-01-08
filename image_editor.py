#Importing the modules
from tkinter import *
from tkinter import filedialog
import os
from PIL import Image,ImageTk,ImageFilter,ImageEnhance
root=Tk()
root.title("Image Editor")
root.geometry("1350x675")
#These are the variables for CheckButton and Entries
var1=IntVar()
var2=StringVar()
var3=StringVar()
var2.set("1.0")
var3.set("0,0,0,0")
fil="apple.jpg"
img1=Image.open(fil)
#the width and height of the image
width,height=img1.size
img2=ImageTk.PhotoImage(img1)
#Our image
lbl=Label(root,image=img2)
#A message
t="*The Image will remain in its original or applied size\nIt is resized to make it fit inside the window."
Label(root,font="lucida 13 italic",text=t).grid(row=0,column=4)
#Our labels for the different values
lbl2=Label(root,text="Width",font="lucida 15 bold")
lbl3=Label(root,text="Height",font="lucida 15 bold")
lbl4=Label(root,text="Rotate",font="lucida 15 bold")
lbl5=Label(root,text="Blur",font="lucida 15 bold")
lbl6=Label(root,text="Brightness",font="lucida 15 bold")
lbl7=Label(root,text="Crop",font="lucida 15 bold")
#Packing all the labels
row=0
labels=[lbl,lbl2,lbl3,lbl4,lbl5,lbl6,lbl7]
for label in labels:
    label.grid(row=row,column=3)
    row+=1
#Sliders for setting values
slider1=Scale(root,from_=0,to=1500,orient=HORIZONTAL)
slider2=Scale(root,from_=0,to=1000,orient=HORIZONTAL)
slider3=Scale(root,from_=0,to=360,orient=HORIZONTAL)
slider4=Scale(root,from_=0,to=40,orient=HORIZONTAL)
sliders=[slider1,slider2,slider3,slider4]
#Packing all the labels
row=1
for slider in sliders:
    slider.grid(row=row,column=4)
    row+=1
#Setting Default Value
slider1.set(width)
slider2.set(height)
#Entries
Entry(root,textvariable=var2).grid(row=5,column=4)
Entry(root,textvariable=var3).grid(row=6,column=4)
#Checkbutton for black and white
b_a=Checkbutton(text="Want Black and White image?",variable=var1,font="lucida 15 bold")
b_a.grid(row=7,column=3)
#Openfile method
def openfile():
    global fil,img1
    fil=filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Image File",filetypes=[("JPG File","*.jpg"),("PNG File","*.png"),("All Files","*.*")])
    img1=Image.open(fil)
    width,height=img1.size
    if height>350 or width>1250:
        img1=img1.resize((int(width/17),int(height/17)))
        slider1.set(int(width/17))
        slider2.set(int(height/17))
    slider1.set(width)
    slider2.set(height)
    img2=ImageTk.PhotoImage(img1)
    lbl.configure(image=img2)
    lbl.image=img2
#Method for cropping
def crop():
    global img1
    width,height=img1.size
    try:
        directions=var3.get().split(",")
        top,bottom,left,right=int(directions[0]),int(directions[1]),int(directions[2]),int(directions[3])
    except Exception as e:
        pass
    else:
        img1=img1.crop((left,top,width-right,height-bottom))
#Our main apply method that applies the effects
def apply():
    global img1
    img1=Image.open(fil)
    width=slider1.get()
    height=slider2.get()
    rotation=slider3.get()
    blur=slider4.get()
    crop()
    try:
        bright=float(var2.get())
    except Exception as e:
        pass
    else:
        enhancer=ImageEnhance.Brightness(img1)
        img1=enhancer.enhance(bright)
    img1=img1.filter(ImageFilter.GaussianBlur(blur))
    img1=img1.rotate(rotation)
    if var1.get()==1:
        img1=img1.convert(mode='L')
    try:
        img1=img1.resize((width,height))
    except ValueError:
        img1=img1.resize((1,1))
    if width>1250 or height>350:
        pass
    if not(width>1250 or height>350):
        img2=ImageTk.PhotoImage(img1)
        lbl.configure(image=img2)
        lbl.image=img2
#Save methodz
def save():
    fil=filedialog.asksaveasfilename(initialfile="Untitled-1.jpg",defaultextension=".jpg",filetypes=[("JPG File","*.jpg*"),("PNG File","*.png")])
    try:
        rgb=img1.convert('RGB')
        rgb.save(fil)
    except Exception as e:
        pass
#Clear Effects method
def clear():
    img1=Image.open(fil)
    width,height=img1.size
    if height>600 or width>1250:
        img1=img1.resize((int(width/17),int(height/17)))
    img2=ImageTk.PhotoImage(img1)
    lbl.configure(image=img2)
    lbl.image=img2
    var1.set(0)
    var2.set("1.0")
    var3.set("0,0,0,0")
    slider1.set(width)
    slider2.set(height)
    slider3.set(0)
    slider4.set(0)
#Filemenu
menu=Menu(root)
filemenu=Menu(menu,tearoff=0)
filemenu.add_command(label="Open",command=openfile)
filemenu.add_command(label="Save",command=save)
filemenu.add_separator()
filemenu.add_command(label="Clear Effects",command=clear)
root.config(menu=menu)
menu.add_cascade(label="File",menu=filemenu)
#Apply button
Button(root,text="Apply",font="lucida 15 bold",bg="red",width="7",command=apply,padx=5).grid(row=8,column=3)
root.mainloop()