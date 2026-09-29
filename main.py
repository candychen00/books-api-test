from fastapi import FastAPI, HTTPException, Path, Query
from starlette import status
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

app = FastAPI()

class Book(BaseModel):
    id: int | None = Field(description= "ID is not needed on create", default=None)
    title: Annotated[ str, Field(min_length=3) ]
    author: Annotated[ str, Field(min_length=1) ]
    description: Annotated[ str, Field(min_length=3) ]
    rating: Annotated[int, Field(ge=1, le=5)] = 1
    publish_date: Annotated[int, Field(ge=1500, le=2026) ]

    model_config = ConfigDict(
        json_schema_extra={'examples': [
                {
                    "id": None,
                    "title": "A new book",
                    "author": "Author name",
                    "description": "This is description",
                    "rating": 3,
                    "publish_date": 2000
                }
            ]
        }
    )


# class BookRequest(BaseModel):
#     id: int
#     title: str
#     author: str
#     description: str
#     rating: int   



BOOKS_CLS = [
    Book(title="To Kill a Mockingbird", author="Harper Lee", description="A novel about racially charged injustice in the Deep South seen through the eyes of young Scout Finch.", rating=5, publish_date=2000),
    Book(title="1984", author="George Orwell", description="A dystopian social science fiction novel set in a totalitarian regime run by Big Brother.", rating=4, publish_date=2001),
    Book(title="The Great Gatsby", author="F. Scott Fitzgerald", description="A story detailing the mysterious millionaire Jay Gatsby and his obsession with Daisy Buchanan.", rating=3, publish_date=2002),
    Book(title="Pride and Prejudice", author="Jane Austen", description="A romantic novel following the turbulent relationship between Elizabeth Bennet and Fitzwilliam Darcy.", rating=2, publish_date=2003),
    Book(title="The Hobbit", author="J.R.R. Tolkien", description="A fantasy quest following Bilbo Baggins as he journeys to reclaim the lost Dwarf Kingdom of Erebor.", rating=1, publish_date=2004),
]


BOOKS = []
book_id = 0
for b in BOOKS_CLS:
    b_dict = b.model_dump()
    book_id += 1
    b_dict["id"] = book_id
    BOOKS.append(b_dict)



@app.get("/books", status_code=status.HTTP_200_OK)
def read_all_books():
    return BOOKS


@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
def find_book(book_id: int = Path(ge=1)) -> dict:
    for b in BOOKS:
        if b["id"] == book_id:
            return b
    raise HTTPException(status_code=404, detail="book not found")


@app.get("/query_book/rating", status_code=status.HTTP_200_OK)
def query_book_by_rating(rating: int = Query(ge=0,le=5)) -> list[dict]:
    books_to_return = []
    for b in BOOKS:
        if b["rating"] >= rating:
            books_to_return.append(b)
    if len(books_to_return) >0:
        return books_to_return
    else: 
        raise HTTPException(status_code=404, detail="Book not found.")


@app.get("/query_book/publish_date", status_code=status.HTTP_200_OK)
def query_book_by_publish_date(publish_date: int = Query(ge=1500,le=2026) ):
    books_to_return = []
    for b in BOOKS:
        if b["publish_date"] == publish_date:
            books_to_return.append(b)
    if len(books_to_return) > 0:
        return books_to_return
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
def create_book(book_data: Book):
    book = Book.model_validate(book_data)
    new_book = book.model_dump()

    new_book["id"] = len(BOOKS) +1
    BOOKS.append(new_book)


@app.post("/update_book", status_code=status.HTTP_204_NO_CONTENT)
def update_book(new_content: Book):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i]["id"] == new_content.id:
            BOOKS[i] = new_content.model_dump()
            book_changed = True
    if book_changed == True:
        return BOOKS[i]
    else:
        raise HTTPException(status_code=404, detail="Book not found")
        


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i]["id"] == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if book_changed == False:
        raise HTTPException(status_code=404, detail="Book not found")
        
