from tkinter import *
import random
from tkinter.filedialog import asksaveasfile,askopenfilename
from PIL import ImageGrab,ImageTk,Image
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from tkinter import ttk
root=Tk()
root.title("Paint")
root.geometry("800x600")
root.update_idletasks()
color="black"
size=10
eraser_size=3
red=0
blue=0
green=0
brushWidth=2
symetric_drawing=False
workingEraser=False
custom_btn=None
eraserColor="white"
eraserWidth=2
typingText=False
text=""
fonts=("helvetica","14")
photo = PhotoImage(file = "paint_icon.png")
root.iconphoto(False, photo)
n=StringVar()
o=StringVar()
p=StringVar()
def save():
	file = asksaveasfile(defaultextension=".jpg" ,filetypes = [('JPG Files', '*.jpg*'),('PNG Files','*.png')])
	x=root.winfo_rootx()+canvas.winfo_x()
	y=root.winfo_rooty()+canvas.winfo_y()
	x1=x+canvas.winfo_width()
	y1=y+canvas.winfo_height()
	if file!=None:
		root.title("Paint - "+file.name)
		ImageGrab.grab().crop((x,y,x1,y1)).save(file)
def openfile():
	file=askopenfilename(defaultextension=".jpg",filetypes=[('JPG Files',"*.jpg"),("PNG Files","*.png")])
	if file!=None:
		try:
			canvas.delete('all')
			file=Image.open(file)
			canvas.image = ImageTk.PhotoImage(file)
			canvas.create_image(0, 0, image=canvas.image, anchor='nw')
		except Exception as e:
			showinfo("Error","Please open a valid image file.")
def symetric(event):
	global symetric_drawing
	symetric_drawing=not(symetric_drawing)
def make_ellipse(event):
	canvas.create_oval(event.x-size/2,event.y-size/2,event.x+size/2,event.y+size/2,fill=color)
	if symetric_drawing:
		canvas.create_oval(root.winfo_width()-(event.x-size/2),event.y-size/2,root.winfo_width()-(event.x+size/2),event.y+size/2,fill=color)
def change_color(event,color_name):
	global color
	if color_name=="random":
		hexadecimal = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
		color=hexadecimal
		random_btn.config(bg=hexadecimal)
	else:
	 	color=color_name
def change_size(event,size_number):
	global size
	if(workingEraser==False):
		size=size_number
	else:
		eraser_size=size_number
def eraser(event):
	global workingEraser
	workingEraser=True
def click(event):
	global prev,typingText
	if(typingText):
		canvas.create_text(event.x,event.y,text=text,fill=color,font=fonts)
		typingText=False
	else:
		prev=event
def move(event):
	global prev
	if(workingEraser==False):
		canvas.create_line(prev.x,prev.y,event.x,event.y,width=brushWidth,fill=color)
		if symetric_drawing:
			canvas.create_line(root.winfo_width()-prev.x,prev.y,root.winfo_width()-event.x,event.y,width=brushWidth,fill=color)
	else:
		canvas.create_line(prev.x,prev.y,event.x,event.y,width=eraserWidth,fill=eraserColor)
	prev=event
def new():
	root.title("Paint")
	canvas.delete('all')
def pointer(event):
	global workingEraser
	workingEraser=False
def background():
	global eraserColor
	background_color=askstring("Background","What do you want the background color to be?")
	try:
		canvas.config(bg=background_color)
	except Exception as e:
		showinfo("Error","Color not found!")
	else:
		canvas.delete('all')
		eraserColor=background_color
def shortcut():
	top=Toplevel(root)
	top.title("Shortcuts")
	top.geometry("300x330")
	text_area=Text(top,bg="#323232",fg="white",width=15,font="arial 14")
	text_area.pack(fill=BOTH)
	text=""
	keys={"a":"random color","right click":"circle","r":"red","b":"blue","y":"yellow","o":"orange","p":"pink","w":"brown","g":"green","e":"eraser","l":"symmetry","m":"pointer","sizes":"1,2,3"}
	for key,value in keys.items():
		text+=key+" : "+value+"\n"
	text_area.insert(1.0,text)
	text_area.config(state=DISABLED)
	top.mainloop()
