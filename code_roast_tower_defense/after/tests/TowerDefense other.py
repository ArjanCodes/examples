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
monsterDictionary = ["Monster1", "Monster2","AlexMonster","BenMonster","MonsterBig"]
towerDictionary = {"Arrow Shooter":"ArrowShooterTower", "Bullet Shooter":"BulletShooterTower", "Tack Tower": "TackTower", "Power Tower": "PowerTower"}
towerCost = {"Arrow Shooter":50,"Bullet Shooter":60,"Tack Tower":70, "Power Tower":70}
towerGrid = [[None for y in range(gridSize)] for x in range(gridSize)]
monsters = []
monstersByHealth = []
monstersByHealthReversed = []
monstersByDistance = []
monstersByDistanceReversed = []
monstersListList = [monstersByHealth,monstersByHealthReversed,monstersByDistance,monstersByDistanceReversed]
projectiles = []
health = 10
money = 250
selectedTower = "<None>"
displayTower = None

class Game(): #the main class that we call "Game"
     def __init__(self): #setting up the window for the game here
          self.root=Tk() #saying this window will use tkinter
          self.root.title("Tower Defense Ultra Mode")
          self.RUN=True #creating a variable RUN. does nothing yet.hu
          self.root.protocol("WM_DELETE_WINDOW", self.end)

          self.frame = Frame(master= self.root)
          self.frame.grid(row = 0, column = 0)

          self.canvas = Canvas(master = self.frame, width=mapSize, height=mapSize, bg = "white", highlightthickness = 0) #actually creates a window and puts our frame on it
          self.canvas.grid(row = 0,column = 0,rowspan = 2, columnspan = 1) #makes the window called "canvas" complete

          self.displayboard = Displayboard(self)
          
          self.infoboard = Infoboard(self)

          self.towerbox = Towerbox(self)

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
         global monstersByHealth
         global monstersByHealthReversed
         global monstersByDistance
         global monstersByDistanceReversed
         global monstersListList
         monstersByHealth = sorted(monsters, key=lambda x: x.health, reverse=True)
         monstersByDistance = sorted(monsters, key=lambda x: x.distanceTravelled, reverse=True)
         monstersByHealthReversed = sorted(monsters, key=lambda x: x.health, reverse=False)
         monstersByDistanceReversed = sorted(monsters, key=lambda x: x.distanceTravelled, reverse=False)
         monstersListList = [monstersByHealth,monstersByHealthReversed,monstersByDistance,monstersByDistanceReversed]
         
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
          if displayTower:
               displayTower.paintSelect(self.canvas)
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
                   blockGrid[x][y] = self.blockType(x*blockSize+blockSize/2,y*blockSize+blockSize/2,self.blockNumber,x,y) #creates a grid of Blocks
                   blockGrid[x][y].paint(self.drawnMap)
        self.drawnMap.save("images/mapImages/"+mapName+".png")
        self.image = Image.open("images/mapImages/"+mapName+".png")
        self.image = ImageTk.PhotoImage(self.image) 
          
    def saveMap(self):
        self.mapFile = open("LeoMap.txt","w")
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
          self.ticks = 1
          self.maxTicks = 2
          self.waveFile = open("texts/waveTexts/WaveGenerator.txt","r")

     def getWave(self):
          self.game.displayboard.nextWaveButton.canPress = False
          self.currentMonster = 1
          self.waveLine = self.waveFile.readline()
          if len(self.waveLine) == 0:
               self.done = True
          else:
               self.currentWave = self.waveLine.split()
               self.currentWave = map(int, self.currentWave)
               self.maxTicks = self.currentWave[0]

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
          monsters.append(self.monsterType(self.spawnx*blockSize + blockSize/2,self.spawny*blockSize + blockSize/2,"None"))
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
          
class MyButton(object):
     def __init__(self, x, y, xTwo, yTwo):
        self.x = x
        self.y = y
        self.xTwo = xTwo
        self.yTwo = yTwo
     
     def checkPress(self, click, x, y):
        if x >=self.x and y >= self.y and x <= self.xTwo and y <= self.yTwo:
             self.pressed()
             return True
        return False

     def pressed(self):
         pass

     def paint(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.xTwo, self.yTwo, fill="red", outline = "black")

class TargetButton(MyButton):
    def __init__(self, x, y, xTwo, yTwo, myType):
        super(TargetButton,self).__init__( x, y, xTwo, yTwo)
        self.type = myType
     
    def pressed(self):
         global displayTower
         displayTower.targetList = self.type

