from tkinter import *
import random
from tkinter.messagebox import showinfo
root=Tk()
root.geometry("400x300")
root.title("Color Game")
score=0
time_left=31
colors=["red","blue","green","yellow","orange","purple","brown","black","white","gold","pink"]
color_name=colors[random.randint(0,len(colors)-1)]
text_color=colors[random.randint(0,len(colors)-1)]
instruction=Label(root,text="Write the color of the text ",font="arial 18")
instruction.pack(anchor="center")
score_text=Label(root,text="Score:0",font="arial 14")
score_text.pack(anchor="center")
time_text=Label(root,text="Time Left:30",font="arial 14")
time_text.pack(anchor="center")
text=Label(root,text=color_name,fg=text_color,font="arial 24")
text.pack(anchor="center")
user_value=StringVar()
e=Entry(root,textvariable=user_value)
e.pack(anchor="center")
def change_time():
    global time_left,score,text_color,color_name
    if(time_left>0):
        time_left-=1
        time_text.config(text="Time Left:"+str(time_left))
        if(user_value.get().lower()==text_color):
        	score+=1
        	score_text.config(text="Score:"+str(score))
        	text_color=colors[random.randint(0,len(colors)-1)]
        	color_name=colors[random.randint(0,len(colors)-1)]
        	text.config(text=color_name,fg=text_color)
        	user_value.set("")
        root.after(1000,change_time)
def restart():
    global time_left,score,text_color,color_name
    if(time_left==0):
        time=True
        time_left=31
    else:
        time=False
        time_left=30
    score=0
    score_text.config(text="Score:"+str(score))
    text_color=colors[random.randint(0,len(colors)-1)]
    color_name=colors[random.randint(0,len(colors)-1)]
    text.config(text=color_name,fg=text_color)
    time_text.config(text="Time Left:" + str(time_left))
    user_value.set("")
    if(time):
        change_time()
change_time()
menubar=Menu(root)
option_menu=Menu(menubar,tearoff=False)
option_menu.add_command(label="Restart",command=restart)
menubar.add_cascade(label="Options",menu=option_menu)
root.config(menu=menubar)
root.mainloop()