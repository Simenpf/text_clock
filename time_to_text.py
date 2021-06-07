from datetime import datetime

def write_time():
    print(datetime.now())
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    #For testing
    hour = 15
    minute = 16

    # AM or PM
    if(hour>12):
        print("pm")
    else:
        print("am")

    # It is
    print("it is")

    # five, ten, quarter, twenty, twentyfive, half
    minute_block = minute // 5
    if minute_block == 0:
        pass
    elif minute_block == 1 or minute_block == 11:
        print("five")
    elif minute_block == 2 or minute_block == 10:
        print("ten")
    elif minute_block == 3 or minute_block == 9:
        print("quarter")
    elif minute_block == 4 or minute_block == 8:
        print("twenty")
    elif minute_block == 5 or minute_block == 7:
        print("twentyfive")
    elif minute_block == 6:
        print("half")

    # Past, to or whole hour
    if(minute < 35):
        print("past")
    elif(minute >= 5):
        print("to")
        hour += 1

    # one, two, three, ...
    if (hour == 1) or (hour == 13):
        print("one")
    elif (hour == 2) or (hour == 14):
        print("two")
    elif (hour == 3) or (hour == 15):
        print("three")
    elif (hour == 4) or (hour == 16):
        print("four")
    elif (hour == 5) or (hour == 17):
        print("five")
    elif (hour == 6) or (hour == 18):
        print("six")
    elif (hour == 7) or (hour == 19):
        print("seven")
    elif (hour == 8) or (hour == 20):
        print("eight")
    elif (hour == 9) or (hour == 21):
        print("nine")
    elif (hour == 10) or (hour == 22):
        print("ten")
    elif (hour == 11) or (hour == 23):
        print("eleven")
    elif (hour == 12) or (hour == 24):
        print("twelwe")

    # Extra minutes
    surplus_minutes = minute % 5
    if surplus_minutes == 1:
        print("plus one minute")
    elif surplus_minutes == 2:
        print("plus two minutes")
    elif surplus_minutes == 3:
        print("plus three minutes")
    elif surplus_minutes == 4:
        print("plus four minutes")

write_time()