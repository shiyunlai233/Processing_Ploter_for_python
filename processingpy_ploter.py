# use this code in the python Mode processing.

add_library('net')

import json, pickle

class RPCHandler:
    def __init__(self):
        self._functions = { }

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_mesg(self, mesg):
        mesg = pickle.loads(mesg)
        # print(mesg)
        mg = mesg
        
        for m in mg:
            m = json.loads(m)
            # print(m, len(m))
            func_name, args, kwargs = m
            try:
                r = self._functions[func_name](*args,**kwargs)
            except Exception as e:
                pass

handler = RPCHandler()
fs = [arc, circle, ellipse, line, point, quad, rect, square, triangle, \
      fill, stroke, background]
for f in fs:
    handler.register_function(f)

s = Server(this, 12345)

def setup():
    size(600 ,600)
    rectMode(CENTER)

def draw():
    c = s.available()
    if c != None:
        mesg = c.readString()
        # print(frameCount, mesg)
        handler.handle_mesg(mesg)
