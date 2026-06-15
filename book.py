from interfaces import BookSearch

class Book:
    def __init__(self, id: int, title: str, author: str, year: int, isbn: str, totalCopies: int):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.totalCopies = totalCopies
        self.availableCopies = totalCopies

    def isAvailable(self):
        return self.availableCopies > 0

    def __str__(self):
        return (
            f"[ID: {self.id} | '{self.title}' | Автор: {self.author} "
            f"| Рік: {self.year} | ISBN: {self.isbn} "
            f"| Копій: {self.availableCopies}/{self.totalCopies}]"
        )


class Catalog(BookSearch):
    def __init__(self):
        self.books = []

    def addBook(self, book: Book):
        self.books.append(book)

    def removeBook(self, bookId: int):
        self.books = [b for b in self.books if b.id != bookId]

    def findBooksByTitle(self, title: str):
        return [b for b in self.books if title.lower() in b.title.lower()]
    def get_info(self): pass
    def get_description(self): pass
