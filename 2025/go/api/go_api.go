package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// Response struct to define the JSON response format
type Response struct {
	Message string `json:"message"`
}

// HelloHandler handles the /hello endpoint
func HelloHandler(w http.ResponseWriter, r *http.Request) {
	// Get the 'name' query parameter
	name := r.URL.Query().Get("name")
	if name == "" {
		name = "World" // Default to "World" if no name is provided
	}

	// Create the response
	response := Response{Message: fmt.Sprintf("Hello, %s!", name)}

	// Set content type to JSON and write the response
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	// Register the handler function to the /hello route
	http.HandleFunc("/hello", HelloHandler)

	// Start the HTTP server
	fmt.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Server failed to start:", err)
	}
}