class StickyButton(MyButton):
    def __init__(self, x, y, xTwo, yTwo):
        super(StickyButton,self).__init__(x, y, xTwo, yTwo)
             
    def pressed(self):
         global displayTower
         if displayTower.stickyTarget == False:
             displayTower.stickyTarget = True
         else:
             displayTower.stickyTarget = False

class SellButton(MyButton):
    def __init__(self, x, y, xTwo, yTwo):
        super(SellButton,self).__init__(x, y, xTwo, yTwo)
             
    def pressed(self):
         global displayTower
         displayTower.sold()
         displayTower = None
          
class Infoboard:
     def __init__(self, game):
          self.canvas = Canvas(master = game.frame, width = 162, height = 174, bg = "gray", highlightthickness = 0)
          self.canvas.grid(row = 0, column = 1)
          self.image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
          self.canvas.create_image(0,0 , image = self.image, anchor = NW)
          self.currentButtons = []
     
     def buttonsCheck(self, click, x, y):
          if click:
               for i in range(len(self.currentButtons)):
                     if self.currentButtons[i].checkPress(click, x, y):
                          self.displaySpecific()
                          return
                     
     def displaySpecific(self):
          self.canvas.delete(ALL) #clear the screen
          self.canvas.create_image(0,0, image = self.image, anchor = NW)
          self.currentButtons = []
          if displayTower== None:
               return
          
          self.towerImage = ImageTk.PhotoImage(Image.open("images/towerImages/"+towerDictionary[displayTower.name]+ ".png"))
          self.canvas.create_text(80,75,text = displayTower.name, font = ("times",20))
          self.canvas.create_image(5,5 , image = self.towerImage, anchor = NW)
          
          if issubclass(displayTower.__class__, TargetingTower):
               
              self.currentButtons.append(TargetButton(26,30,35,39,0))
              self.canvas.create_text(37,28,text = "> Health", font = ("times",12), fill = "white", anchor = NW)
                                    
              self.currentButtons.append(TargetButton(26,50,35,59,1))
              self.canvas.create_text(37,48,text = "< Health", font = ("times",12), fill = "white", anchor = NW)
                                                                       
              self.currentButtons.append(TargetButton(92,50,101,59,2))
              self.canvas.create_text(103,48,text = "> Distance", font = ("times",12), fill = "white", anchor = NW)

              self.currentButtons.append(TargetButton(92,30,101,39,3))
              self.canvas.create_text(103,28,text = "< Distance", font = ("times",12), fill = "white", anchor = NW)
 


              self.currentButtons.append(StickyButton(10,40,19,49))
              self.currentButtons.append(SellButton(5,145,78,168))
              self.canvas.create_text(28,146,text = "Sell", font = ("times",22), fill = "light green", anchor = NW)
              
              self.currentButtons[displayTower.targetList].paint(self.canvas)
              if displayTower.stickyTarget == True:
                   self.currentButtons[4].paint(self.canvas)

     def displayGeneric(self):
          self.currentButtons = []
          if selectedTower == "<None>":
               self.text = None
               self.towerImage = None
          else:
               self.text = selectedTower + " cost: " + str(towerCost[selectedTower])
               self.towerImage = ImageTk.PhotoImage(Image.open("images/towerImages/"+towerDictionary[selectedTower]+".png"))
          self.canvas.delete(ALL) #clear the screen
          self.canvas.create_image(0,0, image = self.image, anchor = NW)
          self.canvas.create_text(80,75,text = self.text)
          self.canvas.create_image(5,5 , image = self.towerImage, anchor = NW)
          
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
          global displayTower
          selectedTower = str(self.box.get(self.box.curselection()))
          displayTower = None
          self.game.infoboard.displayGeneric()
