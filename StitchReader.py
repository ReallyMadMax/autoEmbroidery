
#bytes need to be passed as binary
def parseStitch(stitchBytes):
    stitch = ["", int(stitchBytes[1], 2), int(stitchBytes[2], 2)]

    byte1 = stitchBytes[0][2:]

    if byte1[0] == "1":
        stitch[0] += "stitch"
    if byte1[1] == "1":
        stitch[1] *= -1
    if byte1[2] == "1":
        stitch[2] *= -1
    if byte1[4] == "1":
        stitch[0] += " color change"
    if byte1[7] == "1":
        stitch[0] = " jump"
    if byte1[3] == "1":
        stitch[0] = "end"
    #print(stitch)
    return stitch

# needs to return 3 bytes
def writeStitch(x,y):
    if x >= 0 and y >= 0:
        byte1 = b"10000000"
    elif x < 0 and y < 0:
        byte1 = b"11100000"
    elif x < 0:
        byte1 = b"10100000"
    elif y < 0:
        byte1 = b"11000000"
    byte2 = bin(abs(y))
    byte3 = bin(abs(x))
    return byte1,byte2,byte3

def writeJump(x,y):
    if x >= 0 and y >= 0:
        byte1 = b"00000001"
    elif x < 0 and y < 0:
        byte1 = b"01100001"
    elif x < 0:
        byte1 = b"00100001"
    elif y < 0:
        byte1 = b"01000001"
    byte2 = bin(abs(y))
    byte3 = bin(abs(x))
    return byte1,byte2,byte3

def writeColorChange():
    byte1 = b"10001000"
    byte2 = bin(0)
    byte3 = bin(0)
    return byte1,byte2,byte3

def writeEnd():
    byte1 = b"11111000"
    byte2 = bin(0)
    byte3 = bin(0)
    return byte1,byte2,byte3
