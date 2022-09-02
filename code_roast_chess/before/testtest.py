from pieces import *
from copy import deepcopy



boardWithObjects = [[Empty(), Empty()], 1]

boardDeepCopy = deepcopy(boardWithObjects)
boardNormalCopy = boardWithObjects.copy()



print(f"normal[0] is original[0]: {boardNormalCopy[0] is boardWithObjects[0]}")
print(f"normal[1] is original[1]: {boardNormalCopy[1] is boardWithObjects[1]}")
print(f"deep[0] is original[0]: {boardDeepCopy[0] is boardWithObjects[0]}")
print(f"deep[1] is original[1]: {boardDeepCopy[1] is boardWithObjects[1]}")

boardWithObjects[0][0] = 4
boardWithObjects[1] = 5
print("")

print(f"normal[0] is original[0]: {boardNormalCopy[0] is boardWithObjects[0]}")
print(f"normal[1] is original[1]: {boardNormalCopy[1] is boardWithObjects[1]}")
print(f"deep[0] is original[0]: {boardDeepCopy[0] is boardWithObjects[0]}")
print(f"deep[1] is original[1]: {boardDeepCopy[1] is boardWithObjects[1]}")
#print(f"deep copy = {boardDeepCopy}")
#print(f"shallow copy = {boardNormalCopy}")