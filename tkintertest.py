#!/usr/bin/python

from tkinter import *  
from PIL import ImageTk,Image  
import time
from datetime import datetime
from collections import namedtuple

# Root setup
root = Tk()
root.attributes('-fullscreen', True)
root.overrideredirect(False)
root.wm_attributes("-topmost", 1)
root.focus_set()
root.bind("<Escape>", lambda event:root.destroy())

# Canvas setup
canvas = Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill=BOTH, expand=True) 

# Positional arguments
root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
print(w)
print(h)
txt_wborder=220
txt_hborder=90
txt_hoffset=25
letter_w = (w-2*txt_wborder)/11
letter_h = (h-2*txt_hborder)/10
minute_w = 60

#img = ImageTk.PhotoImage(Image.open("media/test.png")) 

letter_rects = []
letter_imgs  = []
minute_rects = []
minute_imgs  = []


for x in range(11):
        new = []
        letter_rects.append(new)
        letter_imgs.append(new)
        for y in range(10):
                x0 = txt_wborder+x*letter_w
                y0 = txt_hborder+y*letter_h-txt_hoffset
                x1 = x0 + letter_w
                y1 = y0 + letter_h
                letter_rects[x].append(canvas.create_rectangle(x0, y0, x1, y1, fill='black'))
                #letter_imgs.append(canvas.create_image(x0,y0, anchor=NW, image=img))

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
def set_letters(letters,c):
        for l in letters:
                set_letter(l[0],l[1],c)
def set_all_letters(c):
        for x in range(11):
                for y in range(10):
                        set_letter(x,y,c)
def write(word,c):
                if word == "it":
                        set_letters([[0,0],[1,0]],c)
                elif word == "is":
                        set_letters([[3,0],[4,0]],c)
                elif word == "am":
                        set_letters([[7,0],[8,0]],c)                   
                elif word == "pm":
                        set_letters([[9,0],[10,0]],c)
                elif word == "a":
                        set_letters([[0,1]],c)
                elif word == "quarter":
                        set_letters([[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1]],c)
                elif word == "twenty":
                        set_letters([[0,2],[1,2],[2,2],[3,2],[4,2],[5,2]],c)
                elif word == "five1":
                        set_letters([[6,2],[7,2],[8,2],[9,2]],c)
                elif word == "half":
                        set_letters([[0,3],[1,3],[2,3],[3,3]],c)
                elif word == "ten1":
                        set_letters([[5,3],[6,3],[7,3]],c)
                elif word == "to":
                        set_letters([[9,3],[10,3]],c)
                elif word == "past":
                        set_letters([[0,4],[1,4],[2,4],[3,4]],c)
                elif word == "one":
                        set_letters([[0,5],[1,5],[2,5]],c)
                elif word == "two":
                        set_letters([[8,6],[9,6],[10,6]],c)
                elif word == "three":
                        set_letters([[6,5],[7,5],[8,5],[9,5],[10,5]],c)
                elif word == "four":
                        set_letters([[0,6],[1,6],[2,6],[3,6]],c)
                elif word == "five":
                        set_letters([[4,6],[5,6],[6,6],[7,6]],c)
                elif word == "six":
                        set_letters([[3,5],[4,5],[5,5]],c)
                elif word == "seven":
                        set_letters([[0,8],[1,8],[2,8],[3,8],[4,8]],c)
                elif word == "eight":
                        set_letters([[0,7],[1,7],[2,7],[3,7],[4,7]],c)
                elif word == "nine":
                        set_letters([[7,4],[8,4],[9,4],[10,4]],c)
                elif word == "ten":
                        set_letters([[0,9],[1,9],[2,9]],c)
                elif word == "eleven":
                        set_letters([[5,7],[6,7],[7,7],[8,7],[9,7],[10,7]],c)
                elif word == "twelve":
                        set_letters([[5,8],[6,8],[7,8],[8,8],[9,8],[10,8]],c)
def write_sentence(words,c):
        for word in words:
                write(word,c)

def write_time(c,c2):
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    #For testing
    #hour = 15
    #minute = 16


    # It is
    write("it",c)
    write("is",c)

    # five, ten, quarter, twenty, twentyfive, half
    minute_block = minute // 5
    if minute_block == 0:
        pass
    elif minute_block == 1 or minute_block == 11:
        write("five1",c)
    elif minute_block == 2 or minute_block == 10:
        write("ten1",c)
    elif minute_block == 3 or minute_block == 9:
        write("quarter",c)
    elif minute_block == 4 or minute_block == 8:
        write("twenty",c)
    elif minute_block == 5 or minute_block == 7:
        write_sentence(["twenty","five1"],c)
    elif minute_block == 6:
        write("half",c)

    # Past, to or whole hour
    if(minute >= 35 ):
        write("to",c)
        hour+=1
    elif(minute >= 5):
        write("past",c)
        

    # one, two, three, ...
    if (hour == 1) or (hour == 13):
        write("one",c)
    elif (hour == 2) or (hour == 14):
        write("two",c)
    elif (hour == 3) or (hour == 15):
        write("three",c)
    elif (hour == 4) or (hour == 16):
        write("four",c)
    elif (hour == 5) or (hour == 17):
        write("five",c)
    elif (hour == 6) or (hour == 18):
        write("six",c)
    elif (hour == 7) or (hour == 19):
        write("seven",c)
    elif (hour == 8) or (hour == 20):
        write("eight",c)
    elif (hour == 9) or (hour == 21):
        write("nine",c)
    elif (hour == 10) or (hour == 22):
        write("ten",c)
    elif (hour == 11) or (hour == 23):
        write("eleven",c)
    elif (hour == 12) or (hour == 24):
        write("twelwe",c)

    # Extra minutes
    surplus_minutes = minute % 5
    if minute < 35:
         if surplus_minutes == 1:
             set_minutes(1,c2)
         elif surplus_minutes == 2:
             set_minutes(2,c2)
         elif surplus_minutes == 3:
             set_minutes(3,c2)
         elif surplus_minutes == 4:
             set_minutes(4,c2)
    else:
         if surplus_minutes == 1:
             set_minutes(4,c2)
         elif surplus_minutes == 2:
             set_minutes(3,c2)
         elif surplus_minutes == 3:
             set_minutes(2,c2)
         elif surplus_minutes == 4:
             set_minutes(1,c2)

def write_am_pm(c_am,c_pm):
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    #For testing
    #hour = 15
    #minute = 16

    # AM or PM
    if(hour>12):
        write("pm",c_pm)
    else:
        write("am",c_am)

def update_clock():
     set_all_letters("black")
     write_time("white","red")
     write_am_pm("#909090","#707070")
     sec = datetime.now().second
     if sec%2:
         set_logo("green")
     else:
         set_logo("blue")
     root.after(1000, update_clock)
 



root.after(1000,update_clock)
root.mainloop()

     



