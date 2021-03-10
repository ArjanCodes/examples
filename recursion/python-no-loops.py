# TRADITIONAL WHILE LOOP

val = input("Do you want to format your harddrive (y/n)? ")
while val != "y" and val != "n":
    val = input("Please answer yes or no. Do you want to format your harddrive (y/n)? ")

# List printing

lst = ["Arjan", "Codes", "Please", "Subscribe"]

# WHILE LOOP
i = 0
while i < len(lst):
    print(lst[i].upper())
    i += 1

# FOR LOOP
for item in lst:
    print(item.upper()) 

# MAP
list(map(print, lst))
list(map(lambda i: print(i.upper()), lst))

# LIST COMPREHENSION
lst2 = [item.upper() for item in lst]
print(lst2)


# RECURSION
while <condition>:
  do something

def loop():
  if <condition>:
      do something
      loop()
loop()

i = 0
def loop():
    global i
    if i < len(lst):
        print(lst[i].upper())
        i += 1
        loop()

# loop()

for item in lst:
    for element in item: 
        print(element, end=' ') 

i = j = 0
def loop():
    global i, j
    if i < len(lst):
        j = 0
        def inner_loop():
            global i, j
            if j < len(lst[i]):
                print(lst[i][j], end=' ')
                j += 1
                inner_loop()
        inner_loop()
        i += 1
        loop()

loop()


# Haskell
'''
import Data.Char

printElements (x:xs) = do
    let bigX = map toUpper x 
    print bigX
    printElements xs
printElements ([]) = return ()

main = printElements ["Arjan", "Codes", "Please", "Subscribe"]
'''