from tkinter import *
from tkinter.simpledialog import askstring
import random
from datetime import date
from tkinter.filedialog import asksaveasfilename
from pathlib import *
root=Tk()
order_no=0
name=""
def check_change(item):
	for key,value in item_checked.items():
		if value.get()==1:
			if item_quantity[key].get()==0:
				item_quantity[key].set(1)
		elif value.get()==0:
			item_quantity[key].set(0)
def add():
	global order_no,name
	order_no=random.randint(1000,9000)
	if name=="":
	    name=askstring("Name","What is your name?")
	if name!=None:
	    today=date.today()
	    text="Order Number-"+str(order_no)+"\n"
	    text+=f"Name-{name}\nDate-{today}\n"
	    text+="-"*80+"\n"
	    total=0
	    for key,value in item_checked.items():
		    if value.get()==1:
			    if isinstance(item_quantity[key].get(), str):
				    item_quantity[key].set(1)
			    item_cost=int(cost[key])*int(item_quantity[key].get())
			    text+=f"Food: {key},Quantity: {item_quantity[key].get()},Cost: {item_cost}\n"
			    total+=item_cost
	    text+="-"*80+"\n"
	    text+=f"Total Cost:{total}\n"
	    text+=f"Total Cost(GST Included):{total * 105/100}"
	    text_area.config(state=NORMAL)
	    text_area.delete(1.0,END)
	    text_area.insert(1.0,text)
	    text_area.config(state=DISABLED)
def save():
	file = asksaveasfilename(initialfile = f'bill{order_no}.txt',defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
	if file!="":
		with open(file,'w') as f:
			f.write(text_area.get(1.0,END))
def reset():
	global name
	text_area.config(state=NORMAL)
	text_area.delete(1.0,END)
	text_area.config(state=DISABLED)
	for key,value in item_checked.items():
		value.set(0)
		item_quantity[key].set(0)
	name=""
def check_click(event,food):
	if(item_checked[food].get()==0):
	    item_checked[food].set(1)
root.geometry("1000x650")
root.title("Restaurant Management System")
foods=["Dosa","Idli","Pav","Aloo Parantha","Burger","Pizza"]
drinks=["Lassi","Shikanji","Pepsi","Coca-Cola","Red Bulls","Fanta"]
sweets=["Rasmalai","Rasgulla","Rasmulla","Jalebi","Gulab Jamun","Kheer"]
cost={}
for drink in drinks:
	cost[drink]=50
for sweet in sweets:
	cost[sweet]=75
for food in foods:
	cost[food]=120
Label(root,text="Restaurant Management System",bg="red",fg="gold",font="arial 22 bold").pack(fill=X)
#Food frame
left_frame=Frame(root)
left_frame.pack(side="left", fill="both", expand=True)
food_frame=LabelFrame(left_frame)
food_frame.pack(side=LEFT)
item_quantity={}
item_checked={}
Label(food_frame,text="Meals",font="arial 18 bold").pack()
for food in foods:
    var=IntVar()
    var2=IntVar()
    checkbox=Checkbutton(food_frame,text=food,padx=14,variable=var,font="arial 12",command=lambda:check_change(food))
    checkbox.pack()
    entry=Entry(food_frame,textvariable=var2)
    entry.pack()
    entry.bind('<Button-1>',lambda:check_click(food))
    item_quantity[food]=var2
    item_checked[food]=var
#Drinks Frame
drinks_frame=LabelFrame(left_frame,highlightbackground="grey",highlightthickness=2)
drinks_frame.pack(side=LEFT)
Label(drinks_frame,text="Drinks",font="arial 18 bold").pack()
for drink in drinks:
    var=IntVar()
    var2=IntVar()
    checkbox=Checkbutton(drinks_frame,text=drink,padx=14,variable=var,font="arial 12",command=lambda:check_change(drink))
    checkbox.pack()
    entry=Entry(drinks_frame,textvariable=var2)
    entry.pack()
    entry.bind('<Button-1>',lambda :check_click(drink))
    item_quantity[drink]=var2
    item_checked[drink]=var
#Sweets Frame
sweets_frame=LabelFrame(left_frame)
sweets_frame.pack(side=LEFT)
Label(sweets_frame,text="Sweets",font="arial 18 bold").pack()
for sweet in sweets:
    var=IntVar()
    var2=IntVar()
    checkbox=Checkbutton(sweets_frame,text=sweet,padx=14,variable=var,font="arial 12",command=lambda:check_change(sweet))
    checkbox.pack()
    entry=Entry(sweets_frame,textvariable=var2)
    entry.pack()
    entry.bind('<Button-1>',lambda:check_click(sweet))
    item_quantity[sweet]=var2
    item_checked[sweet]=var
# #Right Frame
bill_frame=Frame(root)
bill_frame.pack(side="right",fill="both",expand=True)
scrollbar=Scrollbar(bill_frame)
scrollbar.pack(fill=Y,side=RIGHT)
text_area=Text(bill_frame,yscrollcommand=scrollbar.set)
text_area.pack(fill=Y)
scrollbar.config(command=text_area.yview)
text_area.config(state=DISABLED)
btn_frame=Frame(root)
btn_frame.pack(side=BOTTOM)
reset_btn=Button(btn_frame,text="Reset",font="arial 18 bold",command=reset)
reset_btn.pack(side="left")
add_btn=Button(btn_frame,text="Add",font="arial 18 bold",command=add)
add_btn.pack(side="left")
save_btn=Button(btn_frame,text="Save",font="arial 18 bold",command=save)
save_btn.pack(side="left")
root.mainloop()