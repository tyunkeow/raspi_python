from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import Master
from tinkerforge.bricklet_motion_detector import MotionDetector
from tinkerforge.bricklet_rotary_poti import RotaryPoti
from insulter import speak_next_insult
from time import sleep


def motion_callback():
    print "CALLBACK!!"
    speak_next_insult()

def motion_callback2():
    print "READY"

class PiTinkerforgeStack:
    host = '192.168.178.27' #raspi
    #host = '127.0.0.1' #localhost
    port = 4223
    uid_master = '6JKxCC'
    uid_motion = 'oRL'
    uid_poti_left = 'ejC'
    uid_poti_right = 'ejm'

    def __init__(self):
        self.con = IPConnection()
        self.master = Master(self.uid_master, self.con)
        self.motion = MotionDetector(self.uid_motion, self.con)
        self.poti_left = RotaryPoti(self.uid_poti_left, self.con)
        self.poti_right = RotaryPoti(self.uid_poti_right, self.con)


    def connect(self):
        print "Connecting to host " + self.host + " on port " + str(self.port)
        self.con.connect(self.host, self.port)

    def disconnect(self):
        print "Disconnecting from host " + self.host
        self.con.disconnect()

    def register_motion_callback(self, callback, cb2):
        print "Registering callback to motion detector..."
        self.motion.register_callback(self.motion.CALLBACK_MOTION_DETECTED, callback)
        self.motion.register_callback(self.motion.CALLBACK_DETECTION_CYCLE_ENDED, cb2)


if __name__ == "__main__":
    stack = PiTinkerforgeStack()
    stack.connect()
    #print "Distance Ultrasonic 1       : ", stack.distance_us_1.get_distance_value()
    #print "Distance Infrared 1         : {} cm".format(stack.distance_ir_1.get_distance()/10)
    #print "MultiTouch electrode config : ", stack.multi_touch_1.get_electrode_config()
    #print "Servo 6 position            : ", stack.servo.get_position(6)
    print "Poti left position  : ", stack.poti_left.get_position()
    print "Poti right position : ", stack.poti_right.get_position()
    stack.register_motion_callback(motion_callback, motion_callback2)

    sleep(100)
    stack.disconnect()

