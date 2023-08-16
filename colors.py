#####################
# Color Helper Funcs
#####################
def hexToRgb(hex_color):
    # Remove the '#' symbol if present
    hex_color = hex_color.lstrip('#')
    
    # Convert the hex values to integers
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return r, g, b

def rgbToHex(rgb_color):
    # Ensure that the RGB values are within the valid range (0-255)
    r = max(0, min(255, rgb_color[0]))
    g = max(0, min(255, rgb_color[1]))
    b = max(0, min(255, rgb_color[2]))
    
    # Convert the RGB values to hex and format them
    hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
    
    return hex_color

def rgbToBgr(rgb_color):
    # Ensure that the RGB values are within the valid range (0-255)
    r = max(0, min(255, rgb_color[0]))
    g = max(0, min(255, rgb_color[1]))
    b = max(0, min(255, rgb_color[2]))
    
    # Convert RGB to BGR format
    bgr_color = (b, g, r)
    
    return bgr_color

def bgrToRgb(bgr_color):
    # Ensure that the BGR values are within the valid range (0-255)
    b = max(0, min(255, bgr_color[0]))
    g = max(0, min(255, bgr_color[1]))
    r = max(0, min(255, bgr_color[2]))
    
    # Convert BGR to RGB format
    rgb_color = (r, g, b)
    
    return rgb_color

##############
# Color Class
##############
class Color:
    def __init__(self, color, name = None):
        if isinstance(color,str):
            self.hex = color
            self.rgb = hexToRgb(color)
            self.bgr = rgbToBgr(self.rgb)
        if isinstance(color,tuple):
            self.rgb = color
            self.hex = rgbToHex(color)
            self.bgr = rgbToBgr(self.rgb)
        self.name = name

####################
# Color definitions
####################
standard_colors = {
    "nice_cyan":"#4DDBFF",
    "nice_red":"#FF4D4D",
    "nice_blue":"#4DBBFF",
    "nice_green":"#5AFF57",
    "red":"#FF0000",
    "green":"#00FF00",
    "blue":"#0000FF",
    "black":"#000000",
    "white":"#FFFFFF"}

def get_standard_color(color_name):
    return Color(standard_colors[color_name],color_name)

if __name__ == "__main__":
    red = Color((255,0,0),"red")
    blue = Color("#0000FF","blue")
    green = get_standard_color("green")
    print(red.hex)
    print(red.rgb)
    print(red.name)
    print(green.hex)
    print(green.rgb)
    print(green.name)
    print(blue.hex)
    print(blue.rgb)
    print(blue.name)

