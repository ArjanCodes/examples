package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"time"

	analyticspb "encoding-service/pkg/grpc/generated/pbAnalytics" // Import generated analytics protobuf package
	pb "encoding-service/pkg/grpc/generated/pbEncoding"           // Import generated encoding protobuf package

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
)

type server struct {
	pb.UnimplementedEncodingServiceServer
	analyticsClient analyticspb.AnalyticsServiceClient // gRPC client for the analytics service
}

// gRPC method to handle video upload
func (s *server) UploadVideo(ctx context.Context, req *pb.UploadVideoRequest) (*pb.UploadVideoResponse, error) {
	videoName := req.GetVideoName()

	// Extracting metadata (if any)
	md, ok := metadata.FromIncomingContext(ctx)
	if ok {
		log.Printf("Received metadata: %v", md)
	}

	// Simulating processing time
	time.Sleep(2 * time.Second) // Simulate video processing delay
	log.Println("Processing complete.")

	// Call the analytics service to log or update the video view count
	err := s.logAnalytics(ctx, videoName)
	if err != nil {
		log.Printf("Failed to log analytics for video %s: %v", videoName, err)
	}

	// Return mock URL after "processing"
	videoURL := fmt.Sprintf("/videos/%s", videoName)
	log.Printf("Returning UploadVideo response: videoUrl=%s", videoURL)

	return &pb.UploadVideoResponse{
		VideoUrl: videoURL,
	}, nil
}

// Helper method to call the analytics service
func (s *server) logAnalytics(ctx context.Context, videoName string) error {
	// Create a request to the analytics service
	analyticsReq := &analyticspb.LogViewRequest{
		VideoName: videoName,
	}

	// Call the analytics service and log the view count
	_, err := s.analyticsClient.LogView(ctx, analyticsReq)
	if err != nil {
		return fmt.Errorf("failed to log analytics: %w", err)
	}
	log.Printf("Successfully logged analytics for video: %s", videoName)
	return nil
}

func main() {
	// Start gRPC server for the encoding service
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	// Establish a connection to the analytics service (Python service running on port 50052)
	conn, err := grpc.DialContext(ctx, "localhost:50052", grpc.WithTransportCredentials(insecure.NewCredentials()))

	if err != nil {
		log.Fatalf("Failed to connect to analytics service: %v", err)
	}
	defer conn.Close()

	analyticsClient := analyticspb.NewAnalyticsServiceClient(conn)

	grpcServer := grpc.NewServer()
	pb.RegisterEncodingServiceServer(grpcServer, &server{analyticsClient: analyticsClient})
	log.Printf("Encoding service is listening at %v", lis.Addr())

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
