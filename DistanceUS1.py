#!/usr/bin/python
# DistanceUS1
#
from MyTinkerforge import register_distance_us 
from time import sleep
from Insulter import get_insult 
from Text2Wav import speak

def threshold(dist):
    print str((dist-2927)*1.4) + ' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    #insult = get_insult(-1, -1, -1)
    #speak(insult, 30, 1.3)

dist_20 = 2942
dist_60 = 2970
dist_100 = 3080
register_distance_us(threshold, dist_20)

sleep(1130)
