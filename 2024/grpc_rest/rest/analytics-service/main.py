import logging
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import uvicorn

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI instance
app = FastAPI()

# SQLAlchemy setup
DATABASE_URL = "sqlite:///analytics.db"
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


# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model for request and response
class LogViewRequest(BaseModel):
    video_name: str


class LogViewResponse(BaseModel):
    success: bool


# Initialize the database on startup
@app.on_event("startup")
def startup_event():
    initialize_database()


# Log view and add video if not already in the database
@app.post("/logview", response_model=LogViewResponse)
def log_view(request: LogViewRequest, db: Session = Depends(get_db)):
    video_name = request.video_name

    # Log the incoming request
    logger.info(f"Received LogView request for video_name (URL): {video_name}")

    # Try to find the video URL in the database
    analytics_entry = db.query(Analytics).filter_by(video_name=video_name).first()

    if analytics_entry:
        logger.info(f"Video URL {video_name} already exists in the database.")
    else:
        # If the video doesn't exist, create a new entry
        new_entry = Analytics(video_name=video_name)
        db.add(new_entry)
        db.commit()
        logger.info(f"Stored new video URL: {video_name}")

    return LogViewResponse(success=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
