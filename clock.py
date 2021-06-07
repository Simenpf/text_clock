from guizero import App, Drawing
from datetime import datetime
import time

w=1280
h=1024
let=[0,0]
txt_wborder=220
txt_hborder=90
letter_w = (w-2*txt_wborder)/11
letter_h = (h-2*txt_hborder)/10
app = App(bg="black")
app.set_full_screen()
drawing = Drawing(app, width=w,height=h)
drawing.bg="black"

drawing.rectangle(txt_wborder,txt_hborder,w-txt_wborder,h-txt_hborder, color="black")
def set_logo(c):
     drawing.rectangle(w/2-40,h-70,w/2+40,h, color=c)
def set_minute(m,c):
        if m == 0:
                pass
        elif m == 1:
                pass
        elif m == 2:
                pass
        elif m == 3:
                pass
        elif m == 4:
                pass
def set_letter(x,y,c):
	drawing.rectangle(txt_wborder+letter_w*x,txt_hborder-25+letter_h*y,txt_wborder+letter_w*(x+1),txt_hborder-25+letter_h*(y+1),color=c)
def set_letters(letters,c):
        for l in letters:
                set_letter(l[0],l[1],c)
def set_all_letters(c):
        drawing.rectangle(txt_wborder+letter_w,txt_hborder+letter_h,txt_wborder+letter_w*10,txt_hborder+letter_h*9,color=c)
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

def write_time():
    now = datetime.now()
    hour = now.hour()
    minute = now.minute()
    if(hour>12):
        print("pm")
    else:
        print("am")
    print("it is")

    if(minute < 35):
        print("past")
    else:
        print("to")

write_sentence(["it","is","twenty","five1","past","three"],"white")
write("am","yellow")
set_logo("green")
app.display()
