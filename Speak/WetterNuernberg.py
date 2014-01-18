#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedparser
from Text2Wav import googleSpeak

codes = {
0: "tornado",
1: "tropical storm",
2: "hurricane",
3: "severe thunderstorms",
4: "thunderstorms",
5: "mixed rain and snow",
6: "mixed rain and sleet",
7: "mixed snow and sleet",
8: "freezing drizzle",
9: "niesel", #"drizzle",
10: "freezing rain",
11: "regnerisch", #"showers",
12: "regnerisch", #"showers",
13: "snow flurries",
14: "light snow showers",
15: "blowing snow",
16: "snow",
17: "hail",
18: "sleet",
19: "dust",
20: "neblig", #"foggy",
21: "haze",
22: "smoky",
23: "blustery",
24: "windig", #"windy",
25: "kalt", #"cold",
26: "bewoelkt", #"cloudy",
27: "ueberwiegend bewoelkt", #"mostly cloudy (night)",
28: "ueberwiegend bewoelkt", #"mostly cloudy (day)",
29: "teilweise bewoelkt", #"partly cloudy (night)",
30: "teilweise bewoelkt", #"partly cloudy (day)",
31: "klar", #"clear (night)",
32: "sonnig", #"sunny",
33: "klar", #"fair (night)",
34: "heiter", #"fair (day)",
35: "mixed rain and hail",
36: "hot",
37: "isolated thunderstorms",
38: "scattered thunderstorms",
39: "scattered thunderstorms",
40: "scattered showers",
41: "heavy snow",
42: "scattered snow showers",
43: "heavy snow",
44: "teilweise bewoelkt", #"partly cloudy",
45: "thundershowers",
46: "snow showers",
47: "isolated thundershowers"
}

# RSS wird über cron in /home/pi/data/yahooforecast_nue.rss geladen
#url = "http://weather.yahooapis.com/forecastrss?w=680564&u=c"
feedfile = '/home/pi/data/yahooforecast_nue.rss'

def loadWetterDaten():
    print "Loading and parsing {}".format(feedfile)
    feed = feedparser.parse( feedfile )
    print "loaded."
    condition = feed['items'][0]["yweather_condition"]
    return { 'temp': condition['temp'], 'text': codes[int(condition['code'])] }

def formatWetter():
    data = loadWetterDaten()
    #print data
    return "Die Temperatur betraegt {0[temp]} Grad Celsius. Das Wetter ist {0[text]}".format(data)

def getWetterAudio(volume, speed):
    filename = "/home/pi/data/audio/yahooforecast_nue.wav"
    text = formatWetter()
    googleSpeak(text, filename, volume, speed)

if __name__ == "__main__":
    getWetterAudio(10, 1)
