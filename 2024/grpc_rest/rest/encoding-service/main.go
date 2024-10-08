package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// VideoUploadRequest is the request struct for video uploads
type VideoUploadRequest struct {
	VideoName string `json:"video_name"`
}

// VideoUploadResponse is the response struct for video uploads
type VideoUploadResponse struct {
	VideoURL string `json:"video_url"`
}

// AnalyticsRequest is the request struct for calling the analytics service
type AnalyticsRequest struct {
	VideoName string `json:"video_name"`
}

// Helper method to call the analytics service
func logAnalytics(ctx context.Context, videoName string) error {
	// Create a request to the analytics service
	analyticsReq := AnalyticsRequest{
		VideoName: videoName,
	}

	// Convert request to JSON
	reqBody, err := json.Marshal(analyticsReq)
	if err != nil {
		return fmt.Errorf("failed to marshal analytics request: %w", err)
	}

	// Send a POST request to the analytics service
	resp, err := http.Post("http://localhost:8000/logview", "application/json", bytes.NewBuffer(reqBody))
	if err != nil {
		return fmt.Errorf("failed to call analytics service: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("failed to log analytics: received status %d", resp.StatusCode)
	}

	log.Printf("Successfully logged analytics for video: %s", videoName)
	return nil
}

// Handler function for video upload (REST endpoint)
func uploadVideo(c *gin.Context) {
	var req VideoUploadRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request body"})
		return
	}

	videoName := req.VideoName

	// Simulate video processing time
	time.Sleep(2 * time.Second)
	log.Println("Processing complete.")

	// Call the analytics service to log the video view count
	if err := logAnalytics(c.Request.Context(), videoName); err != nil {
		log.Printf("Failed to log analytics for video %s: %v", videoName, err)
	}

	// Return mock URL after "processing"
	videoURL := fmt.Sprintf("/videos/%s", videoName)
	log.Printf("Returning uploadVideo response: videoUrl=%s", videoURL)

	resp := VideoUploadResponse{
		VideoURL: videoURL,
	}
	c.JSON(http.StatusOK, resp)
}

func main() {
	// Create a new Gin router
	r := gin.Default()

	// Enable CORS for all origins (you can configure it more specifically if needed)
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000"}, // Frontend URL
		AllowMethods:     []string{"POST", "GET", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		AllowCredentials: true,
	}))

	// Define the /upload endpoint
	r.POST("/upload", uploadVideo)

	// Start the HTTP server
	log.Println("Encoding service is listening on port 8080...")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
