struct User {
    name: String,
    email: String
}
impl User {
    fn new(name: &str) -> User {
        User {
            name: name.to_string(),
            email: format!("{}@arjancodes.com", name)
        }
    }
}
fn main() {
    let user = User::new("Arjan");
    println!("Hello, {}!", user.name);
    println!("Your email is: {}", user.email);
}