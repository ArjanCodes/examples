# while <condition>:
#   do something

# def loop():
#   if <condition>:
#       do something
#       loop()
# loop()

lst = ["Arjan", "Codes", "Please", "Subscribe"]

i = 0
# while i < len(lst):
#     print(lst[i].upper())
#     i += 1

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