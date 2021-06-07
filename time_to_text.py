from datetime import datetime

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
write_time()