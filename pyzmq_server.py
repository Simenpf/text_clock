import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
socket.RCVTIMEO = 1000
while True:
    #  Wait for next request from client
    try:
        message = socket.recv_string()
        print(message)
    except:
        print("No message")
    finally:
    #  Do some 'work'

    #  Send reply back to client
    #socket.send(b"World")
