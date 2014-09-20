from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import Master
from tinkerforge.bricklet_motion_detector import MotionDetector
from tinkerforge.bricklet_rotary_poti import RotaryPoti
from tinkerforge.bricklet_io4 import IO4
from insulter import speak_next_insult
from time import sleep



class PiTinkerforgeStack:
    host = '192.168.178.27' #raspi
    #host = '127.0.0.1' #localhost
    port = 4223
    uid_master = '6JKxCC'
    uid_motion = 'oRL'
    uid_poti_left = 'ejC'
    uid_poti_right = 'ejm'
    uid_io = 'hcs'
    female = False

    def __init__(self):
        self.con = IPConnection()
        self.master = Master(self.uid_master, self.con)
        self.motion = MotionDetector(self.uid_motion, self.con)
        self.poti_left = RotaryPoti(self.uid_poti_left, self.con)
        self.poti_right = RotaryPoti(self.uid_poti_right, self.con)
        self.io = IO4(self.uid_io, self.con)
        print "---" + str(15^15)
        print "---" + str(15^14)


    def connect(self):
        print "Connecting to host " + self.host + " on port " + str(self.port)
        self.con.connect(self.host, self.port)

    def disconnect(self):
        print "Disconnecting from host " + self.host
        self.con.disconnect()

    def motion_detected(self):
        print "CALLBACK!!"
        speak_next_insult(self.poti_left.get_position())

    def motion_cycle_ended(self):
        print "READY"

    def io_switch(self, interrupt_mask, value_mask):
        print "SWITCH"
        #print('Interrupt by: ' + str(bin(interrupt_mask)))
        #print('Value: ' + str(bin(value_mask)))
        #print('Val1: ' + str(value_mask))

        if interrupt_mask == 1:
            # button 1 switched
            is_on = value_mask^14
            if is_on:
                print "FEMALE"
                self.female = True
            else:
                print "MALE"
                self.female = False

    def register_callbacks(self):
        print "Registering callback to motion detector..."
        self.motion.register_callback(self.motion.CALLBACK_MOTION_DETECTED, self.motion_detected)
        self.motion.register_callback(self.motion.CALLBACK_DETECTION_CYCLE_ENDED, self.motion_cycle_ended)
        self.io.register_callback(self.io.CALLBACK_INTERRUPT, self.io_switch)
        # Enable interrupt on pin 0
        self.io.set_interrupt(1 << 0)
        print "register done"


if __name__ == "__main__":
    stack = PiTinkerforgeStack()
    stack.connect()
    #print "Distance Infrared 1         : {} cm".format(stack.distance_ir_1.get_distance()/10)
    #print "MultiTouch electrode config : ", stack.multi_touch_1.get_electrode_config()
    print "Poti left position  : ", stack.poti_left.get_position()
    print "Poti right position : ", stack.poti_right.get_position()
    stack.register_callbacks()

    sleep(100)
    stack.disconnect()

