from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
import fastapi.testclient


DATABASE_URL = "sqlite:///test.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()


# Models
class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)


Base.metadata.create_all(bind=engine)


class BlogCreate(BaseModel):
    title: str
    content: str


class BlogModel(BlogCreate):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blogs/", response_model=BlogModel)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    db_blog = Blog(title=blog.title, content=blog.content)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


@app.get("/blogs/{blog_id}", response_model=BlogModel)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog


@app.put("/blogs/{blog_id}", response_model=BlogModel)
def update_blog(blog_id: int, blog: BlogCreate, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    db_blog.title = blog.title
    db_blog.content = blog.content
    db.commit()
    db.refresh(db_blog)
    return db_blog


@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(db_blog)
    db.commit()
    return {"message": "Blog deleted successfully"}


def main():
    client = fastapi.testclient.TestClient(app)
    response = client.post("/blogs/", json={"title": "Test", "content": "Test"})
    assert response.status_code == 200, response.text

    blog = response.json()
    response = client.get(f"/blogs/{blog['id']}")
    assert response.status_code == 200, response.text
    assert response.json() == blog

    response = client.put(
        f"/blogs/{blog['id']}", json={"title": "Test", "content": "Test"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == blog

    response = client.delete(f"/blogs/{blog['id']}")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Blog deleted successfully"}

    response = client.get(f"/blogs/{blog['id']}")
    assert response.status_code == 404, response.text

    response = client.delete("/blogs/0")
    assert response.status_code == 404, response.text


if __name__ == "__main__":
    main()
