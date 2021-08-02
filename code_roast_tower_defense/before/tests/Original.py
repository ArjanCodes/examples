#IMPORTANT INFORMATION: the use of 'self' ALWAYS refers to the class that it is in. EVERY FUNCTION INSIDE OF A CLASS MUST DECLARE SELF! ex: 'def exampleFunction(self, input1, input2):

from Tkinter import * #imports the tkinter database, allowing the use of it in the program
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
towerDictionary = {"Arrow Shooter":"ArrowShooterTower", "Bullet Shooter":"BulletShooterTower", "Tack Tower": "TackTower"}
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

          self.wavegenerator = Wavegenerator(self)

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
         for i in range(len(projectiles)):
             try:
                 projectiles[i].update()
             except:
                 pass
         for y in range(gridSize):
             for x in range(gridSize):
                 blockGrid[x][y].update() #updates each block one by one by going to its 'def update():' command
         for i in range(len(monsters)):
             try:
                 monsters[i].update()
             except:
                 pass
         for y in range(gridSize):
             for x in range(gridSize):
                 if towerGrid[x][y]:
                    towerGrid[x][y].update() #updates each tower one by one by going to its 'def update():' command             
         self.wavegenerator.update()
         self.displayboard.update()
          
     def paint(self):
          self.canvas.delete(ALL) #clear the screen
          self.gameMap.paint(self.canvas)
          self.mouse.paint(self.canvas) #draw the mouse dot by going to its 'def paint(canvas):' command
          for y in range(gridSize):
              for x in range(gridSize):
                   if towerGrid[x][y]:
                        towerGrid[x][y].paint(self.canvas)
          for i in range(len(monsters)):
               monsters[i].paint(self.canvas)
          for i in range(len(projectiles)):
              projectiles[i].paint(self.canvas)
          self.displayboard.paint()

class Map():
    def __init__(self):
        self.image = None
        self.loadMap("secondMap")
    def loadMap(self,mapName):
        self.drawnMap = Image.new("RGBA", (mapSize, mapSize), (255,255,255,255))
        self.mapFile = open("texts/mapTexts/"+mapName+".txt","r")
        self.gridValues = map(int, (self.mapFile.read()).split())
        for y in range(gridSize):
              for x in range(gridSize):
                   global blockGrid
                   self.blockNumber = self.gridValues[gridSize*y + x]
                   self.blockType = globals()[blockDictionary[self.blockNumber]]
                   blockGrid[x][y] = self.blockType(x*blockSize,y*blockSize,self.blockNumber,x,y) #creates a grid of Blocks
                   blockGrid[x][y].paint(self.drawnMap)
        self.drawnMap.save("images/mapImages/"+mapName+".png")
        self.image = Image.open("images/mapImages/"+mapName+".png")
        self.image = ImageTk.PhotoImage(self.image) 
          
    def saveMap(self):
        self.mapFile = open("firstMap.txt","w")
        for y in range(gridSize):
              for x in range(gridSize):
                  self.mapFile.write(blockGrid[x][y].blockType + " ")
        self.mapFile.close()

    def paint(self, canvas):
         canvas.create_image(0,0, image = self.image, anchor = NW)


class Wavegenerator():
     def __init__(self,game):
          self.game = game
          self.done = False
          self.spawnx = None
          self.spawny = None
          self.currentWave = []
          self.currentMonster = 0
          self.findSpawn()
          self.ticks = 14
          self.maxTicks = 15
          self.waveFile = open("texts/waveTexts/WaveGenerator.txt","r")

     def getWave(self):
          self.game.displayboard.nextWaveButton.canPress = False
          self.currentMonster = 0
          self.waveLine = self.waveFile.readline()
          if len(self.waveLine) == 0:
               self.done = True
          self.currentWave = self.waveLine.split()
          self.currentWave = map(int, self.currentWave)

     def findSpawn(self):
          for x in range(gridSize):
               if isinstance(blockGrid[x][0], PathBlock):
                    self.spawnx = x
                    self.spawny = 0
                    return
          for y in range(gridSize):
               if isinstance(blockGrid[0][y], PathBlock):
                    self.spawnx = 0
                    self.spawny = y
                    return

     def spawnMonster(self):
          self.monsterType = globals()[monsterDictionary[self.currentWave[self.currentMonster]]]
          monsters.append(self.monsterType(self.spawnx*blockSize,self.spawny*blockSize,"None"))
          self.currentMonster = self.currentMonster + 1

     def update(self):
          if self.done == False:
               if self.currentMonster == len(self.currentWave):
                    self.game.displayboard.nextWaveButton.canPress = True
               else:
                    self.ticks = self.ticks+1
                    if self.ticks == self.maxTicks:
                         self.ticks = 0
                         self.spawnMonster()

