#!/usr/bin/python

from tkinter import *  
from PIL import ImageTk,Image  
import time
from datetime import datetime
from collections import namedtuple
import zmq
import os

def get_image(img, type):
        img = Image.open("text_clock/media/"+img)
        if type == "text":
               img = img.resize((txt_w,txt_h)) 
        if type == "minute":
                img = img.resize((minute_w,minute_w))
        if type == "logo":
                img = img.resize((logo_w,logo_h))
        return ImageTk.PhotoImage(img)

# Globals
text_color   = "white"
minute_color = "white"
logo_color   = "white"
text_img     = "text/art.jpg"
use_img      = True
global img


# zmg server setup
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
global msg


# Window root setup
root = Tk()
root.attributes('-fullscreen', True)
root.overrideredirect(False)
root.wm_attributes("-topmost", 1)
root.focus_set()
root.bind("<Escape>", lambda event:root.destroy())

# Canvas setup
canvas = Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill=BOTH, expand=True) 

# Positional definitions
root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
txt_wborder=220
txt_hborder=90
txt_hoffset=25
txt_w = w-2*txt_wborder
txt_h = h-2*txt_hborder
letter_w = (w-2*txt_wborder)/11
letter_h = (h-2*txt_hborder)/10
minute_w = 60
logo_w = 80
logo_h = 90



# Image initiation



def change_image(type):
        imgs = os.listdir("text_clock/media/"+type)
        for i,file in enumerate(imgs):
            if file == text_img: 
                 text_img = imgs[(i+1)%len(imgs)]
        img = get_image(text_img,"text")
        use_img = True

cropped_tk_imgs = []
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
                x0 = txt_wborder+x*letter_w
                y0 = txt_hborder+y*letter_h-txt_hoffset
                x1 = x0 + letter_w
                y1 = y0 + letter_h
                letter_rects[x].append(canvas.create_rectangle(x0, y0, x1, y1, fill='black'))


Pos = namedtuple("Pos", "x y")
corner1 = Pos(txt_wborder,     txt_hborder -txt_hoffset)
corner2 = Pos(w - txt_wborder, txt_hborder - txt_hoffset)
corner3 = Pos(w - txt_wborder, h - txt_hborder - txt_hoffset)
corner4 = Pos(txt_wborder,     h - txt_hborder - txt_hoffset)

minute_rects.append(canvas.create_rectangle(corner1.x,corner1.y,corner1.x-minute_w,corner1.y-minute_w))
minute_rects.append(canvas.create_rectangle(corner2.x,corner2.y,corner2.x+minute_w,corner2.y-minute_w))
minute_rects.append(canvas.create_rectangle(corner3.x,corner3.y,corner3.x+minute_w,corner3.y+minute_w))
minute_rects.append(canvas.create_rectangle(corner4.x,corner4.y,corner4.x-minute_w,corner4.y+minute_w))

#minute_imgs.append(canvas.create_image(corner1.x,corner1.y, anchor=SE, image=img))
#minute_imgs.append(canvas.create_image(corner2.x,corner2.y, anchor=SW, image=img))
#minute_imgs.append(canvas.create_image(corner3.x,corner3.y, anchor=NW, image=img))
#minute_imgs.append(canvas.create_image(corner4.x,corner4.y, anchor=NE, image=img))

logo_rect = canvas.create_rectangle(w/2-40,h-90,w/2+40,h,fill="black")
#logo_img  = canvas.create_image(w/2-40,h-90, anchor=NW, image=img)



def set_logo(c):
     canvas.itemconfig(logo_rect, fill=c)
def set_logo_img(img):
     canvas.itemconfig(logo_img, image=img)

def set_minute(m,c):
        canvas.itemconfig(minute_rects[m-1], fill=c)
def set_minutes(m,c):
        if m == 1:
                set_minute(1,c)
        if m == 2:
                set_minute(1,c)
                set_minute(2,c)
        if m == 3:
                set_minute(1,c)
                set_minute(2,c)
                set_minute(3,c)
        if m == 4:
                set_minute(1,c)
                set_minute(2,c)
                set_minute(3,c)
                set_minute(4,c)

def set_letter(x,y,c):
        canvas.itemconfig(letter_rects[x][y], fill=c)
def set_letter_img(x,y,c):
        set_letter(x,y,"#ABABAB")
        canvas.create_image(corner1.x,corner1.y, anchor=NW, image=img)
        for x in range(11):
                for y in range(10):
                        curr_color= canvas.itemcget(letter_rects[x][y], "fill")
                        if curr_color != "#ABABAB":
                                x0 = txt_wborder+x*letter_w
                                y0 = txt_hborder+y*letter_h-txt_hoffset
                                x1 = x0 + letter_w
                                y1 = y0 + letter_h
                                letter_rects[x].append(canvas.create_rectangle(x0, y0, x1, y1, fill=curr_color))
                                

def set_letters(letters,c,set_letter):
        for l in letters:
                set_letter(l[0],l[1],c)

def set_all_letters(c,set_letter):
        for x in range(11):
                for y in range(10):
                        set_letter(x,y,c)
