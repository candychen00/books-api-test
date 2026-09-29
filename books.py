from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/")
def first_api():
    return {"message": "Hello KL!"}


@app.get("/books")
def read_all_books():
    return BOOKS


@app.get("/books/search/id/{book_id}")
def get_book_by_id( book_id: int):
    book_id -=1
    return BOOKS[book_id]


@app.get("/books/search/title/{book_title}")
def get_book_by_title(book_title: str):
    for book in BOOKS:
        if book.get("title").lower() == book_title.lower():
            return book


@app.get("/books/search/author/{book_author}")
def get_book_by_author(book_author: str):
    authors_to_return = []
    for book in BOOKS:
        if book.get("author").lower() == book_author.lower():
            authors_to_return.append(book)
    return authors_to_return


@app.get("/books/query/author/{book_author}")
def query_book_by_author_cat(book_author: str, cat: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").lower() == book_author.lower() \
                and book.get("category").lower() == cat.lower():
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book


@app.put("/books/update_book")
def update_book(new_content=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").lower() == new_content.get("title").lower():
            BOOKS[i] = new_content
    return new_content


@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').lower() == book_title.lower():
            BOOKS.pop(i)
            break
    return BOOKS