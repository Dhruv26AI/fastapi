# To run code use this code in vscode bash - uvicorn app:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Memes Book API")

# ------------------ Data ------------------
books = [

    {"id": 1, "title": "How to become king", "author": "King Babar"},

    {"id": 2, "title": "How to win Modi", "author": "Meloni"},

    {"id": 3, "title": "How to get noble peace price", "author": "Trump"},

    {"id": 4, "title": "Hamba hamba rambha rambha", "author": "Mamta"},

    {"id": 5, "title": "How to learn nothing", "author": "Rahul"},

    {"id": 6, "title": "How to become strongest", "author": "Yamucha"},
    
    {"id": 7, "title": "Thala for a reason", "author": "Dhoni"}
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