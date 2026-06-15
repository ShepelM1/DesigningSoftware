from interfaces import Notifier, BorrowingService
from typing import Optional
from book import Book

class User:
    def __init__(self, id: int, fullName: str, email: str, phone: str):
        self.id = id
        self.fullName = fullName
        self.email = email
        self.phone = phone

class Librarian(User):
    def __init__(self, id: int, fullName: str, email: str, phone: str, employeeNumber: str):
        super().__init__(id, fullName, email, phone)
        self.employeeNumber = employeeNumber

    def register_reader(self, user_manager, fullName: str, email: str, phone: str, address: str):
        return user_manager.registerReader(fullName, email, phone, address)

    def add_book(self, library, book: Book):
        library.addBook(book)

    def edit_book(self, library, bookId: int, title: Optional[str] = None, author: Optional[str] = None,
                  year: Optional[int] = None, isbn: Optional[str] = None, totalCopies: Optional[int] = None):
        library.updateBook(bookId, title, author, year, isbn, totalCopies)

    def remove_book(self, library, bookId: int):
        library.removeBook(bookId)

    def track_overdue(self, library, currentDate):
        return library.getOverdueBorrowings(currentDate)

    def send_reminder(self, notifier: Notifier, message: str):
        notifier.notify(message)


class UserManager:
    def __init__(self):
        self.users = []

    def registerReader(self, fullName, email, phone, address):
        new_id = len(self.users) + 1
        reader = Reader(new_id, fullName, email, phone, address)
        self.users.append(reader)
        return reader

    def registerLibrarian(self, fullName, email, phone, employeeNumber):
        new_id = len(self.users) + 1
        librarian = Librarian(new_id, fullName, email, phone, employeeNumber)
        self.users.append(librarian)
        return librarian

class Reader(User, Notifier):
    def __init__(self, id: int, fullName: str, email: str, phone: str, address: str):
        super().__init__(id, fullName, email, phone)
        self.address = address

    def search_books(self, library, title: str):
        return library.searchBooks(title)

    def borrow_book(self, library: BorrowingService, book: Book):
        return library.processBorrowing(self, book)

    def return_book(self, library: BorrowingService, borrowingId: int):
        return library.processReturn(borrowingId)

    def notify(self, message: str):
        print(f"Повідомлення для {self.fullName}: {message}")