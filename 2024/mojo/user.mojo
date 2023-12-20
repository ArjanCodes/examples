trait Emailable:
    fn get_email(self) -> String:
        ...
        
    fn send_email(self, email: String):
        ...

@value
struct User(Stringable,  Emailable, CollectionElement):
    var username: String # variables must be declared with var in structs.
    var email: String
    
    fn __init__(
            inout self, # mutable, returns ownership
            owned username: String, # takes ownership
            borrowed email: String, # takes ownership
        ):
        self.username = username
        self.email = email
        
    fn __str__(self) -> String:
        return self.username + " " + self.email
    
    fn get_email(self) -> String:
        return self.email
        
    fn send_email(self, email: String):
        print("Sending email to " + self.email + ": " + email)
        
fn main():
    var users = DynamicVector[User]()
    users.append(User("John", 0))
    users.append(User("Jane", 1))
    users.append(User("Jack", 2))
    
    for i in range(len(users)):
        print(users[i])
    
    