use std::fs::File;
use std::io::{self, Read};

fn read_file_contents(path: &str) -> Result<String, io::Error> {
    let mut file = match File::open(path) {
        Ok(file) => file, // On success, we can return the result
        Err(e) => return Err(e), // On error, we return the error
    };
    let mut contents = String::new();
    match file.read_to_string(&mut contents) {
        Ok(_) => Ok(contents), // If successful, return the contents.
        Err(e) => Err(e),  // If an error occurs, return the error.
    }
}
fn read_file_contents_short(path: &str) -> Result<String, io::Error> {
    // this version is shorter, by making use of the ? operator, this is the equivalent of the match statement above
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

fn read_file_if_exists(path: &str) -> Option<String> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Some(contents)
}

fn file_example_match(path: &str) {
    match read_file_contents(path) {
        Ok(contents) => println!("File contents: {}", contents),
        Err(e) => println!("Error reading file: {:?}", e),
    }
}

fn file_example_unwrap(path: &str) {
    let contents = read_file_contents_short(path).unwrap();
    println!("File contents with unwrap: {}", contents);
}
fn file_example_expect(path: &str) {
    let contents = read_file_contents_short(path).expect("Failed to read file");
    println!("File contents with expect: {}", contents);
}

fn panic_example() {
    panic!("Something unrecoverable has happened");
}

fn main() {
    let path = "hello.txt";

    // file_example_match(path);
    // read_file_if_exists(path);
    // panic_example();
    // file_example_unwrap(path);
    // file_example_expect(path);
}

