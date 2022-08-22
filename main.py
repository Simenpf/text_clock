import threading
import cv2
import imutils
from screeninfo import get_monitors
import numpy as np
from clock import *
from flask import Flask, request, render_template
from threading import Thread
from PIL import ImageColor






# Initiate globals
logo_color    = (255,255,0)
minutes_color = (0,255,255)
letters_color = (255,0,255)
        
        
# Screen dimensions
screen = get_monitors()[0]
txt_wborder=220                              #Distance from left and right side, to the closest letter
txt_woffset=20                               #The horisontal shift of the text (if monitor is not horizontally centered behind text)
txt_hborder=90                               #Distance from top and bottom, to the closest letter
txt_hoffset=25                               #The vertical shift of the text (if monitor is not vertically sentered behind text)
txt_w = screen.width-2*txt_wborder           #Total width of text-block
txt_h = screen.height-2*txt_hborder          #Total height of text-block
letter_w = (screen.width-2*txt_wborder)//11  #Width of a letter
letter_h = (screen.height-2*txt_hborder)//10 #Height of a letter
minute_w = 60                                #Width of a minute-dot
logo_w = 80                                  #Width of the logo
logo_h = 90                                  #Height of the logo

# Symbol positional definitions
logo_start      = (screen.width//2-logo_w//2,screen.height-logo_h)
logo_end        = (screen.width//2+logo_w//2,screen.height)
logo_positions = [logo_start,logo_end]
minutes_positions = []
minutes_positions.append([(txt_wborder, txt_hborder),(txt_wborder-minute_w, txt_hborder-minute_w)])
minutes_positions.append([(txt_wborder+txt_w, txt_hborder),(txt_wborder+txt_w+minute_w, txt_hborder-minute_w)])
minutes_positions.append([(txt_wborder+txt_w, txt_hborder+txt_h),(txt_wborder+txt_w+minute_w, txt_hborder+txt_h+minute_w)])
minutes_positions.append([(txt_wborder, txt_hborder+txt_h),(txt_wborder-minute_w, txt_hborder+txt_h+minute_w)])
letters_positions = []
for x in range(11):
    letters_positions.append([])
    for y in range(10):
        x0 = txt_wborder+x*letter_w
        y0 = txt_hborder+y*letter_h
        x1 = x0 + letter_w
        y1 = y0 + letter_h
        letters_positions[x].append([(x0,y0),(x1,y1)])




# Initiate canvas and mask
blank_image = np.zeros((screen.height,screen.width,3), np.uint8)
canvas      = blank_image.copy()
canvas_mask = blank_image.copy()
canvas[:,:] = (255,255,255)


def set_logo(c):
    global canvas_mask
    canvas_mask = cv2.rectangle(canvas_mask, logo_positions[0], logo_positions[1], c, -1)
def set_minute(m,c):
    global canvas_mask
    canvas_mask = cv2.rectangle(canvas_mask, minutes_positions[m-1][0], minutes_positions[m-1][1], c, -1)
def set_letter(x,y,c):
    global canvas_mask
    canvas_mask = cv2.rectangle(canvas_mask, letters_positions[x][y][0], letters_positions[x][y][1], c, -1)
def shift_for_offset(image, x_offset, y_offset):
    translation_matrix = np.float32([[1, 0, -x_offset], [0, 1, -y_offset]])
    return cv2.warpAffine(image, translation_matrix, (screen.width, screen.height))
def update_canvas():
    global canvas
    canvas = cv2.rectangle(canvas, logo_positions[0], logo_positions[1], logo_color, -1)
    canvas = cv2.rectangle(canvas, letters_positions[0][0][0], letters_positions[-1][-1][1], letters_color, -1)
    for pos in minutes_positions:
        canvas = cv2.rectangle(canvas, pos[0], pos[1], minutes_color, -1)





def task():
    global canvas
    global canvas_mask
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    while(True):
        update_canvas()
        canvas_mask = blank_image.copy()
        write_time((255,255,255),(255,255,255),set_letter, set_minute)
        set_logo((255,255,255))
        masked_canvas = cv2.bitwise_and(canvas, canvas_mask)
        masked_canvas = shift_for_offset(masked_canvas, txt_woffset, txt_hoffset)
        cv2.imshow("window",masked_canvas)
        key = cv2.waitKey(200)
        if key & 0xFF == 27:
          break
thread = threading.Thread(target=task)
thread.start()

# Flask constructor
app = Flask(__name__)  
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    global letters_color
    if request.method == "POST":
        color = str(request.form.get("color"))
        color = ImageColor.getcolor(color,"RGB")
        letters_color = (color[2],color[1],color[0])
        return render_template("form.html")
    return render_template("form.html")
 
if __name__=='__main__':
   app.run(host='0.0.0.0', port=80)

# # Setup rpyc server
# class ClockService(rpyc.Service):
#     global logo_color
#     global letters_color
#     global minutes_color
#     def exposed_change_logo_color(self, color):
#         global logo_color
#         logo_color = color
#     def exposed_change_letters_color(self, color):
#         global letters_color
#         letters_color = color
#     def exposed_change_minutes_color(self, color):
#         global minutes_color
#         minutes_color = color
# if __name__ == "__main__":
#     server = ThreadedServer(ClockService, port = 18812)
#     server.start()
