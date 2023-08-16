import threading
import cv2
from screeninfo import get_monitors
import numpy as np
from clock import *
from flask import Flask, request, render_template
from PIL import ImageColor
import colors
import json

# Load config
f = open('text_clock/config.json')
config = json.load(f)

# Initiate globals
light_cyan = colors.get_standard_color("nice_cyan")
logo_color    = light_cyan.bgr
minutes_color = light_cyan.bgr
letters_color = light_cyan.bgr
background_color = light_cyan.bgr
        
# Screen dimensions
screen      = get_monitors()[0]
txt_vborder = config["screen_adjustment"]["text_vertical_border"]    # Distance from left and right side, to the closest letter
txt_voffset = config["screen_adjustment"]["text_vertical_offset"]    # The horisontal shift of the text (if monitor is not horizontally centered behind text)
txt_hborder = config["screen_adjustment"]["text_horizontal_border"]  # Distance from top and bottom, to the closest letter
txt_hoffset = config["screen_adjustment"]["text_horizontal_offset"]  # The vertical shift of the text (if monitor is not vertically sentered behind text)
minute_d    = config["screen_adjustment"]["minute_diameter"]         # Diameter of a minute-dot
logo_w      = config["screen_adjustment"]["logo_width"]              # Width of the logo
logo_h      = config["screen_adjustment"]["logo_width"]              # Height of the logo

def setup_screen():
    global canvas
    global canvas_mask
    global logo_positions
    global logo_positions
    global minutes_positions
    global letters_positions
    global blank_image
    global screen_updated

    txt_w    = screen.width-2*txt_vborder        # Total width of text-block
    txt_h    = screen.height-2*txt_hborder       # Total height of text-block
    letter_w = (screen.width-2*txt_vborder)//11  # Width of a letter
    letter_h = (screen.height-2*txt_hborder)//10 # Height of a letter

    # Symbol positional definitions
    logo_start      = (screen.width//2-logo_w//2,screen.height-logo_h)
    logo_end        = (screen.width//2+logo_w//2,screen.height)
    logo_positions = [logo_start,logo_end]
    minutes_positions = []
    minutes_positions.append([(txt_vborder, txt_hborder),(txt_vborder-minute_d, txt_hborder-minute_d)])
    minutes_positions.append([(txt_vborder+txt_w, txt_hborder),(txt_vborder+txt_w+minute_d, txt_hborder-minute_d)])
    minutes_positions.append([(txt_vborder+txt_w, txt_hborder+txt_h),(txt_vborder+txt_w+minute_d, txt_hborder+txt_h+minute_d)])
    minutes_positions.append([(txt_vborder, txt_hborder+txt_h),(txt_vborder-minute_d, txt_hborder+txt_h+minute_d)])
    letters_positions = []
    for x in range(11):
        letters_positions.append([])
        for y in range(10):
            x0 = txt_vborder+x*letter_w
            y0 = txt_hborder+y*letter_h
            x1 = x0 + letter_w
            y1 = y0 + letter_h
            letters_positions[x].append([(x0,y0),(x1,y1)])

    # Initiate canvas and mask
    blank_image = np.zeros((screen.height,screen.width,3), np.uint8)
    canvas      = blank_image.copy()
    canvas_mask = blank_image.copy()
    canvas[:,:] = background_color
    
    screen_updated = True


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
    global blank_image
    global screen_updated

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    while(True):
        setup_screen()
        while screen_updated == True:
            update_canvas()
            canvas_mask = blank_image.copy()
            write_time((255,255,255),(255,255,255),set_letter, set_minute)
            set_logo((255,255,255))
            masked_canvas = cv2.bitwise_and(canvas, canvas_mask)
            masked_canvas = shift_for_offset(masked_canvas, txt_voffset, txt_hoffset)
            cv2.imshow("window",masked_canvas)
            key = cv2.waitKey(200)
            if key & 0xFF == 27:
              break

# Flask constructor
app = Flask(__name__)  
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/color_settings')
def color_settings():
    return render_template("color_settings.html")

@app.route('/adjust_color', methods=['POST'])
def adjust_color():
    global logo_color
    global letters_color
    global minutes_color
    logo_color = colors.Color(str(request.form['logoColor'])).bgr  # Retrieve color value from request
    letters_color = colors.Color(str(request.form['lettersColor'])).bgr  # Retrieve color value from request
    minutes_color = colors.Color(str(request.form['minutesColor'])).bgr  # Retrieve color value from request

    # Process the color value and perform necessary actions in your Python script
    return ''  # Return a response to the client


@app.route('/screen_adjustment')
def screen_adjustment():
    return render_template('screen_adjustment.html', config=config)

@app.route('/adjust_screen', methods=['POST'])
def adjust_screen():
    global logo_w
    global logo_h
    global txt_vborder
    global txt_voffset
    global txt_hborder
    global txt_hoffset
    global minute_d
    global screen_updated
    logo_w =      int(request.form['logo_width'])
    logo_h =      int(request.form['logo_height'])
    txt_vborder = int(request.form['txt_vborder'])
    txt_voffset = int(request.form['txt_voffset'])
    txt_hborder = int(request.form['txt_hborder'])
    print(txt_hborder)
    txt_hoffset = int(request.form['txt_hoffset'])
    minute_d =    int(request.form['min_d'])
    screen_updated = False
    return ''

@app.route('/fun')
def fun():
    return render_template('fun.html')

if __name__=='__main__':
    setup_screen()
    clock_thread = threading.Thread(target=task)
    clock_thread.start()
    app.run(host='0.0.0.0', port=80)

