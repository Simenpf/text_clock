import rpyc
import sys
r = int(sys.argv[1])
g = int(sys.argv[2])
b = int(sys.argv[3])

c = rpyc.connect("localhost",18812)
c.root.change_letters_color((b,g,r))
