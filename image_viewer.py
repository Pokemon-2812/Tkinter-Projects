from tkinter import *
from tkinter.filedialog import askdirectory
import os
from PIL import ImageTk,Image
root=Tk()
root.geometry("600x400")
root.title("Image Viewer")
index=0
def nextImage():
	global index,dir_
	if(index<len(images)-1):
		index+=1
		image1=Image.open(dir_+"/"+images[index])
		increase=image1.size[0]/150
		image1=image1.resize((int(image1.size[0]/increase),int(image1.size[1]/increase)))
		photo=ImageTk.PhotoImage(image1)
		label.configure(image=photo)
		label.image=photo
def previous():
	global index,dir_
	if(index>=1):
		index-=1
		image1=Image.open(dir_+"/"+images[index])
		increase=image1.size[0]/150
		image1=image1.resize((int(image1.size[0]/increase),int(image1.size[1]/increase)))
		photo=ImageTk.PhotoImage(image1)
		label.configure(image=photo)
		label.image=photo
def openfolder():
	global images,btn,btn2,dir_,index
	dir_=askdirectory()
	if dir_=="":
		dir_=None
	if dir_!=None:
		images=[]
		for file in os.listdir(dir_):
			if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
				images.append(file)
		index=0
		if(btn==None):
			btn=Button(root,text="Previous",bg="blue",fg="white",font="arial 14 bold",command=previous)
			btn.pack(padx=5,ipadx=5,side=LEFT)
			btn2=Button(root,text="Next",bg="red",fg="white",font="arial 14 bold",command=nextImage)
			btn2.pack(padx=5,ipadx=5,side=RIGHT)
		if(len(images)>0):
			image1=Image.open(dir_+"/"+images[0])
			image1=image1.resize((300,200))
			photo=ImageTk.PhotoImage(image1)
			label.configure(image=photo)
			label.image=photo
		if(len(images)==0):
			label.configure(image=None)
			label
menu=Menu(root)
btn=None
btn2=None
fileMenu=Menu(menu,tearoff=0)
fileMenu.add_command(label="Open Folder",command=openfolder)
label=Label(root)
label.pack(side=TOP)
menu.add_cascade(label="File",menu=fileMenu)
root.config(menu=menu)
root.mainloop()