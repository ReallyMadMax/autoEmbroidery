'''
DSB format basics

the top of each file will look like this. anything with an X is unique
The amount of spaces is important

"""
LA:~temp.qe DSC.QEP
ST:      X
CO:  X
+X:    X
-X:    X
+Y:    X
-Y:    X
AX:+    X
AY:+    X
"""

ST -> stitch count
CO -> amount of colour switches
+X, -X -> distance traveled in the X axis, used to tell the machine the width
+Y, -Y -> distance traveled in the Y axis, used to tell the machine the height
AX:(+ or -) -> X end point difference from start point 0 if same. can be negative or positive
AY:(+ or -) -> Y end point difference from start point 0 if same. can be negative or positive

Each embroidery stitch comes in 3 bytes. The first being machine commands, followed by Y and finally X value(s)

stitch | Y = - | X = - |  END  | Color |  NA  |  NA  | Jump
    0       0       0       0       0       0       0       0
Y value
    0       0       0       0       0       0       0       0
X value
    0       0       0       0       0       0       0       0

X and Y are simple calculated using their literal binary value for a theoretical max stitch length of 255?
Machine commands are activated by having a 1 in its respective position
Here are some direct examples

10001000 or 88 = color switch and single stitch after wards
10000000 or 80 = single stitch
10000001 or 81 = jump
11111000 or f8 = end of machine file

The machine will always move BEFORE it stitches in a dsb file
Not sure if necessary but all existing examples show a single stitch after color change

UNIT CONVERSIONS

10 = 1mm so 1 = 0.1mm

1 inch = 25.4mm or 254
'''
from StitchDraw import stitchVisualize
from StitchReader import parseStitch

file = "frame photo.DSB"
colorScheme = [3,4,9,1,5,7,7,9,9,9,9,9,10,11,10,8,4,6,7,8,12,6,7]

content = open(file, "rb")

contents = content.readlines()

content.close()

# only getting the stitch data
contents[0] = contents[0][512:]

stitchArray = []

stitchBytes = [0,0,0]
bytecount = 1
colorCount = 1
stitchCount = 0
for loop in range(len(contents)):
    for line in contents[loop]:
        match bytecount % 3:
            case 1:
                stitchBytes[0] = bin(line)
            case 2:
                stitchBytes[1] = bin(line)
            case 0:
                # our third byte gets added and we can finally group it as a stitch
                stitchBytes[2] = bin(line)
                #print(stitchBytes)
                stitch = parseStitch(stitchBytes)
                stitchArray.append(stitch)
                if "color" in stitch[0]:
                    colorCount += 1
                elif "jump" not in stitch[0]:
                    stitchCount += 1
        bytecount += 1

print(f"stitches: {stitchCount}, colours: {colorCount}")
stitchVisualize(stitchArray, colorScheme)