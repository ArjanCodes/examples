#IMPORTANT INFORMATION: the use of 'self' ALWAYS refers to the class that it is in. EVERY FUNCTION INSIDE OF A CLASS MUST DECLARE SELF! ex: 'def exampleFunction(self, input1, input2):

try:
	from Tkinter import * #imports the tkinter database, allowing the use of it in the program
except:
	from tkinter import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk
import random
import math
gridSize = 30 #the height and width of the array of blocks
blockSize = 20 #pixels wide of each block
mapSize = gridSize*blockSize
blockGrid = [[0 for y in range(gridSize)] for x in range(gridSize)] #creates the array for the grid
blockDictionary = ["NormalBlock", "PathBlock","WaterBlock"]
monsterDictionary = ["Monster1", "Monster2"]
blockNumberDictionary = {"Normal Block":0, "Path Block":1, "Water Block": 2}
blockPlaceDictionary = {"Normal Block":"NormalBlock", "Path Block":"PathBlock", "Water Block": "WaterBlock"}
towerGrid = [[None for y in range(gridSize)] for x in range(gridSize)]
monsters = []
projectiles = []
health = 50
money = 1000
selectedTower = "<None>"

class Game(): #the main class that we call "Game"
     def __init__(self): #setting up the window for the game here
          self.root=Tk() #saying this window will use tkinter
          self.root.title("Tower Defense Ultra Mode")
          self.RUN=True #creating a variable RUN. does nothing yet.
          self.root.protocol("WM_DELETE_WINDOW", self.end)

          self.frame = Frame(master= self.root)
          self.frame.grid(row = 0, column = 0)

          self.canvas = Canvas(master = self.frame, width=mapSize, height=mapSize, bg = "white", highlightthickness = 0) #actually creates a window and puts our frame on it
          self.canvas.grid(row = 0,column = 0,rowspan = 2, columnspan = 1) #makes the window called "canvas" complete

          self.displayboard = Displayboard(self)
          
          self.infoboard = Infoboard(self)

          self.towerbox = Towerbox(self)

          self.images = Images()

          self.mouse = Mouse(self)

          self.gameMap = Map()

          self.empty = Image.new("RGBA", (mapSize, mapSize), (255,255,255,0))
          self.empty.save("images/mapImages/changeImage.png")

          self.changeImage = ImageTk.PhotoImage(Image.open("images/mapImages/changeImage.png"))

          self.run() #calls the function 'def run(self):'

          self.root.mainloop() #starts running the tkinter graphics loop

     def run(self):
          if self.RUN is True: #always going to be true for now
               self.update() #calls the function 'def update(self):'
               self.paint() #calls the function 'def paint(self):'
               
               self.root.after(50, self.run) #does a run of the function every 1/100 seconds (i think)
            
     def end(self):
        self.root.destroy() #closes the game window and ends the program

     def update(self):
         self.mouse.update()
         self.displayboard.update()
          
     def paint(self):
          self.canvas.delete(ALL) #clear the screen
          self.gameMap.paint(self.canvas)
          self.canvas.create_image(0,0, image = self.changeImage, anchor = NW)
          self.mouse.paint(self.canvas) #draw the mouse dot by going to its 'def paint(canvas):' command
          self.displayboard.paint()

class Map():
    def __init__(self):
        self.image = None
        self.map = "LeoMap"
        self.loadMap(self.map)
    def loadMap(self,mapName):
        self.drawnMap = Image.new("RGBA", (mapSize, mapSize), (255,255,255,255))
        self.mapFile = open("texts/mapTexts/"+mapName+".txt","r")
        self.gridValues = list(map(int, (self.mapFile.read()).split()))
        for y in range(gridSize):
              for x in range(gridSize):
                   global blockGrid
                   self.blockNumber = self.gridValues[gridSize*y + x]
                   self.blockType = globals()[blockDictionary[self.blockNumber]]
                   blockGrid[x][y] = self.blockType(x*blockSize+blockSize/2,y*blockSize+blockSize/2,self.blockNumber,x,y) #creates a grid of Blocks
                   blockGrid[x][y].paint(self.drawnMap)
        self.drawnMap.save("images/mapImages/"+mapName+".png")
        self.image = Image.open("images/mapImages/"+mapName+".png")
        self.image = ImageTk.PhotoImage(self.image)

    def saveMap(self):
        self.mapFile = open("texts/mapTexts/"+self.map+".txt","w")
        for y in range(gridSize):
              for x in range(gridSize):
                  self.mapFile.write(str(blockGrid[x][y].blockNumber) + " ")
        self.mapFile.close()

    def paint(self, canvas):
         canvas.create_image(0,0, image = self.image, anchor = NW)

