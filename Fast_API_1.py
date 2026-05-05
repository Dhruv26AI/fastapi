# To run code use this code in vscode bash - uvicorn app:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Memes Book API")

# ------------------ Data ------------------
books = [

     {"id": 1, "title": "The Path to Leadership", "author": "Aarav Sharma"},
    {"id": 2, "title": "Winning Strategies", "author": "Elena Rossi"},
    {"id": 3, "title": "Achieving Global Recognition", "author": "Michael Carter"},
    {"id": 4, "title": "Creative Thinking Simplified", "author": "Priya Verma"},
    {"id": 5, "title": "The Art of Doing Nothing", "author": "Rahul Mehta"},
    {"id": 6, "title": "Becoming Unstoppable", "author": "Yuki Tanaka"},
    {"id": 7, "title": "The Power of Consistency", "author": "Dinesh Kumar"}
]

# ------------------ Schema ------------------
class Book(BaseModel):
    id: int
    title: str
    author: str

class BookCreate(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

# ------------------ Helper ------------------
def find_book(book_id: int):
    return next((book for book in books if book["id"] == book_id), None)

# ------------------ Routes ------------------

@app.get("/")
def home():
    return {"message": "Welcome to the memes book world"}

@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book, status_code=201)
def create_book(book: BookCreate):
    new_id = max([b["id"] for b in books], default=0) + 1
    new_book = {"id": new_id, "title": book.title, "author": book.author}
    books.append(new_book)
    return new_book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated: BookUpdate):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if updated.title is not None:
        book["title"] = updated.title
    if updated.author is not None:
        book["author"] = updated.author

    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    books.remove(book)
    return {"message": "Book deleted successfully"}
