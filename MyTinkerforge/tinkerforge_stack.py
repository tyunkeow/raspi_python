from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_multi_touch import MultiTouch
from tinkerforge.bricklet_distance_us import DistanceUS
from tinkerforge.bricklet_distance_ir import DistanceIR
from tinkerforge.brick_servo import Servo
from tinkerforge.brick_master import Master


class PiTinkerforgeStack:
    host = '192.168.178.20' #raspi
    port = 4223
    uid_master = '6JKxCC'
    uid_multi_touch_1 = 'jS3'
    uid_ultrasonic_1 = 'jAW'
    uid_infrared_1 = 'hJd'
    uid_servo = '6kpTt1'

    def __init__(self):
        self.con = IPConnection()
        self.master = Master(self.uid_master, self.con)
        self.multi_touch_1 = MultiTouch(self.uid_multi_touch_1, self.con)
        self.distance_us_1 = DistanceUS(self.uid_ultrasonic_1, self.con)
        self.distance_ir_1 = DistanceIR(self.uid_infrared_1, self.con)
        self.servo = Servo(self.uid_servo, self.con)

    def connect(self):
        print "Connecting to host " + self.host + " on port " + str(self.port)
        self.con.connect(self.host, self.port)

    def disconnect(self):
        print "Disconnecting from host " + self.host
        self.con.disconnect()

if __name__ == "__main__":
    stack = PiTinkerforgeStack()
    stack.connect()
    print "Distance Ultrasonic 1       : ", stack.distance_us_1.get_distance_value()
    print "Distance Infrared 1         : {} cm".format(stack.distance_ir_1.get_distance()/10)
    print "MultiTouch electrode config : ", stack.multi_touch_1.get_electrode_config()
    print "Servo 6 position            : ", stack.servo.get_position(6)
    stack.disconnect()

