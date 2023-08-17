def get_text_width(screen_adjustment, screen_resolution):
    return screen_resolution.width-2*screen_adjustment["text_horizontal_border"]

def get_text_height(screen_adjustment, screen_resolution):
    return screen_resolution.height-2*screen_adjustment["text_vertical_border"]

def get_letter_width(screen_adjustment, screen_resolution):
    return (screen_resolution.width-2*screen_adjustment["text_horizontal_border"])//11

def get_letter_height(screen_adjustment, screen_resolution):
    return (screen_resolution.height-2*screen_adjustment["text_vertical_border"])//10

def get_minute_positions(screen_adjustment, screen_resolution):
    txt_vborder = screen_adjustment["text_vertical_border"]
    txt_hborder = screen_adjustment["text_horizontal_border"]
    minute_d =    screen_adjustment["minute_diameter"]
    txt_width = get_text_width(screen_adjustment, screen_resolution)
    txt_height = get_text_height(screen_adjustment, screen_resolution)

    minutes_positions = []
    minutes_positions.append([(txt_hborder,             txt_vborder),              (txt_hborder - minute_d,             txt_vborder - minute_d)])
    minutes_positions.append([(txt_hborder + txt_width, txt_vborder),              (txt_hborder + txt_width + minute_d, txt_vborder - minute_d)])
    minutes_positions.append([(txt_hborder + txt_width, txt_vborder + txt_height), (txt_hborder + txt_width + minute_d, txt_vborder + txt_height + minute_d)])
    minutes_positions.append([(txt_hborder,             txt_vborder + txt_height), (txt_hborder - minute_d,             txt_vborder + txt_height + minute_d)])

    return minutes_positions

def get_letter_positions(screen_adjustment, screen_resolution):
    txt_vborder = screen_adjustment["text_vertical_border"]
    txt_hborder = screen_adjustment["text_horizontal_border"]
    letter_width = get_letter_width(screen_adjustment, screen_resolution)
    letter_height = get_letter_height(screen_adjustment, screen_resolution)
    letter_positions = []
    for x in range(11):
        letter_positions.append([])
        for y in range(10):
            x0 = txt_hborder+x*letter_width
            y0 = txt_vborder+y*letter_height
            x1 = x0 + letter_width
            y1 = y0 + letter_height
            letter_positions[x].append([(x0,y0),(x1,y1)])
    return letter_positions

def get_logo_positions(screen_adjustment, screen_resolution):
    logo_start      = (screen_resolution.width//2-screen_adjustment["logo_width"]//2,screen_resolution.height-screen_adjustment["logo_height"])
    logo_end        = (screen_resolution.width//2+screen_adjustment["logo_width"]//2,screen_resolution.height)
    return [logo_start,logo_end]


    # Initiate canvas and mask
    blank_image = np.zeros((screen.height,screen.width,3), np.uint8)
    canvas      = blank_image.copy()
    canvas_mask = blank_image.copy()
    canvas[:,:] = background_color
    
    screen_updated = True