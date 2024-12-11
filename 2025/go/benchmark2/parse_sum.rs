use std::fs::File;
use std::io::{self, Read};
use std::time::Instant;

fn parse_and_sum(file_path: &str) -> io::Result<i64> {
    let mut file = File::open(file_path)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;

    // Each 4 bytes represents a 32-bit integer
    let mut sum: i64 = 0;
    for chunk in buffer.chunks_exact(4) {
        let num = i32::from_le_bytes([chunk[0], chunk[1], chunk[2], chunk[3]]);
        sum += num as i64;
    }

    Ok(sum)
}

fn main() -> io::Result<()> {
    let file_path = "data.bin"; // File path for the large binary file
    let start = Instant::now();

    let result = parse_and_sum(file_path)?;
    let elapsed = start.elapsed();

    println!("Sum of integers: {}", result);
    println!("Execution time (Rust): {:.4} seconds", elapsed.as_secs_f64());

    Ok(())
}
