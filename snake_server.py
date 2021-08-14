#!/usr/bin/python

from tkinter import *  
from PIL import ImageTk,Image  
import time
from collections import namedtuple
import zmq
import os
from clock import *
from random import randint


# Globals
bg_color     = '#202020'
text_color   = "yellow"
minute_color = "yellow"
logo_color   = "#202020"


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





                        
        
letter_rects = []
minute_rects = []


for x in range(11):
        new = []
        letter_rects.append(new)
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

#Snake
start = False
body = [Pos(0,0)]
dir = "right"
apple = Pos(5,5)

def move_snake():
    for i in range(len(body)-1,-1,-1):
        if(i == 0):
            if(dir == "right"):
                body[i] = body[i]._replace(x=(body[0].x+1)%11) 
            if(dir == "left"):
                body[i] = body[i]._replace(x=(body[0].x-1)%11) 
            if(dir == "up"):
                body[i] = body[i]._replace(y=(body[0].y+1)%10) 
            if(dir == "down"):
                body[i] = body[i]._replace(y=(body[0].y-1)%10) 
        else:
            body[i]=body[i-1]

def move_apple():
    global apple
    apple = apple._replace(x=randint(0,10))
    apple = apple._replace(y=randint(0,9))
    print(apple.x)
    print(apple.y)
def draw_game():
    if(body[0] == apple):
        body.append(body[-1])
        move_apple()
    set_letter(apple.x,apple.y,"red")
    move_snake()
    if(body[0].x == 11 or body[0].x == -1 or body[0].y == 10 or body[0].y == -1):
        #exit()
        pass
    for b in body:
        set_letter(b.x,b.y,"#48ff00")


def snake_left():
    global start
    global dir
    start = True
    if(dir == "right"):
        dir = "up"
        return
    if(dir == "left"):
        dir = "down"
        return
    if(dir == "up"):
        dir = "left"
        return
    if(dir == "down"):
        dir = "right"
        return

def snake_right():
    global start
    global dir
    start = True
    if(dir == "right"):
        dir = "down"
        return
    if(dir == "left"):
        dir = "up"
        return
    if(dir == "up"):
        dir = "right"
        return
    if(dir == "down"):
        dir = "left"
        return

def update_clock():
        while(True):
                try:
                    msg = socket.recv(flags = zmq.NOBLOCK)
                    handle_user_msg(msg)
                except:
                    break
        clear_clock(bg_color, set_letter, set_minute)
        if(start):
            draw_game()
        root.after(200, update_clock)

def key(event):
    """shows key or tk code for the key"""
    if event.keysym == 'Escape':
        root.destroy()
    if event.keysym == 'Right':
            snake_left()
    if event.keysym == 'Left':
            snake_right()


def handle_user_msg(msg):
        if(msg == b"left"):
                snake_left()
                pass
        if(msg == b"right"):
                snake_right()
                pass

root.bind_all('<Key>', key)
root.after(200,update_clock)
root.mainloop()
