struct User {
    name: &'static str,
    email: &'static str,
}

impl User {
    fn new(name: &'static str) -> User {
        User {
            name,
            email: &format!("{}@arjancodes.com", name),
    }
}

fn main() {
    let user = User::new("Arjan");
    println!("Hello, {}!", user.name);
    println!("Your email is: {}", user.email);
}
