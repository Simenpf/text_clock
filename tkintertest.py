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
text_color   = "yellow"
minute_color = "yellow"
logo_color   = bg_color
am_color     = bg_color
pm_color     = bg_color
text_img     = "art.jpg"
use_img      = False
text_r       = 0
text_g       = 0
text_b       = 0

def use_text_rgb():
        global text_color
        rgb = (text_r, text_g, text_b)
        text_color = "#%02x%02x%02x" % rgb   


# zmg server setup (For app interface)
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")

# User interface
def key(event):
    """shows key or tk code for the key"""
    if event.keysym == 'Escape':
        root.destroy()
    if event.keysym == 'Right':
            print("Left")
    if event.keysym == 'Left':
            print("Right")
    if event.keysym == 'r':
            global text_r
            text_r = (text_r+4)%255
            use_text_rgb()
    if event.keysym == 'g':
            global text_g
            text_g = (text_g+4)%255
            use_text_rgb()
    if event.keysym == 'b':
            global text_b
            text_b = (text_b+4)%255
            use_text_rgb()
    if event.keysym == 'p':
            print("Current colors:")
            print("R: "+str(text_r))
            print("G: "+str(text_g))
            print("B: "+str(text_b))


# Window root setup
root = Tk()
root.attributes('-fullscreen', True)
root.bind_all('<Key>', key)


# Canvas setup
canvas = Canvas(root, bg=bg_color, highlightthickness=0)
canvas.pack(fill=BOTH, expand=True) 


# Positional definitions (in pixels)
root.update_idletasks() #Update hight and width data
w = root.winfo_width()
h = root.winfo_height()

txt_wborder=220                 #Distance from left and right side, to the closest letter
txt_woffset=20                  #The horisontal shift of the text (if monitor is not horizontally centered behind text)
txt_hborder=90                  #Distance from top and bottom, to the closest letter
txt_hoffset=25                  #The vertical shift of the text (if monitor is not vertically sentered behind text)
txt_w = w-2*txt_wborder         #Total width of text-block
txt_h = h-2*txt_hborder         #Total height of text-block
letter_w = (w-2*txt_wborder)/11 #Width of a letter
letter_h = (h-2*txt_hborder)/10 #Height of a letter
minute_w = 60                   #Width of a minute-dot
logo_w = 80                     #Width of the logo
logo_h = 90                     #Height of the logo

# Should be themes to choose from in app
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
        global text_img
        global img
        global use_img
        use_img = True
        imgs = os.listdir("text_clock/media/text/")
        for i,file in enumerate(imgs):
            if file == text_img: 
                 text_img = imgs[(i+1)%len(imgs)]
                 update_image_tk()
                 use_img = True
                 return

def change_text_color():
        global colors
        global use_img
        global text_color
        use_img = False
        for i, color in enumerate(colors):
                if color == text_color:
                        text_color = colors[(i+1)%len(colors)]
                        return

def change_logo_color():
        global colors
        global logo_color
        for i, color in enumerate(colors):
                if color == logo_color:
                        logo_color = colors[(i+1)%len(colors)]
                        return

def change_minute_color():
        global colors
        global minute_color
        for i, color in enumerate(colors):
                if color == minute_color:
                        minute_color = colors[(i+1)%len(colors)]
                        return
                        

# Tkinter objects initiation 
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
                        msg = socket.recv(flags = zmq.NOBLOCK)
                        handle_user_msg(msg)
                except:
                        break

        #Clear screen and redraw
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

        write_am_pm(am_color,pm_color,set_letter)
        set_logo(logo_color) 
        root.after(100, update_clock)


def handle_user_msg(msg):
        if(msg == b"img"):
                change_image()
        if(msg == b"txtcol"):
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

root.after(100,update_clock)
root.mainloop()
