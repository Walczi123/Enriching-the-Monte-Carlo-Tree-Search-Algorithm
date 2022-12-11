def get_pieces_to_reverse(array,  player, x, y):
    colour = player
    array[x][y] = colour
    
    neighbours = []
    for i in range(max(0,x-1),min(x+2,8)):
        for j in range(max(0,y-1),min(y+2,8)):
            if array[i][j]!=None:
                neighbours.append([i,j])
    
    convert = []
    for neighbour in neighbours:
        neighX = neighbour[0]
        neighY = neighbour[1]
        if array[neighX][neighY]!=colour:
            path = []
            deltaX = neighX-x
            deltaY = neighY-y
            tempX = neighX
            tempY = neighY
            while 0<=tempX<=7 and 0<=tempY<=7:
                path.append([tempX,tempY])
                value = array[tempX][tempY]
                if value==None:
                    break
                if value==colour:
                    for node in path:
                        convert.append(node)
                    break
                tempX+=deltaX
                tempY+=deltaY
    return convert  