def add_color(slider1,slider2,slider3):
	global custom_btn,red,blue,green
	red=slider1.get()
	blue=slider2.get()
	green=slider3.get()
	if(custom_btn==None):
		custom_btn=Button(f1,bg='#%02x%02x%02x' % (slider1.get(),slider2.get(),slider3.get()),width=4,highlightbackground="black",highlightthickness=2)
		custom_btn.bind('<Button-1>',lambda event,col='#%02x%02x%02x' % (slider1.get(),slider2.get(),slider3.get()):change_color(event,col))
		custom_btn.pack(side=LEFT,padx = 5,pady=5)
	else:
		custom_btn.config(bg='#%02x%02x%02x' % (slider1.get(),slider2.get(),slider3.get()))
		custom_btn.bind('<Button-1>',lambda event,col='#%02x%02x%02x' % (slider1.get(),slider2.get(),slider3.get()):change_color(event,col))
def custom_color():
	top2=Toplevel(root)
	top2.title("Custom Color")
	top2.geometry("450x350")
	Label(top2,text="Red",font="arial 16 bold").grid(row=0,column=0)
	slider1=Scale(top2,from_=0,to=255,orient=HORIZONTAL)
	slider1.grid(row=0,column=1)
	Label(top2,text="Green",font="arial 16 bold").grid(row=1,column=0)
	slider2=Scale(top2,from_=0,to=255,orient=HORIZONTAL)
	slider2.grid(row=1,column=1)
	Label(top2,text="Blue",font="arial 16 bold").grid(row=2,column=0)
	slider3=Scale(top2,from_=0,to=255,orient=HORIZONTAL)
	slider3.grid(row=2,column=1)
	sliders=[slider1,slider2,slider3]
	colors=[red,blue,green]
	for i in range(3):
		sliders[i].set(colors[i])
	Label(top2,text="Color",font="arial 16 bold").grid(row=3,column=0)
	text=Text(top2,width=18,height=7,bg='#%02x%02x%02x' % (red,blue,green))
	text.grid(row=3,column=1)
	text.config(state=DISABLED)
	createButton=Button(top2,text="Add",bg="red",fg="black",font="arial 14 bold",padx=8,command=lambda:add_color(slider1,slider2,slider3))
	createButton.grid(row=4,column=0)
	def custom():
		text.config(bg='#%02x%02x%02x' % (slider1.get(),slider2.get(),slider3.get()))
		top2.after(1000,custom)
	custom()
	top2.mainloop()
def eraserSize(wid):
	global eraserWidth
	eraserWidth=wid
	if(eraserWidth<0):
		eraserWidth=2
def brush(wid):
	global brushWidth
	brushWidth=wid
	if brushWidth<0:
		brushWidth=2
def write():
	global text,typingText
	text=askstring("Text","What do you want to type?")
	typingText=True
	showinfo("Click","Click wherever you want the text to be!")
def fontstyle():
	top=Toplevel()
	top.geometry("500x400")
	Label(top,text="Font Style",font="lucida 15 bold").grid(row=0,column=0)
	Label(top,text="Font Size",font="lucida 15 bold").grid(row=1,column=0)
	Label(top,text="Font Type",font="lucida 15 bold").grid(row=2,column=0)
	combobox1=ttk.Combobox(top,width=24,textvariable=n)
	combobox2=ttk.Combobox(top,width=24,textvariable=o)
	combobox3=ttk.Combobox(top,width=24,textvariable=p)
	combobox1['values']=('helvetica','calibri','futura','garamond','times new roman','arial','cambria','verdana','rockwell','franklin gothic',
	'lucida')
	combobox3['values']=('Regular','bold','italic','underline')
	nums=[i for i in range(11,40)]
	combobox2['values']=tuple(nums)
	combobox1.grid(row=0,column=1)
	combobox2.grid(row=1,column=1)
	combobox3.grid(row=2,column=1)
	n.set(fonts[0])
	o.set(fonts[1])
	if(len(fonts)==3):
		p.set(fonts[2])
	else:
		p.set('Regular')
	Button(top,text="Change Font",bg="red",command=change_font,font="lucida 12 bold").grid(row=3,column=0)
	top.mainloop()
def change_font():
	global fonts
	if p.get()=='Regular':
	    fonts=(n.get(),o.get())
	else:
	    fonts=(n.get(),o.get(),p.get())
f1=Frame(root,highlightbackground="black",highlightthickness=2,relief=SUNKEN)
f1.pack(side=TOP,fill=X)
f2=Frame(root,highlightbackground="black",highlightthickness=2,relief=SUNKEN)
f2.pack(side=TOP,fill=X)
canvas = Canvas(root,bg = "white",height=root.winfo_height())
canvas.pack(fill=BOTH)
all_colors=["red","blue","yellow","orange","pink","brown","black","purple","green","white"]
buttons=[]
for new_color in all_colors:
	btn=Button(f1,bg=new_color,width=4,highlightbackground="black",highlightthickness=2)
	btn.bind('<Button-1>',lambda event,col=new_color:change_color(event,col))
	btn.pack(side=LEFT,padx = 5,pady=5)
