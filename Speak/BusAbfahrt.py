# -*- coding: utf-8 -*-
from datetime import date
import time

busdata_spitalhof = {
    "wo": {
        5: [4, 14, 24, 34]
    },
    "sa": {
        1: [1, 30],
        6: [1, 30]
    },
    "so": {}
}

def findNaechsteStunde(key, stunde, minute):
    while not stunde in busdata_spitalhof[key]:
        minute = 0
        stunde = stunde + 1
    return [stunde, minute]

def findNaechsteMinute(key, stunde, minute):
    while not minute in busdata_spitalhof[key][stunde]:
        minute = minute + 1
        #print minute
    return minute


weekday = time.strftime("%a")
key = "wo"
if weekday == "Sat":
    key = "sa"
    
akt_stunde = int(time.strftime("%H"))
akt_minute = int(time.strftime("%M"))
print "akt_min" + str(akt_minute)
stunde, akt_minute = findNaechsteStunde(key, akt_stunde, akt_minute)

print "akt_min" + str(akt_minute)
minute = findNaechsteMinute(key, stunde, akt_minute)

print "Der naechste Bus fährt in {} Stunden und {} Minuten".format((stunde-akt_stunde), (minute-akt_minute))
