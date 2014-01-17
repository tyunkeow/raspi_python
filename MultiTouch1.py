#
# MultiTouch1
#
from MyTinkerforge import register_multi_touch 
from time import sleep

def touch(touch_state):
    for i in range(12):
        if touch_state & (1<<i):
            print str(i) + ' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'


register_multi_touch(touch)

sleep(30)
