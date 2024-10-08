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