random_btn=Button(f1,bg=["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])],width=4,highlightbackground="black",highlightthickness=2)
random_btn.pack(side=LEFT,padx=5,pady=5)
image1=Image.open("pointer.png")
image1=image1.resize((35,25))
photo=ImageTk.PhotoImage(image1)
text_btn=Button(f2,text="A",font="arial 13 bold",command=write)
text_btn.pack(side=LEFT,padx=5,pady=5,ipadx=5)
btn1=Button(f2,image=photo,command=lambda event=None:pointer(event))
btn1.pack(side=LEFT,padx=5,pady=5)
image2=Image.open("eraser.jpg")
image2=image2.resize((35,25))
photo2=ImageTk.PhotoImage(image2)
btn2=Button(f2,image=photo2,command=lambda event=None:eraser(event))
btn2.pack(side=LEFT,padx=5,pady=5)
increase_btn=Button(f2,text="+",font="arial 13 bold",command=lambda:eraserSize(eraserWidth+5))
increase_btn.pack(side=LEFT,padx=5,pady=5,ipadx=5)
decrease_btn=Button(f2,text="-",font="arial 13 bold",command=lambda:eraserSize(eraserWidth-5))
decrease_btn.pack(side=LEFT,padx=5,pady=5,ipadx=5)
values=[5,10,15]
for i in range(len(values)):
	btn=Button(f2,text=i+1,font="arial 13 bold",command=lambda event=None,size=values[i]:change_size(event,size))
	btn.pack(side=LEFT,padx=5,pady=5,ipadx=5)
symetry_btn=Button(f2,text="S",font="arial 13 bold",command=lambda event=None:symetric(event))
symetry_btn.pack(side=LEFT,padx=5,pady=5,ipadx=5)
brushImage=Image.open("brush.jpg")
brushImage=brushImage.resize((35,30))
brushphoto=ImageTk.PhotoImage(brushImage)
brush_btn=Button(f2,image=brushphoto,command=lambda:brush(2))
brush_btn.pack(side=LEFT,padx=5,pady=5)
increase_btn2=Button(f2,text="+",font="arial 13 bold",command=lambda:brush(brushWidth+5))
increase_btn2.pack(side=LEFT,padx=5,pady=5,ipadx=5)
decrease_btn2=Button(f2,text="-",font="arial 13 bold",command=lambda:brush(brushWidth-5))
decrease_btn2.pack(side=LEFT,padx=5,pady=5,ipadx=5)
random_btn.bind('<Button-1>',lambda event:change_color(event,"random"))
root.bind('<Button-3>',make_ellipse)
root.bind('b',lambda event:change_color(event,"blue"))
root.bind('g',lambda event:change_color(event,"green"))
root.bind('y',lambda event:change_color(event,"yellow"))
root.bind('r',lambda event:change_color(event,"red"))
root.bind('o',lambda event:change_color(event,"orange"))
root.bind('p',lambda event:change_color(event,"pink"))
root.bind('w',lambda event:change_color(event,"brown"))
root.bind('a',lambda event:change_color(event,"random"))
root.bind('1',lambda event:change_size(event,5))
root.bind('2',lambda event:change_size(event,10))
root.bind('3',lambda event:change_size(event,20))
root.bind('l',lambda event:symetric(event))
root.bind('e',lambda event:eraser(event))
root.bind('m',lambda event:pointer(event))
canvas.bind('<Button-1>',click)
canvas.bind('<B1-Motion>', move)
menu=Menu(root)
fileMenu=Menu(menu,tearoff=0)
fileMenu.add_command(label="Save",command=save)
fileMenu.add_command(label="New",command=new)
fileMenu.add_command(label="Open",command=openfile)
menu.add_cascade(label="File",menu=fileMenu)
editMenu=Menu(menu,tearoff=0)
editMenu.add_command(label="Change Background",command=background)
editMenu.add_command(label="Custom Color",command=custom_color)
editMenu.add_command(label="Font...",command=fontstyle)
menu.add_cascade(label="Edit",menu=editMenu)
helpMenu=Menu(menu,tearoff=0)
helpMenu.add_command(label="Shortcuts",command=shortcut)
menu.add_cascade(label="Help",menu=helpMenu)
root.config(menu=menu)
def change_width():
	if(root.winfo_height()!=600):
		canvas.config(width=root.winfo_width(),height=root.winfo_height())
	root.after(500,change_width)
change_width()
root.mainloop()