#!/usr/bin/python

from tkinter import *  
from PIL import ImageTk,Image  
import time
from collections import namedtuple
import zmq
import os
from clock import *


# Globals
bg_color     = '#202020'
bg_img       = "birch.jpg"
text_color   = "yellow"
minute_color = "yellow"
logo_color   = "#202020"
text_img     = "art.jpg"
use_img      = False


# zmg server setup
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")


# Window root setup
root = Tk()
root.attributes('-fullscreen', True)
root.overrideredirect(False)
root.wm_attributes("-topmost", 1)
root.focus_set()
root.bind("<Escape>", lambda event:root.destroy())


# Canvas setup
canvas = Canvas(root, bg=bg_color, highlightthickness=0)
canvas.pack(fill=BOTH, expand=True) 


# Positional definitions
root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()

txt_wborder=220
txt_woffset=20
txt_hborder=90
txt_hoffset=25
txt_w = w-2*txt_wborder
txt_h = h-2*txt_hborder
letter_w = (w-2*txt_wborder)/11
letter_h = (h-2*txt_hborder)/10
minute_w = 60
logo_w = 80
logo_h = 90

colors = ["blue","white","#ffff00","yellow","#E99497","#B3E283","#3EDBF0"]

# Image initiation
def update_image_tk():
        global img
        global text_img
        img = Image.open("text_clock/media/text/"+text_img)
        img = img.resize((txt_w,txt_h)) 
        img = ImageTk.PhotoImage(img)

update_image_tk()

def change_image():
        print("Changing image...")
        global text_img
        global img
        global use_img
        use_img = True
        imgs = os.listdir("text_clock/media/text/")
        for i,file in enumerate(imgs):
            if file == text_img: 
                 text_img = imgs[(i+1)%len(imgs)]
                 update_image_tk()
                 print(text_img)
                 use_img = True
                 return
def change_text_color():
        print("Changing colors")
        global colors
        global use_img
        global text_color
        use_img = False
        for i, color in enumerate(colors):
                print(color)
                if color == text_color:
                        print(color)
                        text_color = colors[(i+1)%len(colors)]
                        return
def change_logo_color():
        print("Changing colors")
        global colors
        global logo_color
        for i, color in enumerate(colors):
                print(color)
                if color == logo_color:
                        print(color)
                        logo_color = colors[(i+1)%len(colors)]
                        return
def change_minute_color():
        print("Changing colors")
        global colors
        global minute_color
        for i, color in enumerate(colors):
                print(color)
                if color == minute_color:
                        print(color)
                        minute_color = colors[(i+1)%len(colors)]
                        return
                        
        
letter_rects = []
letter_imgs  = []
minute_rects = []
minute_imgs  = []


for x in range(11):
        new = []
        letter_rects.append(new)
        new2 = []
        letter_imgs.append(new2)
        for y in range(10):
                x0 = txt_wborder+x*letter_w-txt_woffset
                y0 = txt_hborder+y*letter_h-txt_hoffset
                x1 = x0 + letter_w
                y1 = y0 + letter_h
                letter_rects[x].append(canvas.create_rectangle(x0, y0, x1, y1, fill='black'))


Pos = namedtuple("Pos", "x y")
corner1 = Pos(txt_wborder-txt_woffset,     txt_hborder -txt_hoffset)
corner2 = Pos(w - txt_wborder-txt_woffset, txt_hborder - txt_hoffset)
corner3 = Pos(w - txt_wborder-txt_woffset, h - txt_hborder - txt_hoffset)
corner4 = Pos(txt_wborder-txt_woffset,     h - txt_hborder - txt_hoffset)

minute_rects.append(canvas.create_rectangle(corner1.x,corner1.y,corner1.x-minute_w,corner1.y-minute_w))
minute_rects.append(canvas.create_rectangle(corner2.x,corner2.y,corner2.x+minute_w,corner2.y-minute_w))
minute_rects.append(canvas.create_rectangle(corner3.x,corner3.y,corner3.x+minute_w,corner3.y+minute_w))
minute_rects.append(canvas.create_rectangle(corner4.x,corner4.y,corner4.x-minute_w,corner4.y+minute_w))


logo_rect = canvas.create_rectangle(w/2-60,h-90,w/2+40,h,fill="black")



def set_logo(c):
     canvas.itemconfig(logo_rect, fill=c)
def set_minute(m,c):
        canvas.itemconfig(minute_rects[m-1], fill=c)
def set_letter(x,y,c):
        canvas.itemconfig(letter_rects[x][y], fill=c)
def set_letter_img(x,y,c):
        canvas.itemconfig(letter_rects[x][y], fill="#ABABAB")
        global canvas_image
        try:
                canvas.delete(canvas_image)
        except:
                pass
        canvas_image = canvas.create_image(corner1.x, corner1.y, anchor=NW, image=img)
        for x in range(11):
                for y in range(10):
                        curr_color= canvas.itemcget(letter_rects[x][y], "fill")
                        if curr_color != "#ABABAB":
                                x0 = txt_wborder+x*letter_w
                                y0 = txt_hborder+y*letter_h-txt_hoffset
                                x1 = x0 + letter_w
                                y1 = y0 + letter_h
                                canvas.delete(letter_rects[x][y])
                                letter_rects[x][y]=canvas.create_rectangle(x0, y0, x1, y1, fill=curr_color)
                                

def update_clock():
        global logo_color
        global use_img
        # Handle requests from user
        while(True):
                try:
                        print("Looking for input...")
                        msg = socket.recv(flags = zmq.NOBLOCK)
                        handle_user_msg(msg)
                        print("Recieved input!")
                except:
                        print("No recieved input!")
                        break
        clear_clock(bg_color, set_letter, set_minute)
        if(use_img):
                write_time(text_color,minute_color,set_letter_img, set_minute)
        else:
                global canvas_image
                try:
                        canvas.delete(canvas_image)
                except:
                        pass
                write_time(text_color,minute_color,set_letter, set_minute)
        write_am_pm("#202020","#202020",set_letter)
        set_logo(logo_color)
        root.after(500, update_clock)


def handle_user_msg(msg):
        if(msg == b"img"):
                change_image()
        if(msg == b"txtcol"):
                print("Color change")
                change_text_color()
        if(msg == b"logocol"):
                change_logo_color()
        if(msg == b"mincol"):
                change_minute_color()
        if(msg == "alarm_off"):
                #alarm_off()
                pass
        if(msg == "snake_left"):
                #snake_left()
                pass
        if(msg == "snake_right"):
                #snake_right()
                pass



root.after(500,update_clock)
root.mainloop()