class NextWaveButton:
     def __init__(self,game):
          self.game = game
          self.x = 450
          self.y = 25
          self.xTwo = 550
          self.yTwo = 50
          self.canPress = True

     def checkPress(self, click, x, y):
          if x >=self.x and y >= self.y and x <= self.xTwo and y <= self.yTwo:
                if self.canPress and click and len(monsters) == 0:
                     self.game.wavegenerator.getWave()

     def paint(self, canvas):
          if self.canPress and len(monsters) == 0:
               self.color = "blue"
          else:
               self.color = "red"
          canvas.create_rectangle(self.x, self.y, self.xTwo, self.yTwo, fill=self.color, outline = self.color) #draws a rectangle where the pointer is
          canvas.create_text(500,37,text = "Next Wave")
          
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
          self.healthbar = Healthbar()
          self.moneybar = Moneybar()
          self.nextWaveButton = NextWaveButton(game)
          self.paint()
    def update(self):
        self.healthbar.update()
        self.moneybar.update()
    
    def paint(self):         
          self.canvas.delete(ALL) #clear the screen
          self.healthbar.paint(self.canvas)
          self.moneybar.paint(self.canvas)
          self.nextWaveButton.paint(self.canvas)
               

class Towerbox:
     def __init__(self, game):
          self.game = game
          self.box = Listbox(master =game.frame, selectmode = "SINGLE", font = ("times",20), height = 21, width = 16, bg = "gray", fg = "dark blue", bd = 1, highlightthickness = 0)
          self.box.insert(END, "<None>")
          for i in towerDictionary.iterkeys():
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
          self.gridx = (self.x-(self.x%blockSize))/blockSize
          self.gridy = (self.y-(self.y%blockSize))/blockSize

     def update(self):
          if self.gridx >= 0 and self.gridx <= gridSize-1 and self.gridy >= 0 and self.gridy <= gridSize-1:
               blockGrid[self.gridx][self.gridy].hoveredOver(self.pressed, self.game)
          else:
               self.game.displayboard.nextWaveButton.checkPress(self.pressed, self.x-self.xoffset, self.y-self.yoffset)
     def paint(self, canvas):
          if self.gridx >= 0 and self.gridx <= gridSize-1 and self.gridy >= 0 and self.gridy <= gridSize-1:
               if blockGrid[self.gridx][self.gridy].canPlace:
                    canvas.create_rectangle(self.gridx*blockSize, self.gridy*blockSize, self.gridx*blockSize + blockSize-1, self.gridy*blockSize + blockSize-1, fill = self.color) #draws a rectangle where the pointer is
               else:
                    canvas.create_rectangle(self.gridx*blockSize, self.gridy*blockSize, self.gridx*blockSize + blockSize-1, self.gridy*blockSize + blockSize-1, fill = "black") #draws a rectangle where the pointer is
class Images():
     def __init__(self):
          pass
     
class Healthbar():
     def __init__(self):
          self.text = str(health)
     
     def update(self):
        self.text = str(health)
     
     def paint(self, canvas):
          canvas.create_text(40, 40, text="Health: " + self.text,fill="black")
     

class Moneybar():
     def __init__(self):
          self.text = str(money)
     
     def update(self):
        self.text = str(money)
     
     def paint(self, canvas):
          canvas.create_text(240, 40, text="Money: " + self.text,fill="black")

class Projectile(object):
     def __init__(self,x,y,damage,speed):
        self.hit = False
        self.x = x
        self.y = y
        self.speed = blockSize/2
        self.damage = damage
        self.speed = speed
        #self.image = Image.open("images/projectileImages/"+self.__class__.__name__+ ".png")
        #self.image = ImageTk.PhotoImage(self.image) 

     def update(self):
          try:
             if target.alive == False:
                  projectiles.remove(self)
                  return
          except:
               if self.hit:
                  self.gotMonster()
               self.move()
               self.checkHit()

     def gotMonster(self):
        self.target.health -= self.damage
        projectiles.remove(self) 
        
     def paint(self,canvas):
         canvas.create_image(self.x,self.y,image = self.image)
     

class TrackingBullet(Projectile):
    def __init__(self,x,y,damage,speed,target):
          super(TrackingBullet,self).__init__(x,y, damage,speed)
          self.target = target
          self.image = Image.open("images/projectileImages/bullet.png")
          self.image = ImageTk.PhotoImage(self.image) 
        
    def move(self):
        self.length = ((self.x-(self.target.x+blockSize/2))**2 + (self.y-(self.target.y+blockSize/2))**2)**0.5
        self.x += self.speed*((self.target.x+blockSize/2)-self.x)/self.length
        self.y += self.speed*((self.target.y+blockSize/2)-self.y)/self.length
        
    def checkHit(self):
        if self.speed**2 > (self.x-(self.target.x+blockSize/2))**2 + (self.y-(self.target.y+blockSize/2))**2:
            self.hit = True
        