class SaveMapButton:
     def __init__(self,game):
          self.game = game
          self.x = 450
          self.y = 25
          self.xTwo = 550
          self.yTwo = 50
          self.canPress = True

     def checkPress(self, click, x, y):
          if x >=self.x and y >= self.y and x <= self.xTwo and y <= self.yTwo:
                if self.canPress and click:
                     print("Map Saved")
                     self.game.gameMap.saveMap()
                     self.canPress = False
                     
     def paint(self, canvas):
          if self.canPress:
               self.color = "blue"
          else:
               self.color = "red"
               self.canPress = True
          canvas.create_rectangle(self.x, self.y, self.xTwo, self.yTwo, fill=self.color, outline = self.color) #draws a rectangle where the pointer is
          canvas.create_text(500,37,text = "Save Button")
class Infoboard:
     def __init__(self, game):
          self.canvas = Canvas(master = game.frame, width = 162, height = 174, bg = "gray", highlightthickness = 0)
          self.canvas.grid(row = 0, column = 1)
          self.text = "<None>"
          self.paint()

     def displaySpecific(self,tower):
          tower.display(self)
          self.paint()

     def displayGeneric(self,tower):
          self.text = tower
          self.paint()
          
     def paint(self):
          self.canvas.delete(ALL) #clear the screen
          self.canvas.create_text(80,80,text = self.text)

class Displayboard:
    def __init__(self, game):
          self.canvas = Canvas(master = game.frame, width = 600, height = 80, bg = "gray", highlightthickness = 0)
          self.canvas.grid(row = 2, column = 0)
          self.saveMapButton = SaveMapButton(game)
          self.paint()
    def update(self):
        pass
    
    def paint(self):         
          self.canvas.delete(ALL) #clear the screen
          self.saveMapButton.paint(self.canvas)
               

class Towerbox:
     def __init__(self, game):
          self.game = game
          self.box = Listbox(master =game.frame, selectmode = "SINGLE", font = ("times",20), height = 21, width = 16, bg = "gray", fg = "dark blue", bd = 1, highlightthickness = 0)
          self.box.insert(END, "<None>")
          for i in blockPlaceDictionary:
               self.box.insert(END, i)
          for i in range(50):
               self.box.insert(END, "<None>")
          self.box.grid(row = 1, column = 1, rowspan = 2)
          self.box.bind("<<ListboxSelect>>", self.onselect)
     def onselect(self,event):
          global selectedTower
          selectedTower = str(self.box.get(self.box.curselection()))
          self.game.infoboard.displayGeneric(selectedTower)
