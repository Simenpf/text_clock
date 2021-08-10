from datetime import datetime

def set_minutes(m,c,set_minute):
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

def write_time(c,c2,set_letter, set_minute):
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
        write("twelve",c,set_letter)

    # Extra minutes
    surplus_minutes = minute % 5
    if surplus_minutes == 1:
            set_minutes(1,c2, set_minute)
    elif surplus_minutes == 2:
            set_minutes(2,c2, set_minute)
    elif surplus_minutes == 3:
            set_minutes(3,c2, set_minute)
    elif surplus_minutes == 4:
            set_minutes(4,c2, set_minute)


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
def clear_clock(clear_color, set_letter, set_minute):
     set_all_letters(clear_color,set_letter)
     set_minutes(4,clear_color, set_minute)