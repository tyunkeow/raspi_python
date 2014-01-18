from espeak import espeak
from datetime import datetime

t = datetime.now().strftime("%k %M")
espeak.synth("You're listening to Luke's radio station. The time is %s"%t)
