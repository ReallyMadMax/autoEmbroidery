'''
This is are different types of stitches that are available.
Each method will return an array of bytes that contain the stitch from X1, Y1 to X2, Y2
There will also be optional parameters for length and density
Not yet sure how to account for pull compensation
'''
import math
from StitchReader import parseStitch, writeStitch
from StitchDraw import stitchVisualize
import random
import copy

defaultLength = 20
defaultDensity = 5
defaultAngle = 0

# length of 20 is 2mm
# goes from point A to B
def runStitch(x1, y1, x2, y2, length = defaultLength):
    x = 0
    y = 0
    direct = math.ceil(math.sqrt(((x2-x1)**2) + ((y2-y1)**2)))
    #print(f"direct: {direct}")
    output = []
    # if there is only a single stitch
    if direct < length + length/2:
        output = writeStitch(x2-x1, y2-y1)
    # logic for multiple stitches
    else:
        fraction = int(direct / length)
        #print(f"fraction: {fraction}")
        fractionX = int((x2 - x1) / fraction)
        fractionY = int((y2 - y1) / fraction)
        #print(f"fractionX: {fractionX}, fractionY: {fractionY}")

        for i in range(fraction):
            output += writeStitch(fractionX, fractionY)
            x += fractionX
            y += fractionY
        # finding any remainder x or y values so we make sure we land exactly on our x2 and y2
        remainderX = abs((x2-x1) - (fractionX*fraction))
        remainderY = abs((y2-y1) - (fractionY*fraction))
        #print(f"remainderX: {remainderX}, remainderY: {remainderY}")

        totalStiches = int(len(output))

        # distributing the remainder X between all of the existing x values
        for split in range(remainderX):
            pos = split % totalStiches
            newX = int(output[pos][2],2) + 1
            x += 1
            output[pos][2] = bin(newX)

        # distributing the remainder Y between all of the existing y values
        for split in range(remainderY):
            pos = split % totalStiches
            newY = int(output[pos][1],2) + 1
            y += 1
            output[pos][1] = bin(newY)

        #print(f"final X: {x}, final Y: {y}")

        #randomly shuffle all values so the slighlty longer moves are more distrbuted and not all right beside each other
        random.shuffle(output)

        #for stitch in output:
        #    print(f"x: {parseStitch(stitch)[2]}, y: {parseStitch(stitch)[1]}")
        #print("END RUN STITCH")
    return output

# goes from point A to B to A
def runStitchDouble(x1, y1, x2, y2, length = defaultLength):
    backwards = []
    forwards = runStitch(x1, y1, x2, y2, length)

    #this is annoying but needed so we dont overwrite the values in forwards
    cloneList = copy.deepcopy(forwards)

    #go through the stitches in reverse order so we go directly backwards
    for stitch in reversed(cloneList):
        byte1 = stitch[0][2:]
        newStr = "1"
        # inverting the Y sign
        if byte1[1] == "0":
            newStr += "1"
        else:
            newStr += "0"
        # inverting the X sign
        if byte1[2] == "0":
            newStr += "1"
        else:
            newStr += "0"

        newStr += byte1[3:]
        stitch[0] = "0b" + newStr
        backwards.append(stitch)

    #for stitch in backwards:
    #    print(f"x: {parseStitch(stitch)[2]}, y: {parseStitch(stitch)[1]}")

    #print("END RUN STITCH DOUBLE")
    #print(forwards)
    #print(backwards)
    return (forwards + backwards)

# triple stacked run stitch. Goes A -> B -> A -> B
def runStitchTriple(x1, y1, x2, y2, length = defaultLength):
    double = runStitchDouble(x1, y1, x2, y2, length)
    half = int(len(double)/2)
    return double + double[:half]

# needs to be passed an array of 3 stitches at a minimum
# we add the first vector to the end of the list so it makes a closed shape.
def fillStitch(vectorList, length = defaultLength, density = defaultDensity, angle = defaultAngle):

    minX,minY,maxX,maxY = (0,0,0,0)

    # creating the bounding boxes for our shape
    for item in vectorList:
        if item[0] > maxX:
            maxX = item[0]
        elif item[0] < minX:
            minX = item[0]
        if item[1] > maxY:
            maxY = item[1]
        elif item[1] < minY:
            minY = item[1]



    output, arrays, centerLines, edgeLines, areas, triangleVectors, angles = ([],[],[],[],[],[],[])
    totalArea = 0

    #arrays.append(runStitch(0,0,middleX,middleY,length))

    vectorList.append(vectorList[0])
    #print(vectorList)

    for pos in range(len(vectorList)-1):
        vec1 = vectorList[pos]
        x1 = vec1[0]
        y1 = vec1[1]
        vec2 = vectorList[pos+1]
        x2 = vec2[0]
        y2 = vec2[1]
        stitches = runStitch(x1,y1,x2,y2,length)
        arrays.append(stitches)
        # lines for our triangles
        edgeLines.append(math.sqrt(((x2-x1)**2) + ((y2-y1)**2)))
    
    for array in arrays:
        for stitches in array:
            output.append(stitches)

    # calculating the area of the shape maybe

    print(f"box area:x1,y1,x2,y2: {minX},{minY},{maxX},{maxY}")

    return output

# calculate area of triangle when 3 sides are known
def heronFormula(a,b,c):
    s = (a+b+c)/2
    #area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    return 0

def cosineLaw(a,b,c):
    angle = ((a**2)-(b**2)-(c**2))/((-2)*b*c)
    #angle = math.acos(angle)*180/math.pi
    return angle


shape = [[0,0],[200,50],[300,300],[100,200],[100,100],[-25,100]]
parsed = []
for stitches in fillStitch(shape):
    parsed.append(parseStitch(stitches))
stitchVisualize(parsed,[1,1])