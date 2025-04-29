import types

# Dynamically create a class with a __call__ method
DynamicFunction = types.new_class(
    "DynamicFunction",
    (),
    {},
    exec_body=lambda ns: ns.update({"__call__": lambda self, x: x * 2}),
)
double = DynamicFunction()
print(double(5))  # 10
