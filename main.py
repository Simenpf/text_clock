import os
import cv2
import json
import threading
import numpy as np
from screeninfo import get_monitors
from flask import Flask, request, render_template

import clock
import colors
import screen
import snake_game

# Definitions
white = colors.get_standard_color("white")
showClock = True
showSnake = False

def load_config():
    global config_file_path
    global config
    current_directory_path = os.path.dirname(__file__)
    config_file_path = os.path.join(current_directory_path, 'config.json')
    config_file = open(config_file_path)
    config = json.load(config_file)


def save_config():
    config_file = open(config_file_path, "w")
    json.dump(config,config_file)

def update_screen_adjustments(screen_adjustment, screen_resolution):
    global minute_positions
    global letter_positions
    global logo_positions
    minute_positions = screen.get_minute_positions(screen_adjustment, screen_resolution)
    letter_positions = screen.get_letter_positions(screen_adjustment, screen_resolution)
    logo_positions   = screen.get_logo_positions(screen_adjustment, screen_resolution)
    save_config()

def init_screen_adjustments(screen_adjustment):
    global screen_resolution
    screen_resolution = get_monitors()[0]
    update_screen_adjustments(screen_adjustment, screen_resolution)

def update_colors(color_settings):
    global logo_color
    global letters_color
    global minutes_color
    logo_color = colors.Color(color_settings["logo_color"]).bgr
    letters_color = colors.Color(color_settings["letters_color"]).bgr
    minutes_color = colors.Color(color_settings["minutes_color"]).bgr
    save_config()

def set_logo():
    global canvas_mask
    canvas_mask = cv2.rectangle(canvas_mask, logo_positions[0], logo_positions[1], white.bgr, -1)

def set_minute(m,):
    global canvas_mask
    canvas_mask = cv2.rectangle(canvas_mask, minute_positions[m-1][0], minute_positions[m-1][1], white.bgr, -1)

def set_letter(x,y):
    global canvas_mask
    canvas_mask = cv2.rectangle(canvas_mask, letter_positions[x][y][0], letter_positions[x][y][1], white.bgr, -1)

def shift_for_offset(image, x_offset, y_offset):
    translation_matrix = np.float32([[1, 0, -x_offset], [0, 1, -y_offset]])
    return cv2.warpAffine(image, translation_matrix, (screen_resolution.width, screen_resolution.height))

def update_canvas():
    global canvas
    canvas = cv2.rectangle(canvas, logo_positions[0], logo_positions[1], logo_color, -1)
    canvas = cv2.rectangle(canvas, letter_positions[0][0][0], letter_positions[-1][-1][1], letters_color, -1)
    for pos in minute_positions:
        canvas = cv2.rectangle(canvas, pos[0], pos[1], minutes_color, -1)


def clear_pixels():
    global canvas
    for x in range(11):
        for y in range(10):
            canvas = cv2.rectangle(canvas, letter_positions[x][y][0], letter_positions[x][y][1], colors.get_standard_color("black").bgr, -1)


def set_pixel(x,y,color):
    global canvas
    canvas = cv2.rectangle(canvas, letter_positions[x][y][0], letter_positions[x][y][1], color.bgr, -1)

def show_pixels():
    global canvas
    cv2.imshow("window",canvas)


def display_time():
    global canvas
    global canvas_mask
    global showClock
    global showSnake
    blank_image = np.zeros((screen_resolution.height,screen_resolution.width,3), np.uint8)
    canvas      = blank_image.copy()
    canvas_mask = blank_image.copy()

    # Initialize window
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)  

    # Run display loop
    while(True):
        while(showClock):
            update_canvas()
            canvas_mask = blank_image.copy()
            clock.write_time(set_letter, set_minute)
            set_logo()
            masked_canvas = cv2.bitwise_and(canvas, canvas_mask)
            masked_canvas = shift_for_offset(masked_canvas, config["screen_adjustment"]["text_horizontal_offset"], config["screen_adjustment"]["text_vertical_offset"])
            cv2.imshow("window",masked_canvas)
            key = cv2.waitKey(200)
            if key & 0xFF == 27:
              break
        if showSnake:
            canvas = blank_image.copy()
            snake_game.init_game(clear_pixels,set_pixel,show_pixels)
            showClock = True
            showSnake = False



###############
# Define webapp
###############
app = Flask(__name__)  
 
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/color_settings')
def color_settings():
    return render_template("color_settings.html", config=config)

@app.route('/adjust_color', methods=['POST'])
def adjust_color():
    global config
    config["color_settings"]["logo_color"] =    str(request.form['logo_color'])
    config["color_settings"]["letters_color"] = str(request.form['letters_color'])
    config["color_settings"]["minutes_color"] = str(request.form['minutes_color'])
    update_colors(config["color_settings"])
    return ''


@app.route('/screen_adjustment')
def screen_adjustment():
    return render_template('screen_adjustment.html', config=config)

@app.route('/adjust_screen', methods=['POST'])
def adjust_screen():
    global config
    config["screen_adjustment"]["logo_width"]             = int(request.form['logo_width'])
    config["screen_adjustment"]["logo_height"]            = int(request.form['logo_height'])
    config["screen_adjustment"]["text_vertical_border"]   = int(request.form['text_vertical_border'])
    config["screen_adjustment"]["text_horizontal_border"] = int(request.form['text_horizontal_border'])
    config["screen_adjustment"]["text_vertical_offset"]   = int(request.form['text_vertical_offset'])
    config["screen_adjustment"]["text_horizontal_offset"] = int(request.form['text_horizontal_offset'])
    config["screen_adjustment"]["minute_diameter"]        = int(request.form['minute_diameter'])
    update_screen_adjustments(config["screen_adjustment"], screen_resolution)
    return ''

@app.route('/fun')
def fun():
    return render_template('fun.html')

@app.route('/snake')
def snake():
    global showClock 
    global showSnake
    showClock = False
    showSnake = True
    return render_template('snake.html')

@app.route('/snake_update', methods=['POST'])
def snake_update():
    global snake_button
    snake_game.snake_button = str(request.form['button'])
    return ''



def fun():
    return render_template('fun.html')

if __name__=='__main__':
    load_config()
    init_screen_adjustments(config["screen_adjustment"])
    update_colors(config["color_settings"])
    clock_thread = threading.Thread(target=display_time)
    clock_thread.start()
    app.run(host='0.0.0.0', port=80)