class AngledProjectile(Projectile):
     def __init__(self,x,y,damage,speed,angle,givenRange):
          super(AngledProjectile,self).__init__(x,y,damage,speed)
          self.xChange = speed*math.cos(angle)
          self.yChange = speed*math.sin(-angle)
          self.range = givenRange
          self.image = Image.open("images/projectileImages/arrow.png")
          self.image = ImageTk.PhotoImage(self.image.rotate(math.degrees(angle)))
          self.target = None
          self.speed = speed
          self.distance = 0

     def checkHit(self):
          for i in range(len(monsters)):
               if (monsters[i].x-self.x)**2+(monsters[i].y-self.y)**2 <= (blockSize)**2:
                    self.hit = True
                    self.target = monsters[i]
                    return

     def move(self):
          self.x += self.xChange
          self.y += self.yChange
          self.distance += self.speed
          if self.distance >= self.range:
               projectiles.remove(self)
          
         
class Tower(object):
     def __init__(self,x,y,gridx,gridy):
          self.range = 0
          self.clicked = False
          self.x = x
          self.y = y
          self.xTwo = x + blockSize-1
          self.yTwo = y + blockSize-1
          self.gridx = gridx
          self.gridy = gridy
          self.image = None
          self.infotext = "Tower"
          self.image = Image.open("images/towerImages/"+self.__class__.__name__+ ".png")
          self.image = ImageTk.PhotoImage(self.image) 

     def display(self, infoboard):
          print self

     def update(self):
          pass

     def paint(self, canvas):
          canvas.create_image(self.x,self.y, image = self.image, anchor = NW)
          if self.clicked:
              canvas.create_oval(self.x-self.range,self.y-self.range,self.xTwo + self.range,self.yTwo + self.range,fill=None, outline = "black")
              self.clicked = False

class ShootingTower(Tower):
     def __init__(self,x,y,gridx,gridy):
        super(ShootingTower,self).__init__(x,y,gridx,gridy)
        self.bulletsPerSecond = None
        self.ticks = 0
        self.damage = 0
        self.speed = None

     def update(self):
          self.prepareShot()
              
class TargetingTower(ShootingTower):
    def __init__(self,x,y,gridx,gridy):
        super(TargetingTower,self).__init__(x,y,gridx,gridy)
        self.target = None
    
    def prepareShot(self):
          if self.target:
              if self.target.alive and self.range+blockSize >= ((self.x-self.target.x)**2 + (self.y-self.target.y)**2)**0.5:
                  self.ticks += 1
                  if self.ticks == 20/self.bulletsPerSecond:
                      self.shoot()
                      self.ticks = 0
              else:
                  self.target = None
          else:
              for i in range(len(monsters)):
                  if (self.range+blockSize)**2 >= (self.x-monsters[i].x)**2 + (self.y-monsters[i].y)**2:
                      self.target = monsters[i]
        

class ArrowShooterTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super(ArrowShooterTower,self).__init__(x,y,gridx,gridy)
          self.infotext = "ArrowShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = blockSize*5
          self.bulletsPerSecond = 5
          self.damage = 10
          self.speed = blockSize
          
     def shoot(self):
        self.angle = math.atan2(self.y- self.target.y,self.target.x-self.x)
        projectiles.append(AngledProjectile(self.x +blockSize/2, self.y+blockSize/2, self.damage, self.speed, self.angle,self.range))
 
          
class BulletShooterTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super(BulletShooterTower,self).__init__(x,y,gridx,gridy)
          self.infotext = "BulletShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = blockSize*6
          self.bulletsPerSecond = 2
          self.damage = 5
          self.speed = blockSize/2

     def shoot(self):
          projectiles.append(TrackingBullet(self.x +blockSize/2, self.y+blockSize/2, self.damage, self.speed, self.target))
 
class TackTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super(TackTower,self).__init__(x,y,gridx,gridy)
          self.infotext = "TackTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = blockSize*5
          self.bulletsPerSecond = .5
          self.damage = 10
          self.speed = blockSize
          
     def shoot(self):
          for i in range(8):
             self.angle = math.radians(i*45)
             projectiles.append(AngledProjectile(self.x +blockSize/2, self.y+blockSize/2, self.damage, self.speed, self.angle,self.range))
 
     
