from python import Python as py
from python import Dictionary as dict

fn imports(names: DynamicVector[StringRef]) raises -> dict:
    let imports: dict = py.dict()
    
    for i in range(len(names)):
        imports[names[i]] = py.import_module(names[i])
    
    return imports

def main():
    import_names = DynamicVector[StringRef]()
    import_names.append("builtins")
    import_names.append("math")
    imported = imports(import_names)
    user_num = imported["builtins"].input("Enter a number: ")
    user_num = imported["builtins"].int(user_num)
    user_num = imported["math"].sqrt(user_num)
    imported["builtins"].print("The square root of your number is: " + str(user_num))
    
# fn main():
#     var import_names = DynamicVector[StringRef]()
#     import_names.append("builtins")
#     import_names.append("math")
#     try:
#         let imported = imports(import_names) 
#     except:
#         print("Error importing modules")
#         return
#     try:
#         let user_num = imported["builtins"].input("Enter a number: ")
#         let user_num = imported["builtins"].int(user_num)
#         let user_num = imported["math"].sqrt(user_num)
#         imported["builtins"].print("The square root of your number is: " + str(user_num))
#     except:
#         print("Error executing program")
#         return
            
    