# -*- coding: utf-8 -*-
import zmq
import time
import tkinter as tk

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:5555")


def key(event):
    """shows key or tk code for the key"""
    if event.keysym == 'Escape':
        root.destroy()
    if event.keysym == 'Right':
            socket.send(b"right")
    if event.keysym == 'Left':
            socket.send(b"left")


root = tk.Tk()
print( "Use the arrow keys (Escape key to exit):" )
root.bind_all('<Key>', key)

left_pressed = False
right_pressed = False

root.withdraw()
root.mainloop()