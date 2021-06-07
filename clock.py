from guizero import App, Drawing, Picture
import time
from datetime import datetime
from collections import namedtuple

Pos = namedtuple("Pos", "x y")

w=1280
h=1024
let=[0,0]
txt_wborder=220
txt_hborder=90
circ_inner = 10
circ_outer = circ_inner+32
letter_w = (w-2*txt_wborder)/11
letter_h = (h-2*txt_hborder)/10
app = App(bg="black")
app.set_full_screen()
drawing = Drawing(app, width=w,height=h)
drawing.bg="black"
picture = Picture(app, image="media/colorgif1.gif")

corner1 = Pos(txt_wborder,txt_hborder-25)
corner2 = Pos(w-txt_wborder,txt_hborder-25)
corner3 = Pos(w-txt_wborder,h-txt_hborder-25)
corner4 = Pos(txt_wborder,h-txt_hborder-25)

def set_logo(c):
     drawing.rectangle(w/2-40,h-90,w/2+40,h, color=c)
def set_circle(i,c):
        if i == 0:
             pass
        elif i == 1:
                drawing.oval(corner1.x-circ_inner,corner1.y-circ_inner,corner1.x-circ_outer,corner1.y-circ_outer,color=c)  
        elif i == 2:
                drawing.oval(corner2.x+circ_inner,corner2.y-circ_inner,corner2.x+circ_outer,corner2.y-circ_outer,color=c)  
        elif i == 3:
                drawing.oval(corner3.x+circ_inner,corner3.y+circ_inner,corner3.x+circ_outer,corner3.y+circ_outer,color=c)  
        elif i == 4:
                drawing.oval(corner4.x-circ_inner,corner4.y+circ_inner,corner4.x-circ_outer,corner4.y+circ_outer,color=c)
def set_minutes(m,c):
        if m == 0:
             pass
        elif m == 1:
             set_circle(1,c)
        elif m == 2:
             set_circle(1,c)
             set_circle(2,c)
        elif m == 3:
             set_circle(1,c)
             set_circle(2,c)
             set_circle(3,c)
        elif m == 4:
             set_circle(1,c)
             set_circle(2,c)
             set_circle(3,c)
             set_circle(4,c)
def set_letter(x,y,c):
	drawing.rectangle(txt_wborder+letter_w*x,txt_hborder-25+letter_h*y,txt_wborder+letter_w*(x+1),txt_hborder-25+letter_h*(y+1),color=c)
def set_letters(letters,c):
        for l in letters:
                set_letter(l[0],l[1],c)
def set_all_letters(c):
        drawing.rectangle(txt_wborder,txt_hborder-25,txt_wborder+letter_w*11,txt_hborder+letter_h*10-25,color=c)
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

def write_time(c):
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
    if surplus_minutes == 1:
        set_minutes(1,c)
    elif surplus_minutes == 2:
        set_minutes(2,c)
    elif surplus_minutes == 3:
        set_minutes(3,c)
    elif surplus_minutes == 4:
        set_minutes(4,c)

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
     drawing.clear()
     write_time("white")
     write_am_pm("#909090","#707070")
     set_logo("yellow")


#drawing.repeat(7,update_clock)
app.display()
