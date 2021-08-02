class pathMaker():
    def __init__(self,direction)
    self.direction = direction
    self.move()
    
    def move(self):
        global pathList
        pathList.append(self.direction)
        if self.direction == 1:
               self.gridx += 1
        if self.direction == 2:
               self.gridx -= 1
        if self.direction == 3:
               self.gridy +=1
        if self.direction == 4:
               self.gridx -=1
        self.decideMove()

    def decidemove(self):
        if self.direction != 2 and self.gridx < gridSize-1 and self.gridy >= 0 and self.gridy <= gridSize-1:
            if isinstance(blockGrid[self.gridx+1][self.gridy], PathBlock):
                self.direction = 1
                self.move()
                return
            
        if self.direction != 1 and self.gridx > 0 and self.gridy >= 0 and self.gridy <= gridSize-1:
            if isinstance(blockGrid[self.gridx-1][self.gridy], PathBlock):
                self.direction = 2
                self.move()
                return

        if self.direction != 4 and self.gridy < gridSize-1 and self.gridx >= 0 and self.gridx <= gridSize-1:
            if isinstance(blockGrid[self.gridx][self.gridy+1], PathBlock):
                self.direction = 3
                self.move()
                return
                        
        if self.direction != 3 and self.gridy > 0 and self.gridx >= 0 and self.gridx <= gridSize-1:
            if isinstance(blockGrid[self.gridx][self.gridy-1], PathBlock):
                self.direction = 4
                self.move()
                return

        
        
