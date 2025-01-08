use std::time::Instant;

fn is_prime(n: u32) -> bool {
    if n < 2 {
        return false;
    }
    let sqrt_n = (n as f64).sqrt() as u32;
    for i in 2..=sqrt_n {
        if n % i == 0 {
            return false;
        }
    }
    true
}

fn count_primes(limit: u32) -> u32 {
    let mut count = 0;
    for n in 2..=limit {
        if is_prime(n) {
            count += 1;
        }
    }
    count
}

fn main() {
    let n: u32 = 1_000_000; // Define a large number
    let start = Instant::now();
    let result = count_primes(n);
    let elapsed = start.elapsed();
    println!("Number of primes: {}", result);
    println!("Execution time (Rust): {:.4} seconds", elapsed.as_secs_f64());
}
