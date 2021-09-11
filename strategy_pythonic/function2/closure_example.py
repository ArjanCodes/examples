def a(x: int = 1):
    def b():
        return x

    return b


b = a()
print(b())
# 1
b.__closure__[0].cell_contents = 2
print(b())
# 2
del b.__closure__[0].cell_contents
print(b())
# NameError: free variable 'x' referenced before assignment in enclosing scope
