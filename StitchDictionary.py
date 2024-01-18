'''
This is are different types of stitches that are available.
Each method will return an array of bytes that contain the stitch from X1, Y1 to X2, Y2
There will also be optional parameters for length and density
Not yet sure how to account for pull compensation
'''
import math
from StitchReader import parseStitch, writeStitch, writeJump
from StitchDraw import stitchVisualize
import random
import copy

defaultLength = 20
defaultDensity = 5
defaultAngle = 0


# length of 20 is 2mm
# goes from point A to B
def runStitch(x1, y1, x2, y2, length=defaultLength):
    x = 0
    y = 0
    direct = math.ceil(math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2)))
    # print(f"direct: {direct}")
    output = []
    # if there is only a single stitch
    if direct < length + length / 2:
        output.append(writeStitch(x2 - x1, y2 - y1))
    # logic for multiple stitches
    else:
        fraction = int(direct / length)
        # print(f"fraction: {fraction}")
        fractionX = int((x2 - x1) / fraction)
        fractionY = int((y2 - y1) / fraction)
        # print(f"fractionX: {fractionX}, fractionY: {fractionY}")

        for i in range(fraction):
            output.append(writeStitch(fractionX, fractionY))
            x += fractionX
            y += fractionY
        # finding any remainder x or y values so we make sure we land exactly on our x2 and y2
        remainderX = abs((x2 - x1) - (fractionX * fraction))
        remainderY = abs((y2 - y1) - (fractionY * fraction))
        # print(f"remainderX: {remainderX}, remainderY: {remainderY}")

        totalStiches = int(len(output))

        # distributing the remainder X between all of the existing x values
        for split in range(remainderX):
            pos = split % totalStiches
            newX = int(output[pos][2], 2) + 1
            x += 1
            output[pos][2] = bin(newX)

        # distributing the remainder Y between all of the existing y values
        for split in range(remainderY):
            pos = split % totalStiches
            newY = int(output[pos][1], 2) + 1
            y += 1
            output[pos][1] = bin(newY)

        # print(f"final X: {x}, final Y: {y}")

        # randomly shuffle all values so the slighlty longer moves are more distrbuted and not all right beside each other
        random.shuffle(output)

        # for stitch in output:
        #    print(f"x: {parseStitch(stitch)[2]}, y: {parseStitch(stitch)[1]}")
        # print("END RUN STITCH")
    return output


# goes from point A to B to A
def runStitchDouble(x1, y1, x2, y2, length=defaultLength):
    backwards = []
    forwards = runStitch(x1, y1, x2, y2, length)

    # this is annoying but needed so we dont overwrite the values in forwards
    cloneList = copy.deepcopy(forwards)

    # go through the stitches in reverse order so we go directly backwards
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

    # for stitch in backwards:
    #    print(f"x: {parseStitch(stitch)[2]}, y: {parseStitch(stitch)[1]}")

    # print("END RUN STITCH DOUBLE")
    # print(forwards)
    # print(backwards)
    return (forwards + backwards)


# triple stacked run stitch. Goes A -> B -> A -> B
def runStitchTriple(x1, y1, x2, y2, length=defaultLength):
    double = runStitchDouble(x1, y1, x2, y2, length)
    half = int(len(double) / 2)
    return double + double[:half]


