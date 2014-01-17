
HOST='localhost'
PORT=4223
UID_MT='jS3'
UID_US='jAW'

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_multi_touch import MultiTouch
from tinkerforge.bricklet_distance_us import DistanceUS
from time import sleep

con = IPConnection()
mt = MultiTouch(UID_MT, con)
us = DistanceUS(UID_US, con)
con.connect(HOST, PORT)

def register_distance_us(callback, threshold):
    us.set_debounce_period(1000)
    us.set_distance_callback_period(500)
    us.register_callback(us.CALLBACK_DISTANCE_REACHED, callback)
    print "Callback for distance < {}".format(threshold)
    us.set_moving_average(20)
    print "Moving averag is {}".format(us.get_moving_average())
    us.set_distance_callback_threshold('<', threshold, 0)

def register_multi_touch(callback):
    #if callback == None:
    #    raise Exception
    mt.register_callback(mt.CALLBACK_TOUCH_STATE, callback)

def callback_touch_state(touch_state):
    s = ''
    if touch_state & (1<<12):
        s += "In prox, "

    if (touch_state & 0xFFF) == 0:
        s += "none"
    else:
        s += "electrodes "
        for i in range(12):
            if touch_state & (1<<i):
                s += str(i) + ' '
    print s

if __name__ == "__main__":
    register_multi_touch(callback_touch_state)  
    sleep(30) 
