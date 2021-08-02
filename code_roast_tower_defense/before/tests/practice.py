blockSize = 20
blockList = [1,2,3,4,2]

def positionFormula(distance):
    xPos = 0
    yPos = 0
    blocks = (distance-(distance%blockSize))/blockSize

    for i in range(blocks):
        if blockList[i] == 1:
            xPos += blockSize
        elif blockList[i] == 2:
            xPos -= blockSize
        elif blockList[i] == 3:
            yPos += blockSize
        else:
            yPos -= blockSize
    if distance%blockSize != 0:
        if blockList[blocks] == 1:
            xPos += (distance%blockSize)
        elif blockList[blocks] == 2:
            xPos -= (distance%blockSize)
        elif blockList[blocks] == 3:
            yPos += (distance%blockSize)
        else:
            yPos -= (distance%blockSize)

    return xPos,yPos

print positionFormula(70)