def write(word,c,set_letter):
                if word == "it":
                        set_letters([[0,0],[1,0]],c,set_letter)
                elif word == "is":
                        set_letters([[3,0],[4,0]],c,set_letter)
                elif word == "am":
                        set_letters([[7,0],[8,0]],c,set_letter)                   
                elif word == "pm":
                        set_letters([[9,0],[10,0]],c,set_letter)
                elif word == "a":
                        set_letters([[0,1]],c,set_letter)
                elif word == "quarter":
                        set_letters([[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1]],c,set_letter)
                elif word == "twenty":
                        set_letters([[0,2],[1,2],[2,2],[3,2],[4,2],[5,2]],c,set_letter)
                elif word == "five1":
                        set_letters([[6,2],[7,2],[8,2],[9,2]],c,set_letter)
                elif word == "half":
                        set_letters([[0,3],[1,3],[2,3],[3,3]],c,set_letter)
                elif word == "ten1":
                        set_letters([[5,3],[6,3],[7,3]],c,set_letter)
                elif word == "to":
                        set_letters([[9,3],[10,3]],c,set_letter)
                elif word == "past":
                        set_letters([[0,4],[1,4],[2,4],[3,4]],c,set_letter)
                elif word == "one":
                        set_letters([[0,5],[1,5],[2,5]],c,set_letter)
                elif word == "two":
                        set_letters([[8,6],[9,6],[10,6]],c,set_letter)
                elif word == "three":
                        set_letters([[6,5],[7,5],[8,5],[9,5],[10,5]],c,set_letter)
                elif word == "four":
                        set_letters([[0,6],[1,6],[2,6],[3,6]],c,set_letter)
                elif word == "five":
                        set_letters([[4,6],[5,6],[6,6],[7,6]],c,set_letter)
                elif word == "six":
                        set_letters([[3,5],[4,5],[5,5]],c,set_letter)
                elif word == "seven":
                        set_letters([[0,8],[1,8],[2,8],[3,8],[4,8]],c,set_letter)
                elif word == "eight":
                        set_letters([[0,7],[1,7],[2,7],[3,7],[4,7]],c,set_letter)
                elif word == "nine":
                        set_letters([[7,4],[8,4],[9,4],[10,4]],c,set_letter)
                elif word == "ten":
                        set_letters([[0,9],[1,9],[2,9]],c,set_letter)
                elif word == "eleven":
                        set_letters([[5,7],[6,7],[7,7],[8,7],[9,7],[10,7]],c,set_letter)
                elif word == "twelve":
                        set_letters([[5,8],[6,8],[7,8],[8,8],[9,8],[10,8]],c,set_letter)
def write_sentence(words,c,set_letter):
        for word in words:
                write(word,c,set_letter)

def write_time(c,c2,set_letter):
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    #For testing
    #hour = 15
    #minute = 16


    # It is
    write("it",c,set_letter)
    write("is",c,set_letter)

    # five, ten, quarter, twenty, twentyfive, half
    minute_block = minute // 5
    if minute_block == 0:
        pass
    elif minute_block == 1 or minute_block == 11:
        write("five1",c,set_letter)
    elif minute_block == 2 or minute_block == 10:
        write("ten1",c,set_letter)
    elif minute_block == 3 or minute_block == 9:
        write("quarter",c,set_letter)
    elif minute_block == 4 or minute_block == 8:
        write("twenty",c,set_letter)
    elif minute_block == 5 or minute_block == 7:
        write_sentence(["twenty","five1"],c,set_letter)
    elif minute_block == 6:
        write("half",c,set_letter)

    # Past, to or whole hour
    if(minute >= 35 ):
        write("to",c,set_letter)
        hour+=1
    elif(minute >= 5):
        write("past",c,set_letter)
        

    # one, two, three, ...
    if (hour == 1) or (hour == 13):
        write("one",c,set_letter)
    elif (hour == 2) or (hour == 14):
        write("two",c,set_letter)
    elif (hour == 3) or (hour == 15):
        write("three",c,set_letter)
    elif (hour == 4) or (hour == 16):
        write("four",c,set_letter)
    elif (hour == 5) or (hour == 17):
        write("five",c,set_letter)
    elif (hour == 6) or (hour == 18):
        write("six",c,set_letter)
    elif (hour == 7) or (hour == 19):
        write("seven",c,set_letter)
    elif (hour == 8) or (hour == 20):
        write("eight",c,set_letter)
    elif (hour == 9) or (hour == 21):
        write("nine",c,set_letter)
    elif (hour == 10) or (hour == 22):
        write("ten",c,set_letter)
    elif (hour == 11) or (hour == 23):
        write("eleven",c,set_letter)
    elif (hour == 12) or (hour == 24):
        write("twelwe",c,set_letter)

    # Extra minutes
    surplus_minutes = minute % 5
    if surplus_minutes == 1:
            set_minutes(1,c2)
    elif surplus_minutes == 2:
            set_minutes(2,c2)
    elif surplus_minutes == 3:
            set_minutes(3,c2)
    elif surplus_minutes == 4:
            set_minutes(4,c2)


def write_am_pm(c_am,c_pm,set_letter):
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    #For testing
    #hour = 15
    #minute = 16

    # AM or PM
    if(hour>12):
        write("pm",c_pm,set_letter)
    else:
        write("am",c_am,set_letter)
def clear_clock():
     set_all_letters("black",set_letter)
     set_minutes(4,"black")
def update_clock():
        # Handle requests from user
        while(True):
                try:
                        msg = socket.recv(flags = zmq.NOBLOCK)
                        handle_user_msg(msg)
                except:
                        break

        clear_clock()
        if(use_img):
                write_time(text_color,minute_color,set_letter_img)
        else:
                write_time(text_color,minute_color,set_letter)   
        write_am_pm("#909090","#707070",set_letter)
        sec = datetime.now().second
        set_logo(logo_color)
        root.after(500, update_clock)

def handle_user_msg(msg):
        if(msg == "img"):
                print("!")
                change_image()
        if(msg == "color_change"):
                #change_color()
                pass
        if(msg == "alarm_off"):
                #alarm_off()
                pass
        if(msg == "snake_left"):
                #snake_left()
                pass
        if(msg == "snake_right"):
                #snake_right()
                pass


img = get_image(text_img,"text")
root.after(500,update_clock)
root.mainloop()

     