class Mouse():
     def __init__(self,game): #when i define a "Mouse", this is what happens
          self.game = game
          self.x = 0
          self.y = 0
          self.gridx = 0
          self.gridy = 0
          self.xoffset = 0
          self.yoffset = 0
          self.pressed = False
          game.root.bind("<Button-1>", self.clicked) #whenever left mouse button is pressed, go to def released(event)
          game.root.bind("<ButtonRelease-1>", self.released) #whenever left mouse button is released, go to def released(event)
          game.root.bind("<Motion>", self.motion) #whenever left mouse button is dragged, go to def released(event)
          self.image = Image.open("images/mouseImages/HoveringCanPress.png")
          self.image = ImageTk.PhotoImage(self.image) 
          self.canNotPressImage = Image.open("images/mouseImages/HoveringCanNotPress.png")
          self.canNotPressImage = ImageTk.PhotoImage(self.canNotPressImage) 
          
     def clicked(self, event):
        self.pressed = True #sets a variable
        self.image = Image.open("images/mouseImages/Pressed.png")
        self.image = ImageTk.PhotoImage(self.image) 
        
     def released(self, event):
        self.pressed = False
        self.image = Image.open("images/mouseImages/HoveringCanPress.png")
        self.image = ImageTk.PhotoImage(self.image) 

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
               self.game.infoboard.buttonsCheck(self.pressed, self.x-self.xoffset, self.y-self.yoffset)
     def paint(self, canvas):
          if self.gridx >= 0 and self.gridx <= gridSize-1 and self.gridy >= 0 and self.gridy <= gridSize-1:
               if blockGrid[self.gridx][self.gridy].canPlace:
                    canvas.create_image(self.gridx*blockSize,self.gridy*blockSize, image = self.image, anchor = NW)
               else:
                    canvas.create_image(self.gridx*blockSize,self.gridy*blockSize, image = self.canNotPressImage, anchor = NW)
     
               
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
        self.length = ((self.x-(self.target.x))**2 + (self.y-(self.target.y))**2)**0.5
        self.x += self.speed*((self.target.x)-self.x)/self.length
        self.y += self.speed*((self.target.y)-self.y)/self.length
        
    def checkHit(self):
        if self.speed**2 > (self.x-(self.target.x))**2 + (self.y-(self.target.y))**2:
            self.hit = True

class PowerShot(TrackingBullet):
    def __init__(self,x,y,damage,speed,target,slow):
         super(PowerShot,self).__init__(x,y, damage,speed,target)
         self.slow = slow
         self.image = Image.open("images/projectileImages/powerShot.png")
         self.image = ImageTk.PhotoImage(self.image)

    def gotMonster(self):
        self.target.health -= self.damage
        self.target.movement = (self.target.speed)/self.slow
        projectiles.remove(self) 
        
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
          self.gridx = gridx
          self.gridy = gridy
          self.image = None
          self.name = None
          self.image = Image.open("images/towerImages/"+self.__class__.__name__+ ".png")
          self.image = ImageTk.PhotoImage(self.image) 

     def update(self):
          pass

     def sold(self):
          towerGrid[self.gridx][self.gridy] = None

     def paintSelect(self,canvas):
          canvas.create_oval(self.x-self.range,self.y-self.range,self.x + self.range,self.y + self.range,fill=None, outline = "white")
 
     def paint(self, canvas):
          canvas.create_image(self.x,self.y, image = self.image, anchor = CENTER)

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
        self.targetList = 0
        self.stickyTarget = False
    
    def prepareShot(self):
          self.checkList = monstersListList[self.targetList]
          if self.ticks != 20/self.bulletsPerSecond:
               self.ticks += 1
          if self.stickyTarget == False:
               for i in range(len(self.checkList)):
                  if (self.range+blockSize)**2 >= (self.x-self.checkList[i].x)**2 + (self.y-self.checkList[i].y)**2:
                      self.target = self.checkList[i]
          if self.target:
              if self.target.alive and self.range+blockSize >= ((self.x-self.target.x)**2 + (self.y-self.target.y)**2)**0.5:
                  if self.ticks >= 20/self.bulletsPerSecond:
                      self.shoot()
                      self.ticks = 0
              else:
                  self.target = None
          elif self.stickyTarget == True:
              for i in range(len(self.checkList)):
                  if (self.range+blockSize)**2 >= (self.x-self.checkList[i].x)**2 + (self.y-self.checkList[i].y)**2:
                      self.target = self.checkList[i]
        

class ArrowShooterTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super(ArrowShooterTower,self).__init__(x,y,gridx,gridy)
          self.name = "Arrow Shooter"
          self.infotext = "ArrowShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = blockSize*10 - blockSize/2
          self.bulletsPerSecond = 1
          self.damage = 10
          self.speed = blockSize
          
     def shoot(self):
        self.angle = math.atan2(self.y- self.target.y,self.target.x-self.x)
        projectiles.append(AngledProjectile(self.x , self.y, self.damage, self.speed, self.angle,self.range+blockSize/2))
          
class BulletShooterTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super(BulletShooterTower,self).__init__(x,y,gridx,gridy)
          self.name = "Bullet Shooter"
          self.infotext = "BulletShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = blockSize*6 - blockSize/2
          self.bulletsPerSecond = 4
          self.damage = 5
          self.speed = blockSize/2

     def shoot(self):
          projectiles.append(TrackingBullet(self.x , self.y, self.damage, self.speed, self.target))

class PowerTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super(PowerTower,self).__init__(x,y,gridx,gridy)
          self.name = "Power Tower"
          self.infotext = "PowerTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = blockSize*8 - blockSize/2
          self.bulletsPerSecond = 10
          self.damage = 1
          self.speed = blockSize
          self.slow = 2

     def shoot(self):
          projectiles.append(PowerShot(self.x , self.y, self.damage, self.speed, self.target,self.slow))
 
