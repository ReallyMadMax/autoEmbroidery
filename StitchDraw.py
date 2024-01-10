import turtle
from turtle import Turtle, Screen
import math
from tkinter import ALL, EventType

def stitchVisualize(file, colorOrder):
    # super basic tutrle drawing. to represent our stitches
    needle = turtle.Turtle()
    needle.speed("fast")
    #turtle.tracer(0,0)
    needle.shape("circle")
    needle.shapesize(0.25)
    needle.penup()

    # dictionary to set our colors that are already on the machine
    colors = {1: "white", 2: "black", 3: "grey", 4: "blue", 5: "yellow",
              6: "red", 7: "orange", 8: "purple", 9: "green", 10: "brown",
              11: "beige", 12: "pink"}


    colorArray = colorOrder
    needle.color(colors[colorArray[0]])
    color = 1

    for pos in range(len(file)):

        if "color" in file[pos][0]:
            needle.color(colors[colorArray[color]])
            color +=1
        if "jump" in file[pos]:
            needle.penup()
        elif "jump" not in file[pos-1][0]:
            needle.pendown()
            # stamp will show where the individual stich is but also makes it very laggy
            needle.stamp()

        x = file[pos][2]
        y = file[pos][1]

        if x != 0 and y != 0:
            if x < 0 and y < 0:
                needle.setheading(180 + math.degrees(math.atan(y/x)))
            elif x < 0 < y:
                needle.setheading(180 + math.degrees(math.atan(y/x)))
            elif x > 0 and y > 0:
                needle.setheading(math.degrees(math.atan(y/x)))
            elif x > 0 > y:
                needle.setheading(math.degrees(math.atan(y/x)))
            needle.forward(math.sqrt((x**2) + (y**2)))
        elif x != 0:
            needle.setheading(0)
            needle.forward(x)
        elif y != 0:
            needle.setheading(90)
            needle.forward(y)

    screen = needle.getscreen()
    canvas = screen.getcanvas()

    # zoom into canvas. could be moved elsewhere in the future
    def do_zoom(event):
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        factor = 1.001 ** event.delta
        canvas.scale(ALL, x, y, factor, factor)

    def reset(event):
        baseline = 500
        canvas.canvasx(baseline)
        canvas.canvasy(baseline)
        canvas.scale(baseline, baseline)

    canvas.bind("<MouseWheel>", do_zoom)
    canvas.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
    canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))
    canvas.bind("a", reset)
    screen.mainloop()
