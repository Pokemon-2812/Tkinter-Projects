from tkinter import *
import random
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo,askquestion
root=Tk()
root.geometry("400x300")
root.title("Blackjack")
root.configure(bg="green")
game_running=False
sum_num=0
bet=0
deposit=0
def startGame():
    global game_running,sum_num,bet,deposit
    if not(game_running):
        try:
            bet=int(askstring("Bet","How much do you bet?"))
        except Exception as e:
            deposit=10
            bet=5
        game_running=True
        num1=random.randint(1,10)
        num2=random.randint(1,10)
        cards_label.config(text="Cards:"+str(num1)+" "+str(num2))
        sum_num=num1+num2
        sum_label.config(text="Sum: "+str(sum_num))
        checkSum(sum_num)
def checkSum(sumNum):
    global game_running,deposit,bet
    if sumNum>21:
        message.config(text="You're out of the game.")
        game_running=False
        deposit-=bet
        if deposit<0:
            showinfo("Pay",f"Sorry,You have to pay ${deposit}.Game Over")
            continueGame()
        elif deposit==0:
            showinfo("Money Finished",f"Sorry,you have lost all the money deposited.Game Over")
            continueGame()
    elif sumNum==21:
        message.config(text="Congratulations,you got a blackjack!")
        game_running=False
        deposit+=bet
    else:
        message.config(text="Want to draw a new card?")
    money_text.config(text=f"{name}:{deposit}$")
def drawCard():
    global sum_num
    if(game_running):
        cards_text=cards_label.cget("text")
        num=random.randint(1,10)
        sum_num+=num
        cards_label.config(text=cards_text+" " + str(num))
        sum_label.config(text="Sum: "+str(sum_num))
        checkSum(sum_num)
def withdraw():
    global deposit
    showinfo("Withdraw",f"Withdrawing {deposit}$")
    continueGame()
def continueGame():
    ans=askquestion("Continue","Do you want to continue?")
    if(ans=='yes'):
        askDeposit()
    else:
        root.destroy()
def askDeposit():
    global deposit
    try:
        deposit=int(askstring("Deposit","How much money do you deposit?"))
    except Exception as e:
        deposit=10
Label(root,text="Blackjack",fg="orange",font="arial 20 bold",bg="green").pack()
message=Label(root,text="Want to play a round?",fg="white",font="arial 14 italic",bg="green")
message.pack()
cards_label=Label(root,text="Cards:",fg="white",font="arial 14",bg="green")
cards_label.pack()
sum_label=Label(root,text="Sum:",fg="white",font="arial 14",bg="green")
sum_label.pack()
btn1=Button(root,text="Start Game",font="arial 16 bold",fg="green",bg="orange",width=12,command=startGame)
btn1.pack()
btn2=Button(root,text="Draw Card",font="arial 16 bold",fg="green",bg="orange",width=12,command=drawCard)
btn2.pack()
name = askstring('Name', 'What is your name?')
if name==None:
    name="Player"
money_text=Label(root,text=f"{name}:0$",font="arial 16",fg="white",bg="green")
money_text.pack()
askDeposit()
money_text.config(text=f"{name}:{deposit}$")
menubar=Menu(root)
option_menu=Menu(menubar,tearoff=False)
option_menu.add_command(label="Withdraw",command=withdraw)
menubar.add_cascade(label="Options",menu=option_menu)
root.config(menu=menubar)
root.mainloop()