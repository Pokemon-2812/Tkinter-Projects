from notepadclass import Notepad
from PIL import Image,ImageTk
if __name__=="__main__":
    pycode=Notepad("Pycode",600,900)
    image=Image.open('notepad2.png')
    photo=ImageTk.PhotoImage(image)
    pycode.tk.call('wm', 'iconphoto', pycode._w, photo)
    pycode.mainloop()