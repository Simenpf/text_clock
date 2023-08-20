import random
import cv2
import colors
import clock
delay = 200

# Score
score = 0
high_score = 0


class Object:
    def __init__(self) -> None:
        self.direction = "right"
        self.ycor = 5
        self.xcor = 5
    
    def sety(self, y):
        self.ycor = y

    def setx(self, x):
        self.xcor = x

    def goto(self, x, y):
        self.setx(x)
        self.sety(y)
    def getPos(self):
        return (self.xcor, self.ycor)

class SnakeGame:
    def __init__(self) -> None:
        self.head = Object()
        self.food = Object()
        self.food.goto(random.randint(0,10),random.randint(0,9))
        self.segments = []

    # Functions
    def go_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def move(self):
        if self.head.direction == "up":
            y = self.head.ycor
            self.head.sety(y - 1)

        if self.head.direction == "down":
            y = self.head.ycor
            self.head.sety(y + 1)

        if self.head.direction == "left":
            x = self.head.xcor
            self.head.setx(x - 1)

        if self.head.direction == "right":
            x = self.head.xcor
            self.head.setx(x + 1)

snake_button = None
def init_game(clear_pixels, set_pixel, show_pixels):
    global delay
    global score
    global high_score
    global head
    global food
    global segment
    global snake_button
    game = SnakeGame()
    # Main game loop
    clock.write("three",lambda x,y:set_pixel(x,y,colors.get_standard_color("nice_green")))
    show_pixels()
    cv2.waitKey(1000)
    clear_pixels()
    clock.write("two",lambda x,y:set_pixel(x,y,colors.get_standard_color("nice_green")))
    show_pixels()
    cv2.waitKey(1000)
    clear_pixels()
    clock.write("one",lambda x,y:set_pixel(x,y,colors.get_standard_color("nice_green")))
    show_pixels()
    cv2.waitKey(1000)
    clear_pixels()
    while True:
        # Check for a collision with the food
        if game.head.getPos() == game.food.getPos():
            # Move the food to a random spot
            x = random.randint(0, 10)
            y = random.randint(0, 9)
            game.food.goto(x,y)

            # Add a segment
            new_segment = Object()
            game.segments.append(new_segment)

            # Shorten the delay
            delay -= 1

            # Increase the score
            score += 10

            if score > high_score:
                high_score = score

        # Move the end segments first in reverse order
        for index in range(len(game.segments)-1, 0, -1):
            x = game.segments[index-1].xcor
            y = game.segments[index-1].ycor
            game.segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if len(game.segments) > 0:
            x = game.head.xcor
            y = game.head.ycor
            game.segments[0].goto(x,y)

        game.move()    

        # Check for head collision with the body segments
        for segment in game.segments:
            if segment.getPos() == game.head.getPos():
                return
            
        # Check for a collision with the border
        if game.head.xcor>10 or game.head.xcor<-0 or game.head.ycor>9 or game.head.ycor<0:
            return

        clear_pixels()
        set_pixel(game.head.xcor,game.head.ycor, colors.get_standard_color("nice_green"))
        for segment in game.segments:
            set_pixel(segment.xcor,segment.ycor, colors.get_standard_color("nice_green"))
        set_pixel(game.food.xcor,game.food.ycor, colors.get_standard_color("nice_red"))
        show_pixels()
        cv2.waitKey(delay)
        if snake_button == "up":
            game.go_up()
        if snake_button == "down":
            game.go_down()
        if snake_button == "left":
            game.go_left()
        if snake_button == "right":
            game.go_right()
