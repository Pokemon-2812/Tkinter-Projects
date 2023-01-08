from tkinter import *
import random 
root=Tk()
root.title("Friendship Calculator")
root.geometry("600x400")
var1=StringVar()
var2=StringVar()
def show(p):
	lbl.config(text=f"Friendship between {var1.get()} and {var2.get()}:{p}%")
def calculate():
	percentage=random.randint(0,100)
	lbl.config(text="Calculating friendship...")
	root.after(5000,lambda p=percentage:show(p))
Label(root,text="Friendship Calculator",font="arial 18 bold").grid(row=0,column=0)
Label(root,text="Enter first person's name",font="arial 12").grid(row=1,column=0)
entry1=Entry(root,textvariable=var1).grid(row=1,column=1)
Label(root,text="Enter second person's name",font="arial 12").grid(row=2,column=0)
entry2=Entry(root,textvariable=var2).grid(row=2,column=1)
btn=Button(root,text="Calculate",font="arial 14 bold",bg="red",command=calculate)
btn.grid(row=3,column=0)
lbl=Label(root,font="arial 16")
lbl.grid(row=4,column=0)
root.mainloop()