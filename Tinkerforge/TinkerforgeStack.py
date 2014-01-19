from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_multi_touch import MultiTouch
from tinkerforge.bricklet_distance_us import DistanceUS


class TinkerforgeStack:
    def __init__(self):
        self.host = 'localhost'
        self.port = 4223
        self.uid_master = ''
        self.uid_multi_touch_1 = 'jS3'
        self.uid_ultrasonic_1 = 'jAW'
        self.con = IPConnection()
        self.multi_touch_1 = MultiTouch(self.uid_multi_touch_1, self.con)
        self.distance_us_1 = DistanceUS(self.uid_ultrasonic_1, self.con)
        #self.master = Master(uidMaster, con)

    def connect(self):
        self.con.connect(self.host, self.port)

    def disconnect(self):
        self.con.disconnect()

    def get_multi_touch_1(self):
        return self.multi_touch_1

    def get_distance_us_1(self):
        return self.distance_us_1

    def get_master(self):
        return 0
        #return master
