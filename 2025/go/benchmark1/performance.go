package main

import (
	"fmt"
	"math"
	"time"
)

func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	sqrt := int(math.Sqrt(float64(n)))
	for i := 2; i <= sqrt; i++ {
		if n%i == 0 {
			return false
		}
	}
	return true
}

func countPrimes(limit int) int {
	count := 0
	for i := 2; i <= limit; i++ {
		if isPrime(i) {
			count++
		}
	}
	return count
}

func main() {
	n := 1000000 // Define a large number
	start := time.Now()
	result := countPrimes(n)
	elapsed := time.Since(start)
	fmt.Printf("Number of primes: %d\n", result)
	fmt.Printf("Execution time (Go): %.4f seconds\n", elapsed.Seconds())
}
