import time

def fibonacci_recursion(n):
   if n == 1 or n == 2:
       return 1
   else:
       return fibonacci_recursion(n-1) + fibonacci_recursion(n-2)

def fibonacci_for(n):
    a = 1
    b = 1
    for _ in range(1, n):
        new = a + b
        a = b
        b = new
    return a

# store time for measuring performance
t = time.process_time()

# compute the 40th fibonacci number
f = fibonacci_for(40)

# print out the time
print(time.process_time() - t)