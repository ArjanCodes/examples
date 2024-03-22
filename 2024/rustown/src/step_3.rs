mod main;

fn same_lifetime<'a>(s: &'a str, start: usize, end: usize) -> &'a str {
    &s[start..end]
}

fn equal_lifetimes<'a, 'b: 'a>(x: &'a str, y: &'b str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let s1 = String::from("hello, world!");
    let s2 = same_lifetime(s1.as_str(), 0, 5);
    let result = equal_lifetimes(s1.as_str(), s2);
    println!("The longest string is {}", result);
}
