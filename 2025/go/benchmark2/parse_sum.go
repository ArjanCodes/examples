package main

import (
	"encoding/binary"
	"fmt"
	"os"
	"time"
)

func parseAndSum(filePath string) (int64, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return 0, err
	}
	defer file.Close()

	var buffer []byte
	stat, err := file.Stat()
	if err != nil {
		return 0, err
	}
	buffer = make([]byte, stat.Size())

	_, err = file.Read(buffer)
	if err != nil {
		return 0, err
	}

	var sum int64
	for i := 0; i < len(buffer); i += 4 {
		// Convert 4 bytes to a little-endian 32-bit integer
		num := int32(binary.LittleEndian.Uint32(buffer[i : i+4]))
		sum += int64(num)
	}

	return sum, nil
}

func main() {
	filePath := "data.bin" // File path for the large binary file
	start := time.Now()

	result, err := parseAndSum(filePath)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	elapsed := time.Since(start)
	fmt.Printf("Sum of integers: %d\n", result)
	fmt.Printf("Execution time (Go): %.4f seconds\n", elapsed.Seconds())
}