class Mouse():
     def __init__(self, game): #when i define a "Mouse", this is what happens
          self.game = game
          self.x = 0
          self.y = 0
          self.gridx = 0
          self.gridy = 0
          self.xoffset = 0
          self.yoffset = 0
          self.pressed = False
          self.color = "light blue"
          game.root.bind("<Button-1>", self.clicked) #whenever left mouse button is pressed, go to def released(event)
          game.root.bind("<ButtonRelease-1>", self.released) #whenever left mouse button is released, go to def released(event)
          game.root.bind("<Motion>", self.motion) #whenever left mouse button is dragged, go to def released(event)

     def clicked(self, event):
        self.pressed = True #sets a variable
        self.color = "red"
        
     def released(self, event):
        self.pressed = False
        self.color = "light blue"

     def motion(self, event):
          if event.widget == self.game.canvas:
               self.xoffset = 0
               self.yoffset = 0
          elif event.widget == self.game.infoboard.canvas:
               self.xoffset = mapSize
               self.yoffset = 0
          elif event.widget == self.game.towerbox.box:
               self.xoffset = mapSize
               self.yoffset = 174
          elif event.widget == self.game.displayboard.canvas:
               self.yoffset = mapSize
               self.xoffset = 0
          self.x = event.x +self.xoffset#sets the "Mouse" x to the real mouse's x
          self.y = event.y +self.yoffset#sets the "Mouse" y to the real mouse's y
          if self.x < 0: self.x = 0
          if self.y < 0: self.y = 0
          self.gridx = int((self.x-(self.x%blockSize))/blockSize)
          self.gridy = int((self.y-(self.y%blockSize))/blockSize)

     def update(self):
          if self.gridx >= 0 and self.gridx <= gridSize-1 and self.gridy >= 0 and self.gridy <= gridSize-1:
               blockGrid[self.gridx][self.gridy].hoveredOver(self.pressed, self.game)
          else:
               self.game.displayboard.saveMapButton.checkPress(self.pressed, self.x-self.xoffset, self.y-self.yoffset)
     def paint(self, canvas):
          if self.gridx >= 0 and self.gridx <= gridSize-1 and self.gridy >= 0 and self.gridy <= gridSize-1:
               if blockGrid[self.gridx][self.gridy].canPlace:
                    canvas.create_rectangle(self.gridx*blockSize, self.gridy*blockSize, self.gridx*blockSize + blockSize-1, self.gridy*blockSize + blockSize-1, fill = self.color) #draws a rectangle where the pointer is
               else:
                    canvas.create_rectangle(self.gridx*blockSize, self.gridy*blockSize, self.gridx*blockSize + blockSize-1, self.gridy*blockSize + blockSize-1, fill = "black") #draws a rectangle where the pointer is
class Images():
     def __init__(self):
          pass
     
class Block(object):
     def __init__(self, x, y, blockNumber,gridx,gridy): #when i define a "Block", this is what happens
          self.x = x #sets Block x to the given 'x'
          self.y = y #sets Block y to the given 'y'
          self.canPlace = True
          self.blockNumber = blockNumber
          self.gridx = gridx
          self.gridy = gridy
          self.image = None
          self.axis = blockSize/2

     def hoveredOver(self,click,game):
          if click == True:
               global blockGrid
               if selectedTower != "<None>":
                    self.towerType = globals()[blockPlaceDictionary[selectedTower]]
                    blockGrid[self.gridx][self.gridy] = self.towerType(self.x,self.y,blockNumberDictionary[selectedTower],self.gridx,self.gridy)

                    game.changeImage = Image.open("images/mapImages/changeImage.png")
                    blockGrid[self.gridx][self.gridy].paint(game.changeImage)
                    game.changeImage.save("images/mapImages/changeImage.png")
                    game.changeImage = ImageTk.PhotoImage(game.changeImage)

     def update(self):
          pass

     def paint(self, draw):
          self.image = Image.open("images/blockImages/"+ self.__class__.__name__+".png")
          self.offset = (int(self.x - self.axis),int(self.y - self.axis))
          draw.paste(self.image, self.offset)
          self.image = None


class NormalBlock(Block):
     def __init__(self,x,y,blockNumber,gridx,gridy):
          super(NormalBlock,self).__init__(x,y,blockNumber,gridx,gridy)

class PathBlock(Block):
     def __init__(self,x,y,blockNumber,gridx,gridy):
          super(PathBlock,self).__init__(x,y,blockNumber,gridx,gridy)
          self.canPlace = False         

class WaterBlock(Block):
     def __init__(self,x,y,blockNumber,gridx,gridy):
          super(WaterBlock,self).__init__(x,y,blockNumber,gridx,gridy)
          self.canPlace = False 
                                  
game=Game() #start the application at Class Game()



