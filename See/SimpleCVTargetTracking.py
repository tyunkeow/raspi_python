from SimpleCV import Color, Camera, Display, RunningSegmentation, Blob


cam = Camera(-1, {'width': 640, 'height': 420})
rs = RunningSegmentation(.5)

size = cam.getImage().size()
disp = Display(size)

center2 = size[0]/2, size[1]/2

while disp.isNotDone():
    input = cam.getImage()
    input = input.flipHorizontal()

    print "adding image to segmenter"
    rs.addImage(input.erode(5))

    if rs.isReady():
        print "ready!"
        img = rs.getSegmentedImage(False)
        blobs = img.dilate(3).findBlobs(-1, 15, 0)
        #print "ok"

        if blobs is not None:
            #blobs = blobs.sortArea()
            #center1 = int(blobs[-1].minRectX()), int(blobs[-1].minRectY())
            #center2 = 0, 0
            if len(blobs) < 8:
                continue
            print len(blobs)

            total_weight = 0
            dx, dy = 0, 0
            for b in blobs:
                weight = b.area()
                #if weight < 500:
                #    continue
                total_weight += weight
                dx += b.minRectX() * weight
                dy += b.minRectY() * weight
                b.drawRect(input.dl(), Color.RED)
            if total_weight > 0:
                center2 = int(dx / total_weight), int(dy / total_weight)

        #input.dl().circle(center1, 50, Color.BLACK, width=3)
        input.dl().circle(center2, 50, Color.GREEN, width=3)

    print "saving disp"
    input.save(disp)