# needs to be passed an array of 3 stitches at a minimum
# we add the first vector to the end of the list, so it makes a closed shape.
def fillStitch(vectorList, length=defaultLength, density=defaultDensity, angle=defaultAngle):
    # vectorList.append(vectorList[0])
    # print(vectorList)
    stitches_to_stitch = []
    shape_segments = []
    shape_segments.append([])
    segment_count = 1
    # find the points at the extremes
    # find which points are tangent to the angle line
    # ( if there are multiple, then choose the furthest one on either side )
    min_vector = vectorList[0]
    max_vector = vectorList[0]
    for vector in vectorList:
        if vector[1] < min_vector[1]:
            min_vector = vector
        if vector[1] > max_vector[1]:
            max_vector = vector

    # adding all the points as connecting lines to a list
    segments = []
    for v in range(len(vectorList)):
        segments.append([vectorList[v-1], vectorList[v]])

    number_of_slices = math.ceil((max_vector[1] - min_vector[1])/density)
    # defining the direction vector of the angle line for calculations
    line = [[0, min_vector[1]], [1, min_vector[1]]]

    for s in range(number_of_slices):
        slice = [[line[0][0], line[0][1]], [line[1][0], line[1][1]]]
        slice[0][1] += s * density
        slice[1][1] += s * density

        intersections = []
        for segment in segments:
            if line_intersects_segment(slice, segment):
                intersections.append(get_intersection_point(slice, segment))

        if intersections:
            intersections.sort()
            # must remove stitches that don't go anywhere
            i = 1
            while i < len(intersections):
                if intersections[i-1] == intersections[i]:
                    intersections.pop(i-1)
                    intersections.pop(i-1)
                else:
                    i += 1

            # flip every other row so that it lines up for the proper stitching order
            if s % 2 == 1 and len(intersections) <= 2:
                intersections.reverse()

            # for each gap there will be 2 new limits. ex 1 jump = 4 limits, 0 jumps = 2 limits
            # these are stored in the intersections array
            # adding the lines that are within the shape
            section = 1
            if len(intersections) > 2:
                if len(shape_segments) < len(intersections) - 1 :
                    shape_segments.append([])
                    shape_segments.append([])

                for lim in range(0, len(intersections), 2):
                    if s % 2 == 0:
                        shape_segments[section].append(intersections[lim])
                        shape_segments[section].append(intersections[lim+1])
                    else:
                        shape_segments[section].append(intersections[lim+1])
                        shape_segments[section].append(intersections[lim])
                    section += 1
                    segment_count = max(segment_count,section)
            else:
                shape_segments[0] += intersections

    # calculating the shape_segments max x and y values to properly calculate the jump stitch
    segment_displacement = []

    jumps = len(shape_segments) -1

    # weird math for calculating the segment displacement properly
    for i in range (jumps):

        x = -shape_segments[i][-1][0] + shape_segments[(i+1)][0][0]
        y = -(shape_segments[i][-1][1] + shape_segments[(i+1)][1][1]) + density*2

        segment_displacement.append([x,y])

    for shape in shape_segments:

        for line in range(0, len(shape), 2):

            x1 = shape[line][0]
            y1 = shape[line][1]
            if (line + 1) % len(shape) == 0:
                x2 = vectorList[0][0]
                y2 = vectorList[0][1]
            else:
                x2 = shape[(line+1)][0]
                y2 = shape[(line+1)][1]

            #print(f"x1,y1: {x1}, {y1}")
            #print(f"x2,y2: {x2}, {y2}")

            row = runStitch(x1, y1, x2, y2, length)

            for stitch in row:
                stitches_to_stitch.append(stitch)

            # adding line along the outline from last end point to the start of the new line
            if line + 2 < len(shape):
                p0 = shape[line+1]
                p1 = shape[line+2]
                for stitch in runStitch(p0[0], p0[1], p1[0], p0[1]+density, length):
                    stitches_to_stitch.append(stitch)
            else:
                # todo calculate proper jump coordinates
                if shape_segments.index(shape) < jumps:
                    x = segment_displacement[shape_segments.index(shape)][0]
                    y = segment_displacement[shape_segments.index(shape)][1]
                    stitches_to_stitch.append(writeJump(x,y))

    return stitches_to_stitch

def to_points(point):
    return int(point[0]), int(point[1])

def line_to_points(start, end):
    start_points = to_points(start)
    end_points = to_points(end)
    return start_points[0], start_points[1], end_points[0], end_points[0]

def line_intersects_segment(line, segment):
    x1 = segment[0][0]
    y1 = segment[0][1]
    x2 = segment[1][0]
    y2 = segment[1][1]
    x3 = line[0][0]
    y3 = line[0][1]
    x4 = line[1][0]
    y4 = line[1][1]

    if ((x4 - x3) * (y1 - y3) - (x1 - x3) * (y4 - y3)) * ((x4 - x3) * (y2 - y3) - (x2 - x3) * (y4 - y3)) <= 0:
        return True
    else:
        return False


def get_intersection_point(line, segment):
    x1 = segment[0][0]
    y1 = segment[0][1]
    x2 = segment[1][0]
    y2 = segment[1][1]
    x3 = line[0][0]
    y3 = line[0][1]
    x4 = line[1][0]
    y4 = line[1][1]

    # write the lines in general form
    # convert from y-y1 = m(x-x1) where m =
    # ax + by + c = 0
    a1 = y2 - y1
    b1 = -(x2 - x1)
    c1 = x2*y1 - y2*x1

    a2 = y4 - y3
    b2 = -(x4 - x3)
    c2 = x4 * y3 - y4 * x3

    # using cross multiplication rule
    if a1 != a2 or c1 != c2:
        x = int((b1*c2 - b2*c1)/(a1*b2 - a2*b1))
        y = int((c1*a2 - c2*a1)/(a1*b2 - a2*b1))

        return [x, y]
    else:
        return segment[0]

arrow = [[300, 0], [0, 150], [-300, 0], [0, 300]]

shape = [[100,0],[100,100],[0,100],[0,0]]
parsed = []
for stitches in fillStitch(shape, density=5):
    parsed.append(parseStitch(stitches))
stitchVisualize(parsed, [2, 2])
