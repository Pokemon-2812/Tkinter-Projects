from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo,askquestion
from tkinter.filedialog import asksaveasfile,askopenfilename
from PIL import ImageGrab,ImageTk,Image
root=Tk()
root.title("Create Grid")
root.geometry("600x400")
canvas=Canvas(root,bg="white")
canvas.pack(fill=BOTH)
width=2
imageWidth=0
imageHeight=0
increase=0
dpi = root.winfo_fpixels('1i')
def change_size(square_height,square_width):
	canvas.config(width=root.winfo_width(),height=root.winfo_height())
	y=0
	x=0
	y+=square_height
	rows=int(imageHeight//square_height+1)
	for i in range(rows-1):
		canvas.create_line(0,y,root.winfo_width(),y)
		y+=square_height
	columns=int(imageWidth//square_width+1)
	x+=square_width
	for i in range(columns-1):
		canvas.create_line(x,0,x,root.winfo_height())
		x+=square_width
def upload():
	global imageWidth,imageHeight,increase
	file=askopenfilename(defaultextension=".jpg",filetypes=[('JPG Files',"*.jpg"),("PNG Files","*.png")])
	if file=="":
		file=None
	if file!=None:
		canvas.delete('all')
		file=Image.open(file)
		increase=file.size[0]/400
		file=file.resize((int(file.size[0]/increase),int(file.size[1]/increase)))
		canvas.image = ImageTk.PhotoImage(file)
		canvas.create_image(0, 0, image=canvas.image, anchor='nw')
		root.geometry(f"{file.size[0]}x{file.size[1]}")
		imageWidth=file.size[0]
		imageHeight=file.size[1]
def make_grid():
	if(imageWidth==0):
		showinfo("Image","First Upload an Image!")
	else:
		try:
			square_width=float(askstring("Width","What do you want the width of each square?(in inches)"))
			square_height=float(askstring("Height","What do you want the height of each square?(in inches)"))
			square_height*=float(dpi)
			square_width*=float(dpi)

		except Exception as e:
			showinfo("Number","Please enter numbers!")
		else:
			square_height=float(square_height/increase)
			square_width=float(square_width/increase)
			change_size(square_height,square_width)
def save():
	global imageWidth,imageHeight
	file = asksaveasfile(defaultextension=".jpg" ,filetypes = [('JPG Files', '*.jpg*'),('PNG Files','*.png')])
	x=root.winfo_rootx()+canvas.winfo_x()
	y=root.winfo_rooty()+canvas.winfo_y()
	x1=x+imageWidth
	y1=y+imageHeight
	if file!=None:
		ImageGrab.grab().crop((x,y,x1,y1)).save(file)
def clear():
	global imageWidth,imageHeight
	imageWidth=0
	imageHeight=0
	canvas.delete('all')
menu=Menu(root)
fileMenu=Menu(menu,tearoff=0)
fileMenu.add_command(label="Save",command=save)
fileMenu.add_command(label="Make Grid",command=make_grid)
fileMenu.add_command(label="Upload",command=upload)
fileMenu.add_command(label="Clear",command=clear)
menu.add_cascade(label="File",menu=fileMenu)
root.config(menu=menu)
def change_screen():
	canvas.config(width=root.winfo_width(),height=root.winfo_height())
	root.after(500,change_screen)
change_screen()
root.mainloop()