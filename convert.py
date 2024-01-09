'''
import tkinter
import turtle
from random import randint
from tkinter import *

x = 0
y = 0

count = 0

zoomFactor = 100

# X, Y, stitch type
def BinToVal(binstr,byteNum):
    returnVal = [0,0,""]
    #print(binstr)
    match byteNum:
        case 0:
            if binstr[0] == "1":
                returnVal[1] += 1
            if binstr[1] == "1":
                returnVal[1] -= 1
            if binstr[2] == "1":
                returnVal[1] += 9
            if binstr[3] == "1":
                returnVal[1] -= 9
            if binstr[4] == "1":
                returnVal[0] -= 9
            if binstr[5] == "1":
                returnVal[0] += 9
            if binstr[6] == "1":
                returnVal[0] -= 1
            if binstr[7] == "1":
                returnVal[0] += 1
        case 1:
            if binstr[0] == "1":
                returnVal[1] += 3
            if binstr[1] == "1":
                returnVal[1] -= 3
            if binstr[2] == "1":
                returnVal[1] += 27
            if binstr[3] == "1":
                returnVal[1] -= 27
            if binstr[4] == "1":
                returnVal[0] -= 27
            if binstr[5] == "1":
                returnVal[0] += 27
            if binstr[6] == "1":
                returnVal[0] -= 3
            if binstr[7] == "1":
                returnVal[0] += 3
        case 2:
            if binstr[0] == "1":
                returnVal[2] += "-jump"
            if binstr[1] == "1":
                returnVal[2] += "-color change"
            if binstr[2] == "1":
                returnVal[1] += 81
            if binstr[3] == "1":
                returnVal[1] -= 81
            if binstr[4] == "1":
                returnVal[0] -= 81
            if binstr[5] == "1":
                returnVal[0] += 81
            if binstr[6] == "1":
                returnVal[2] += "-set"
            if binstr[7] == "1":
                returnVal[2] += "-set"

    return returnVal

def zoom(t, amount):
    global zoomFactor
    zoomFactor += amount
    t.shapesize(zoomFactor)

file = open("AXTX1.dst.txt", "r")
#print(file.read())

file = file.readlines()

coordinates = [0,0,""]

needle = turtle.Turtle()
screen = turtle.Screen()

image = "photos/circlegrid.gif"

screen.addshape(image)
turtle.shape(image)

root = tkinter.Tk()
root.title('turn mouse wheel')

# with Windows OS
root.bind("<MouseWheel>",zoom(turtle, -0.25))

# ... which is the same size as our image
# now set the background to our space image
needle.shape("circle")
needle.shapesize(0.25)
needle.penup()
needle.color("black")

for line in file[10:len(file)-1]:
    line = line[7:]
    line = line.split(" ")
    #print(line)
    for hexval in line:
        #print(hexval)
        if len(line) != 1:
            if hexval[:1] == '\n':
                hexval = hexval[1:]

            hexToInt = int(hexval, 16)
            intToBin = format(hexToInt, '08b')
            #print(intToBin)
            #print(BinToVal(intToBin,count))

            coordinates[0] += BinToVal(intToBin,count)[0]
            coordinates[1] += BinToVal(intToBin,count)[1]
            coordinates[2] += BinToVal(intToBin,count)[2]

            count += 1
            if count == 3:
                count = 0
                print(coordinates)
                x += coordinates[0]
                y += coordinates[1]

                needle.forward(coordinates[0])
                needle.left(90)
                needle.forward(coordinates[1])
                needle.right(90)
                if "color" in coordinates[2]:
                    needle.color("violet")
                if "jump" in coordinates[2]:
                    needle.penup()
                else:
                    needle.pendown()
                    needle.stamp()
                print(f"x = {x}, y = {y}")
                coordinates = [0,0,""]

turtle.mainloop()
'''