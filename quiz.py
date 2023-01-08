#Program to make a quiz application with tkinter
from tkinter import *
import json
root=Tk()
root.geometry("500x400")
root.title("Quiz")
user_answers={}
score=0
with open('data.json') as f:
	data=json.load(f)
	questions=data[0]
	answers=data[1]
	options=data[2]
for i in range(len(questions)):
	user_answers[i]=None
label=Label(root,text="Quiz",font="arial 20 bold").pack()
index=0
radiobuttons=[]
var1=StringVar()
var1.set(" ")
question_label=Label(root,text="1."+questions[index],font="arial 14")
question_label.pack(anchor=W)
for option in options[index]:
    radiobutton=Radiobutton(root, text = option, variable = var1,value = option,font="arial 12")
    radiobutton.pack(anchor=W)
    radiobuttons.append(radiobutton)
def next_option():
	global index,score
	if(button.cget("text")=="Next"):
		if(index<len(questions)-1):
			user_answers[index]=var1.get()
			index+=1
			if(user_answers[index]==None):
				var1.set(" ")
			else:
				var1.set(user_answers[index])
			question_label.config(text=f"{index+1}.{questions[index]}")
			for i in range(4):
				radiobuttons[i].config(text=options[index][i],value=options[index][i])
			if(index==len(questions)-1):
				button.config(text="Submit")
	else:
		user_answers[index]=var1.get()
		for i in range(len(answers)):
			if(answers[i]==user_answers[i]):
				score+=1
		score_text.config(text=f"Score:{score}/{len(questions)}")
		button.config(state=DISABLED)
		button2.config(state=DISABLED)
def previous_option():
	global index
	if(index>0):
		index-=1
		for i in range(4):
			radiobuttons[i].config(text=options[index][i],value=options[index][i])
		var1.set(user_answers[index])
		button.config(text="Next")
		question_label.config(text=questions[index])
f=Frame(root)
f.pack(anchor=W)
score_text=Label(root,font="arial 14")
score_text.pack(anchor=W)
button=Button(f,text="Next",font="arial 16 bold",bg="red",command=next_option,width=9)
button.pack(side=RIGHT)
button2=Button(f,text="Previous",font="arial 16 bold",bg="lightblue",command=previous_option,width=9)
button2.pack(side=RIGHT)
root.mainloop()