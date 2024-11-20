import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from concurrent import futures
import grpc
import analytics.analytics_pb2_grpc as analytics_pb2_grpc
import analytics.analytics_pb2 as analytics_pb2

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# SQLAlchemy setup
DATABASE_URL = "sqlite:///analytics.db"  # Define the database URL
Base = declarative_base()


# Define the Analytics table schema using SQLAlchemy ORM
class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_name = Column(String, unique=True, nullable=False)


# Create an SQLite engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Initialize the database schema
def initialize_database():
    Base.metadata.create_all(bind=engine)
    logger.info("SQLite database initialized with SQLAlchemy and tables created.")


class AnalyticsService(analytics_pb2_grpc.AnalyticsServiceServicer):
    def LogView(self, request, context):
        # Log the incoming request
        logger.info(
            f"Received LogView request for video_name (URL): {request.video_name}"
        )

        session = SessionLocal()
        video_name = request.video_name

        # Try to find the video URL in the database
        analytics_entry = (
            session.query(Analytics).filter_by(video_name=video_name).first()
        )

        if analytics_entry:
            logger.info(f"Video URL {video_name} already exists in the database.")
        else:
            # If the video doesn't exist, create a new entry
            new_entry = Analytics(video_name=video_name)
            session.add(new_entry)
            session.commit()
            logger.info(f"Stored new video URL: {video_name}")

        session.close()

        # Return success response
        return analytics_pb2.LogViewResponse(success=True)


def serve():
    # Initialize the SQLite database
    initialize_database()

    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analytics_pb2_grpc.add_AnalyticsServiceServicer_to_server(
        AnalyticsService(), server
    )
    server.add_insecure_port("[::]:50052")
    logger.info("gRPC server is running on port 50052...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
