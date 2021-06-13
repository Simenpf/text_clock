# -*- coding: utf-8 -*-
import zmq
import time

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")



socket.send(b"img")


