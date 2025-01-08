package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Custom error for invalid content
var ErrInvalidContent = errors.New("file contains invalid content")

// Function to read a file and parse integers
func readAndSumIntegers(filePath string) (int, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return 0, fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	sum := 0
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		num, err := strconv.Atoi(line)
		if err != nil {
			return 0, fmt.Errorf("%w: '%s'", ErrInvalidContent, line)
		}
		sum += num
	}

	if err := scanner.Err(); err != nil {
		return 0, fmt.Errorf("error reading file: %w", err)
	}

	return sum, nil
}

func main() {
	filePath := "numbers.txt"

	// Call the function and handle errors
	sum, err := readAndSumIntegers(filePath)
	if err != nil {
		if errors.Is(err, ErrInvalidContent) {
			fmt.Printf("Content error: %v\\n", err)
		} else {
			fmt.Printf("General error: %v\\n", err)
		}
		return
	}

	fmt.Printf("Sum of integers: %d\\n", sum)
}
