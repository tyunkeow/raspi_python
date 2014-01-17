import os  

def say(something):  
  os.system('espeak -ven+f2 --stdout "{0}"| aplay'.format(something))

a, b = 0, 1  
say(a)  
while b < 50:  
  say(b)  
  a, b = b, a+b  

