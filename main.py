import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import time

class DRS:
    def __init__(self):
        self.width=650
        self.height=368
        self.win=tk.Tk()
        self.win.title("Third Umpire")
        self.win.iconphoto(False, tk.PhotoImage(file="Logo.png"))
        self.cv=cv2.cvtColor(cv2.imread("Chinnaswamy_DRS.png"), cv2.COLOR_BGR2RGB)
        self.img=PIL.Image.fromarray(self.cv)
        self.img=self.img.resize((self.width, self.height), PIL.Image.LANCZOS)
        self.photo=PIL.ImageTk.PhotoImage(image=self.img)
        self.canvas=tk.Canvas(self.win, width=self.width, height=self.height)
        self.img_canvas=self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.pack()
        self.stream=cv2.VideoCapture("clip.mp4")

        # Buttons
        self.button1=tk.Button(self.win, text="<<Previous(fast)", width=50, command=partial(self.play, -25))
        self.button1.pack()
        self.button2=tk.Button(self.win, text="<<Previous(slow)", width=50, command=partial(self.play, -2))
        self.button2.pack()
        self.button3=tk.Button(self.win, text="Next(fast)>>", width=50, command=partial(self.play, 25))
        self.button3.pack()
        self.button4=tk.Button(self.win, text="Next(slow)>>", width=50, command=partial(self.play, 0.25))
        self.button4.pack()
        self.button5=tk.Button(self.win, text="OUT", width=50, command=partial(self.out))
        self.button5.pack()
        self.button6=tk.Button(self.win, text="NOT OUT", width=50, command=partial(self.not_out))
        self.button6.pack()
        self.win.mainloop()

    def pending(self,decision):
        self.pending_img=cv2.cvtColor(cv2.imread("Chinnaswamy_Decision_Pending.png"), cv2.COLOR_BGR2RGB)
        self.pending_img=PIL.Image.fromarray(self.pending_img)
        self.pending_img=self.pending_img.resize((self.width, self.height), PIL.Image.LANCZOS)
        self.photo=PIL.ImageTk.PhotoImage(image=self.pending_img)
        self.canvas.itemconfig(self.img_canvas,image=self.photo)

        time.sleep(1)
        if decision=='OUT':
            self.image="Chinnaswamy_OUT.png"
        else:
            self.image="Chinnaswamy_NOT_OUT.png"

        self.pending_img=cv2.cvtColor(cv2.imread(self.image), cv2.COLOR_BGR2RGB)
        self.pending_img=PIL.Image.fromarray(self.pending_img)
        self.pending_img=self.pending_img.resize((self.width, self.height), PIL.Image.LANCZOS)
        self.photo=PIL.ImageTk.PhotoImage(image=self.pending_img)
        self.canvas.itemconfig(self.img_canvas,image=self.photo)

    def play(self, speed):
        frame=self.stream.get(cv2.CAP_PROP_POS_FRAMES)
        self.stream.set(cv2.CAP_PROP_POS_FRAMES, frame+speed)
        grabbed, frame = self.stream.read()

        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame=cv2.resize(frame,(self.width,self.height))
        
        self.photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.itemconfig(self.img_canvas,image=self.photo)
        self.canvas.image=self.photo
    
    def out(self):
        self.thread=threading.Thread(target=self.pending, args=("OUT",))
        self.thread.daemon=1
        self.thread.start()
    
    def not_out(self):
        self.thread=threading.Thread(target=self.pending, args=("NOT OUT",))
        self.thread.daemon=1
        self.thread.start()




drs = DRS()
