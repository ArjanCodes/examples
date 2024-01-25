fn hello():
    print("Hello")
    
def world() -> NoneType:
    print("World")
    
fn main():
    hello()
    try:
        world()
    except:
        print("World not found")
    print("from")
    print(add("Arjan", "Codes"))
    
fn add(a: String, b: String) -> String:
    return a + b