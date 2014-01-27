from SimpleCV import Image, Camera, Display
from time import sleep

camera = Camera(prop_set={'width':320, 'height':240})
display = Display(resolution=(320, 240))

mustacheImage = Image("/Users/jharms/Desktop/Mustache.jpg")
mustacheImage = mustacheImage.resize(w=120, h=80)
stacheMask = mustacheImage.createBinaryMask(color1=(10,10,10), color2=(255,255,255))
stacheMask = stacheMask.invert()
#i.save(myDisplay)

def mustachify(frame):
    faces = None
    print frame.listHaarFeatures()
    faces = frame.findHaarFeatures('face')
    if faces:
        for face in faces:
            print "Gesicht bei " + str(face.coordinates())
            frame = frame.blit(mustacheImage, pos=face.coordinates(), mask=stacheMask)
    return frame
    
while not display.isDone():
    frame = camera.getImage()
    frame = mustachify(frame)
    frame.save(display)
    sleep(.1)