class Monster(object):
     def __init__(self,x,y,direction):
          self.alive = True
          self.image = None
          self.direction = direction
          self.x = x +0.0
          self.y = y +0.0
          self.health = 0
          self.maxHealth = 0
          self.speed = 0.0
          self.tick = blockSize + 0.0
          self.maxTick = blockSize +0.0
          self.distanceTravelled = 0
          self.armor = 0
          self.magicresist = 0
          self.value = 0
          self.image = Image.open("images/monsterImages/"+self.__class__.__name__+ ".png")
          self.image = ImageTk.PhotoImage(self.image) 

     def update(self):
          if self.health <= 0:
              self.killed()
          if self.tick == self.maxTick:
               self.decidemove()
               self.tick = 0
          self.move()
          self.tick += self.speed

     def move(self):
          if self.direction == "Right":
               self.x += self.speed
          if self.direction == "Left":
               self.x -= self.speed
          if self.direction == "Down":
               self.y += self.speed
          if self.direction == "Up":
               self.y -= self.speed
          self.distanceTravelled += self.speed

     def decidemove(self):
          self.possibleDirections = []
          if int(self.x)%20 != 0:
               self.x = int(self.x)+1
          if int(self.y)%20 != 0:
               self.y = int(self.y)+1
               
          self.gridx = int(self.x/float(blockSize))
          self.gridy = int(self.y/float(blockSize))
          if self.direction != "Left" and self.gridx < gridSize-1 and self.gridy >= 0 and self.gridy <= gridSize-1:
               if isinstance(blockGrid[self.gridx+1][self.gridy], PathBlock):
                    self.possibleDirections.append("Right")
          if self.direction != "Right" and self.gridx > 0 and self.gridy >= 0 and self.gridy <= gridSize-1:
               if isinstance(blockGrid[self.gridx-1][self.gridy], PathBlock):
                    self.possibleDirections.append("Left")
          if self.direction != "Up" and self.gridy < gridSize-1 and self.gridx >= 0 and self.gridx <= gridSize-1:
               if isinstance(blockGrid[self.gridx][self.gridy+1], PathBlock):
                    self.possibleDirections.append("Down")
          if self.direction != "Down" and self.gridy > 0 and self.gridx >= 0 and self.gridx <= gridSize-1:
               if isinstance(blockGrid[self.gridx][self.gridy-1], PathBlock):
                    self.possibleDirections.append("Up")
          try:
               self.direction = self.possibleDirections[random.randrange(0,len(self.possibleDirections))]
          except:
              self.gotThrough()

     def killed(self):
          global money
          money += self.value
          self.die()

     def gotThrough(self):
          global health
          health -= 1
          self.die()
              
     def die(self):
          self.alive = False
          monsters.remove(self)

     def paint(self,canvas):
          canvas.create_rectangle(self.x, self.y-blockSize/4, self.x+blockSize-1, self.y-1, fill="red", outline = "black") 
          canvas.create_rectangle(self.x+1, self.y-blockSize/4 +1, self.x+(blockSize-2)*self.health/self.maxHealth, self.y-2, fill="green", outline = "green")
          canvas.create_image(self.x,self.y, image = self.image, anchor = NW)
 


class Monster1(Monster):
     def __init__(self,x,y,direction):
          super(Monster1,self).__init__(x,y,direction)
          self.maxHealth = 30
          self.health = self.maxHealth
          self.value = 5
          self.speed = float(blockSize)/3
          
class Monster2(Monster):
     def __init__(self,x,y,direction):
          super(Monster2,self).__init__(x,y,direction)
          self.maxHealth = 40
          self.health = self.maxHealth
          self.value = 10
          self.speed = float(blockSize)/6

class Block(object):
     def __init__(self, x, y, blockNumber,gridx,gridy): #when i define a "Block", this is what happens
          self.x = x #sets Block x to the given 'x'
          self.y = y #sets Block y to the given 'y'
          self.canPlace = True
          self.blockNumber = blockNumber
          self.gridx = gridx
          self.gridy = gridy
          self.image = None

     def hoveredOver(self,click,game):
          if click == True:
               global towerGrid
               if towerGrid[self.gridx][self.gridy]:
                    if selectedTower == "<None>":
                        towerGrid[self.gridx][self.gridy].clicked = True
                        game.infoboard.displaySpecific(towerGrid[self.gridx][self.gridy])
               elif selectedTower != "<None>" and self.canPlace == True:
                    self.towerType = globals()[towerDictionary[selectedTower]]
                    towerGrid[self.gridx][self.gridy] = self.towerType(self.x,self.y,self.gridx,self.gridy)
                    

     def update(self):
          pass

     def paint(self, draw):
          self.image = Image.open("images/blockImages/"+ self.__class__.__name__+".png")
          self.offset = (self.x,self.y)
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



