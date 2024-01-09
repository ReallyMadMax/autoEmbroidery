'''
This is are different types of stitches that are available.
Each method will return an array of bytes that contain the stitch from X1, Y1 to X2, Y2
There will also be optional parameters for length and density
Not yet sure how to account for pull compensation
'''
import math
import StitchReader

# length of 20 is 2mm
def runStitch(x1, y1, x2, y2, length = 20):
    direct = math.ceil(math.sqrt(((x2-x1)**2) + ((y2-y1)**2)))
    print(f"direct: {direct}")
    output = []
    # if there is only a single stitch
    if direct <= length:
        output = StitchReader.writeStitch(x2, y2)
    # logic for multiple stitches
    else:
        if direct > length + length/2:
            fraction = direct / length
            print(f"fraction: {fraction}")
            fraction = int(fraction)
            fractionX = (x2 - x1) / fraction
            fractionX = int(fractionX)
            fractionY = (y2 - y1) / fraction
            fractionY = int(fractionY)
            print(f"fractionX: {fractionX}, fractionY: {fractionY}")

            for i in range(1,fraction+1):
                output += StitchReader.writeStitch(fractionX, fractionY)
            # makes sure the last stitch is the appropriate length, so we can get to exactly x2 and y2
            if fractionX*fraction % x2-x1 == 0:
                output += StitchReader.writeStitch(fractionX, fractionY)
            else:
                remainderX = (x2-x1) - (fractionX*fraction)
                remainderY = (y2-y1) - (fractionY*fraction)
                output += StitchReader.writeStitch(x1 + fractionX*fraction + remainderX, y1 + fractionY*fraction + remainderY)

    # test
    return output

print(runStitch(0,0,200,200))