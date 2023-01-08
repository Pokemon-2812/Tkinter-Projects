from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
from tkinter.filedialog import askopenfilename,asksaveasfilename
import os
import re
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
import subprocess
import sys
class Notepad(Tk):
    def __init__(self,title,height,width):
        super().__init__()
        self.titles=title
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.scrollbar=Scrollbar()
        self.run=False
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.text_area=Text(self,font="lucida 13",height = 700,yscrollcommand=self.scrollbar.set,undo=True,cursor="xterm white")
        self.text_area2=Text(self,bg="#1d1f21",fg="#c5c8c6",font=self.text_area["font"],width=2,yscrollcommand=self.scrollbar.set)
        self.text_area2.pack(anchor=NW,side=LEFT,fill=Y)
        self.text_area.pack(fill=BOTH)
        self.text_area2.config(state=DISABLED)
        self.scrollbar.config(command=self.viewall)
        self.file=None
        self.highlighted=True
        self.linenumbers()
        self.syntax_highlight()
        self.add_menus()
        self.n=StringVar()
        self.o=IntVar()
        self.p=StringVar()
        self.bind_events()
    def viewall(self,*args):
        self.text_area.yview(*args)
        self.text_area2.yview(*args)
    def syntax_highlight(self):
        if self.file is not None:
            if self.highlighted:
                Percolator(self.text_area).insertfilter(ColorDelegator())
                self.highlighted=False
    def linenumbers(self,event=''):
        self.final_index=int(float(self.text_area.index(END)))
        self.indexs=""
        for index in range(1,self.final_index+1):
            self.indexs+=f"{index}\n"
        self.text_area2.config(state='normal')
        self.text_area2.delete(1.0,END)
        self.text_area2.insert(1.0,self.indexs)
        self.text_area2.config(width=len(str(self.final_index-1)),state='disabled')
    def boilerplate(self,event):
        widget=event.widget
        line=widget.get("insert linestart","insert lineend")
        text="""<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        </head>
        <body>
        </body>
        </html>"""
        widget.insert("insert",event.char+text)
        return "break"
    def autoindent(self,event):
        #Get the widget on which this function was called
        widget=event.widget
        #Get current line
        line=widget.get("insert linestart","insert lineend")
        #Find the current indenation of the line
        match=re.match(r'^(\s+)',line)
        current_indent=len(match.group(0)) if match else 0
        #Do new indentation
        new_indent=current_indent+4
        #Insert a newline and then an indent
        widget.insert("insert",event.char+"\n"+" "*new_indent)
        #return break to prevent default behaviour
        return "break"
    def copylinedown(self,event):
        widget=event.widget
        line=widget.get("insert linestart","insert lineend")
        widget.insert("insert",event.char+"\n"+line)
        return "break"
    def bind_events(self):
        self.text_area.bind('<Return>',self.linenumbers)
        self.text_area.bind('<Button-1>',self.linenumbers)
        self.text_area.bind(':',self.autoindent)
        self.bind('<Control-S>',self.saveasfile)
        self.bind('<Control-s>',self.savefile)
        self.bind('<Control-n>',self.newfile)
        self.bind('<Control-o>',self.openfile)
        self.bind('<Control-Return>',self.runfile)
        self.text_area.bind('<Control-d>',self.copylinedown)
        self.text_area.bind('<Control-k>',self.fontstyle)
        self.bind('<Escape>',self.exitfile)
    def html(self):
        if self.file.endswith(".html"):
            self.text_area.bind("<Control-l>",self.boilerplate)
    def newfile(self,event=''):
        self.title(f"Untitled-{self.titles}")
        self.file=None
        self.text_area.delete(1.0,END)
    def openfile(self,event=''):
        self.file=askopenfilename(defaultextension=".txt",filetypes=[("Python File","*.py"),("HTML File","*.html"),
        ("Css File","*.css"),("Text Documents","*.txt"),("All Files","*.*")])
        if self.file=="" :
            self.file=None
        else:
            self.html()
            self.syntax_highlight()
            self.title(os.path.basename(self.file)+ "-" + self.titles)
            self.text_area.delete(1.0,END)
            with open(self.file) as f:
                self.text_area.insert(1.0,f.read())
            self.linenumbers()
    def writefile(self):
        with open(self.file,'w') as f:
            f.write(self.text_area.get(1.0,END))
    def saveasfile(self,event=''):
        if self.file==None:
            self.file=asksaveasfilename(initialfile="Untitled-1.txt",defaultextension=".txt",filetypes=[("Python File","*.py"),("HTML File","*.html"),("Css File","*.css"),("Text Documents","*.txt"),("All Files","*.*")])
            if self.file=="":
                self.file=None
            else:
                self.html()
                self.writefile()
                self.title(os.path.basename(file)+ self.titles)
    def savefile(self,event=''):
        if self.file:
            try:
                self.writefile()
            except Exception:
                pass
        else:
            self.saveasfile()
    def exitfile(self,event=''):
        if self.file==None:
            ans=tmsg.askyesno("Exit","Do you want to exit without saving?\nPress no to save and the quit.")
            if ans:
                self.destroy()
            else:
                self.savefile()
        else:
            self.destroy()
    def cut(self):
        self.text_area.event_generate(("<<Cut>>"))
    def copy(self):
        self.text_area.event_generate(("<<Copy>>"))
    def paste(self):
        self.text_area.event_generate(("<<Paste>>"))
    def AboutNotepad(self):
        tmsg.showinfo("About","This is a simple text editor made by Ishaan.")
    def change_font(self):
        if self.p.get()=='Regular':
            fonts=(self.n.get(),self.o.get())
        else:
            fonts=(self.n.get(),self.o.get(),self.p.get())
        self.text_area2.config(font=fonts)
        self.text_area.config(font=fonts)
    def fontstyle(self,event=''):
        top=Toplevel(self)
        top.geometry("500x400")
        Label(top,text="Font Style",font="lucida 15 bold").grid(row=0,column=0)
        Label(top,text="Font Size",font="lucida 15 bold").grid(row=1,column=0)
        Label(top,text="Font Type",font="lucida 15 bold").grid(row=2,column=0)
        combobox1=ttk.Combobox(top,width=24,textvariable=self.n)
        combobox2=ttk.Combobox(top,width=24,textvariable=self.o)
        combobox3=ttk.Combobox(top,width=24,textvariable=self.p)
        combobox1['values']=('helvetica','calibri','futura','garamond','times new roman','arial','cambria','verdana','rockwell','franklin gothic',
        'lucida')
        combobox3['values']=('Regular','bold','italic','underline')
        nums=[]
        for i in range(11,40,1):
            nums.append(i)
        nums=tuple(nums)
        combobox2['values']=nums
        combobox1.grid(row=0,column=1)
        combobox2.grid(row=1,column=1)
        combobox3.grid(row=2,column=1)
        self.n.set('lucida')
        self.o.set(13)
        self.p.set('Regular')
        Button(top,text="Change Font",bg="red",command=self.change_font,font="lucida 12 bold").grid(row=3,column=0)
        top.mainloop()
    def runfile(self,event=''):
        if not(self.run):
            self.terminal=Toplevel(self)
            self.terminal.geometry("500x400")
            self.terminal.title("Run Code")
            self.run_text=Text(self.terminal,font="lucida 13",state=DISABLED)
            self.run_text.pack()
            self.result=subprocess.run([sys.executable, "-c", self.text_area.get(1.0,END)],capture_output=True,text=True)
            self.run_text.config(state=NORMAL)
            self.run_text.insert(1.0,self.result.stdout)
            self.run=True
        else:
            self.result=subprocess.run([sys.executable, "-c", self.text_area.get(1.0,END)],capture_output=True,text=True)
            self.run_text.delete(1.0,END)
            self.run_text.insert(1.0,self.result.stdout)
    def newterminal(self):
        self.terminal=Toplevel(self)
        self.terminal.geometry("500x400")
        self.terminal.title("Run Code")
        self.run_text=Text(self.terminal,font="lucida 13",state=DISABLED)
        self.run_text.pack()
    def add_menus(self):
        menu=Menu(self)
        FileMenu=Menu(menu,tearoff=0)
        FileMenu.add_command(label="New",command=self.newfile)
        FileMenu.add_command(label="Open",command=self.openfile)
        FileMenu.add_command(label="Save As",command=self.saveasfile)
        FileMenu.add_command(label="Save",command=self.savefile)
        FileMenu.add_separator()
        FileMenu.add_command(label="Run",command=self.runfile)
        FileMenu.add_command(label="New Terminal",command=self.newterminal)
        FileMenu.add_command(label="Exit",command=self.exitfile)

        EditMenu=Menu(menu,tearoff=0)
        EditMenu.add_command(label="Cut",command=self.cut)
        EditMenu.add_command(label="Copy",command=self.copy)
        EditMenu.add_command(label="Paste",command=self.paste)

        Helpmenu=Menu(menu,tearoff=0)
        Helpmenu.add_command(label="about",command=self.AboutNotepad)
  
        Fontmenu=Menu(menu,tearoff=0)
        Fontmenu.add_command(label="Font...",command=self.fontstyle)

        self.config(menu=menu)
        menu.add_cascade(label="File",menu=FileMenu)
        menu.add_cascade(label="Edit",menu=EditMenu)
        menu.add_cascade(label="Help",menu=Helpmenu)
        menu.add_cascade(label="Format",menu=Fontmenu)