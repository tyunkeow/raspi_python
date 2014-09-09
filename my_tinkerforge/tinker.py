#HOST = '192.168.178.22'
HOST = '127.0.10.1'
PORT = 4223
UID_MT = 'jS3'
UID_US = 'jAW'

from time import sleep
from tinkerforge_stack import PiTinkerforgeStack

def register_distance_us(stack, callback, threshold):
    us = stack.distance_us_1

    us.set_debounce_period(1000)
    us.set_distance_callback_period(500)
    us.register_callback(us.CALLBACK_DISTANCE_REACHED, callback)
    print "Callback for distance < {}".format(threshold)
    us.set_moving_average(20)
    print "Moving averag is {}".format(us.get_moving_average())
    us.set_distance_callback_threshold('<', threshold, 0)

def register_distance_ir(stack, callback, threshold):
    ir = stack.distance_ir_1

    ir.set_debounce_period(500)
    ir.set_distance_callback_period(0)
    ir.register_callback(ir.CALLBACK_DISTANCE_REACHED, callback)
    print "Callback for distance < {}".format(threshold)
    #ir.set_moving_average(20)
    #print "Moving averag is {}".format(us.get_moving_average())
    ir.set_distance_callback_threshold('<', threshold, 0)


def register_multi_touch(stack, callback):
    #if callback == None:
    #    raise Exception
    mt = stack.multi_touch_1
    mt.register_callback(mt.CALLBACK_TOUCH_STATE, callback)


def callback_touch_state(touch_state):
    s = ''
    if touch_state & (1 << 12):
        s += "In prox, "

    if (touch_state & 0xFFF) == 0:
        s += "none"
    else:
        s += "electrodes "
        for i in range(12):
            if touch_state & (1 << i):
                s += str(i) + ' '
    print s


def callback_distance_ir(distance):
    print "Distance is {} cm".format(distance/10)

if __name__ == "__main__":
    stack = PiTinkerforgeStack()
    stack.connect()

    #register_multi_touch(stack, callback_touch_state)
    register_distance_ir(stack, callback_distance_ir, 220)
    sleep(30) 