class TackTower(TargetingTower):
     def __init__(self,x,y,gridx,gridy):
          super(TackTower,self).__init__(x,y,gridx,gridy)
          self.name = "Tack Tower"
          self.infotext = "TackTower at [" + str(gridx) + "," + str(gridy) + "]."
          self.range = blockSize*5
          self.bulletsPerSecond = .5
          self.damage = 10
          self.speed = blockSize
          
     def shoot(self):
          for i in range(8):
             self.angle = math.radians(i*45)
             projectiles.append(AngledProjectile(self.x , self.y, self.damage, self.speed, self.angle,self.range))
 
     
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
          self.movement = 0.0
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
               self.movement = self.speed
               self.tick = 0
          self.move()
          self.tick += self.movement

     def move(self):
          if self.direction == "Right":
               self.x += self.movement
          if self.direction == "Left":
               self.x -= self.movement
          if self.direction == "Down":
               self.y += self.movement
          if self.direction == "Up":
               self.y -= self.movement
          self.distanceTravelled += self.movement

     def decidemove(self):
          self.possibleDirections = []
          if int(self.x-blockSize/2)%blockSize != 0:
               self.x = int(self.x)+1
          if int(self.y-blockSize/2)%blockSize != 0:
               self.y = int(self.y)+1
               
          self.gridx = int((self.x-blockSize/2)/float(blockSize))
          self.gridy = int((self.y-blockSize/2)/float(blockSize))
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
          canvas.create_rectangle(self.x-self.axis, self.y-3*self.axis/2, self.x+self.axis-1, self.y-self.axis-1, fill="red", outline = "black") 
          canvas.create_rectangle(self.x-self.axis+1, self.y-3*self.axis/2 +1, self.x-self.axis+(self.axis*2-2)*self.health/self.maxHealth, self.y-self.axis-2, fill="green", outline = "green")
          canvas.create_image(self.x,self.y, image = self.image, anchor = CENTER)
 


class Monster1(Monster):
     def __init__(self,x,y,direction):
          super(Monster1,self).__init__(x,y,direction)
          self.maxHealth = 30
          self.health = self.maxHealth
          self.value = 5
          self.speed = float(blockSize)/3
          self.movement = float(blockSize)/3
          self.axis = blockSize/2
          
class Monster2(Monster):
     def __init__(self,x,y,direction):
          super(Monster2,self).__init__(x,y,direction)
          self.maxHealth = 50
          self.health = self.maxHealth
          self.value = 10
          self.speed = float(blockSize)/4
          self.movement = float(blockSize)/4
          self.axis = blockSize/2

class AlexMonster(Monster):
     def __init__(self,x,y,direction):
          super(AlexMonster,self).__init__(x,y,direction)
          self.maxHealth = 500
          self.health = self.maxHealth
          self.value = 100
          self.speed = float(blockSize)/6
          self.movement = float(blockSize)/6
          self.axis = blockSize

class BenMonster(Monster):
     def __init__(self,x,y,direction):
          super(BenMonster,self).__init__(x,y,direction)
          self.maxHealth = 499
          self.health = self.maxHealth
          self.value = 99
          self.speed = float(blockSize)/4
          self.movement = float(blockSize)/4
          self.axis = 2*blockSize
          
class MonsterBig(Monster):
     def __init__(self,x,y,direction):
          super(MonsterBig,self).__init__(x,y,direction)
          self.maxHealth = 1000
          self.health = self.maxHealth
          self.value = 10
          self.speed = float(blockSize)/6
          self.movement = float(blockSize)/6
          self.axis = 3*blockSize/2

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
               global towerGrid
               global money
               if towerGrid[self.gridx][self.gridy]:
                    if selectedTower == "<None>":
                        towerGrid[self.gridx][self.gridy].clicked = True
                        global displayTower
                        displayTower = towerGrid[self.gridx][self.gridy]
                        game.infoboard.displaySpecific()
               elif selectedTower != "<None>" and self.canPlace == True and money >= towerCost[selectedTower]:
                    self.towerType = globals()[towerDictionary[selectedTower]]
                    towerGrid[self.gridx][self.gridy] = self.towerType(self.x,self.y,self.gridx,self.gridy)
                    money -= towerCost[selectedTower]
                    

     def update(self):
          pass

     def paint(self, draw):
          self.image = Image.open("images/blockImages/"+ self.__class__.__name__+".png")
          self.offset = (self.x - self.axis,self.y - self.axis)
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



