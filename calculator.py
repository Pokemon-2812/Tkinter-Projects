from tkinter import *
root=Tk()
img = PhotoImage(file='cal_ico.ico')
root.tk.call('wm', 'iconphoto', root._w, img)
def click(event):
    global scvalue
    text=event.widget.cget("text")
    if text=='=':
        if scvalue.get().isdigit():
            value=int(scvalue.get())
            scvalue.set(value)
        else:
            try:
                value=eval(screen.get())
            except Exception as e :
                print("Entered a wrong expression.")
            else:
                scvalue.set(value)
    elif text=='C':
        scvalue.set("")
    else:
        scvalue.set(scvalue.get()+str(text))
        screen.update()
root.geometry("550x700")
root.title("Calculator")
scvalue=StringVar()
scvalue.set("")
screen=Entry(root,textvariable=scvalue,font="lucida 40 bold")
screen.pack(fill=X,ipadx=8,pady=12)
num=9
def create_frame():
    global f
    f=Frame(root)
    f.pack()
def create_button(text):
    b=Button(f,text=text,width=8,height=2,fg="green",bg="orange",font="lucida 19 bold")
    b.pack(side=LEFT)
    b.bind("<Button-1>",click)
for i in range(3):
    create_frame()
    for i in range(3):
        create_button(num)
        num-=1
create_frame()
buttons=['+','-','/']
for text in buttons:
    create_button(text)
create_frame()
buttons=['*','=','0']
for text in buttons:
    create_button(text)
create_frame()
buttons=['%','.','C']
for text in buttons:
    create_button(text)
create_frame()
buttons=['(',')','00']
for text in buttons:
    create_button(text)
root.mainloop()

