from tkinter import *
from tkinter.filedialog import askopenfile
from pygame import mixer
import json
root=Tk()
root.geometry("500x400")
root.title("Music Player")
file=None
mixer.init()
def add():
    global file
    file = askopenfile(defaultextension='.wav', filetypes =[('Wav Files', '*.wav'),("Mp3 Files",'*.mp3'),("Mp4 Files",'*.mp4'),("All Files","*.*")])
    if file=="":
        file=None
    if file!=None:
        if not(file.name in songs):
            song_name=file.name.split("/")[len(file.name.split("/"))-1]
            lbx.insert(END,song_name)
            songs.append(file.name)
            short_songs[song_name]=file.name
def play():
    global file
    for i in lbx.curselection():
        if lbx.get(i)!=None:
            file=short_songs[lbx.get(i)]
    if file!=None:
        try:
            mixer.music.load(file)
            root.title("Music Player - "+ file)
            mixer.music.play()
        except Exception as e:
            pass
def delete():
    selected_songs=lbx.curselection()
    for song in selected_songs:
        songs.remove(short_songs[lbx.get(song)])
        lbx.delete(song)
    save()
def save():
    with open('songs.json','w') as f:
        json.dump(songs,f)
try:
    with open('songs.json','r') as f:
        songs=json.load(f)
except Exception as e:
    songs=[]
Label(root,text="Playlist",font="arial 22 bold").pack()
scrollbar=Scrollbar(root)
scrollbar.pack(fill=Y,side=RIGHT)
lbx=Listbox(root,yscrollcommand=scrollbar.set)
lbx.pack(fill=X)
scrollbar.config(command=lbx.yview)
short_songs={}
for song in songs:
    if "/" in song:
        song_name=song.split("/")[len(song.split("/"))-1]
    else:
        song_name=song
    short_songs[song_name]=song
    lbx.insert(END,song_name)
btn1=Button(root,text="Add",font="arial 16",fg="white",bg="red",width=9,command=add)
btn1.pack()
btn2=Button(root,text="Delete",font="arial 16",fg="white",bg="green",width=9,command=delete)
btn2.pack()
btn3=Button(root,text="Save",font="arial 16",fg="white",bg="orange",width=9,command=save)
btn3.pack()
btn4=Button(root,text="Play Sound",font="arial 16",fg="white",bg="blue",width=9,command=play)
btn4.pack()
root.mainloop()