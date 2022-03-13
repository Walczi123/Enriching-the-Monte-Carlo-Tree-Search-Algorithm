def get_pieces_to_reverse(array,  player, x, y):
    #Must copy the passedArray so we don't alter the original
    # array = deepcopy(state)
    #Set colour and set the moved location to be that colour
    colour = player
    array[x][y] = colour
    
    #Determining the neighbours to the square
    neighbours = []
    for i in range(max(0,x-1),min(x+2,8)):
        for j in range(max(0,y-1),min(y+2,8)):
            if array[i][j]!=None:
                neighbours.append([i,j])
    
    #Which tiles to convert
    convert = []

    #For all the generated neighbours, determine if they form a line
    #If a line is formed, we will add it to the convert array
    for neighbour in neighbours:
        neighX = neighbour[0]
        neighY = neighbour[1]
        #Check if the neighbour is of a different colour - it must be to form a line
        if array[neighX][neighY]!=colour:
            #The path of each individual line
            path = []
            
            #Determining direction to move
            deltaX = neighX-x
            deltaY = neighY-y

            tempX = neighX
            tempY = neighY

            #While we are in the bounds of the board
            while 0<=tempX<=7 and 0<=tempY<=7:
                path.append([tempX,tempY])
                value = array[tempX][tempY]
                #If we reach a blank tile, we're done and there's no line
                if value==None:
                    break
                #If we reach a tile of the player's colour, a line is formed
                if value==colour:
                    #Append all of our path nodes to the convert array
                    for node in path:
                        convert.append(node)
                    break
                #Move the tile
                tempX+=deltaX
                tempY+=deltaY

    return convert  