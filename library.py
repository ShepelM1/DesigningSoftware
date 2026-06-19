from interfaces import Notifier, BookSearch, BorrowingService
from datetime import date, timedelta
from book import Catalog, Book
from user import Reader
from borrowing import Borrowing


class LibraryManager(BorrowingService):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, catalog: BookSearch = None):
        if self._initialized:
            return

        self.catalog = catalog if catalog else Catalog()
        self.borrowings = []
        self._notifiers = []
        self._initialized = True

    # Сповіщення через абстракцію Notifier
    def attach(self, notifier: Notifier):
        self._notifiers.append(notifier)

    def detach(self, notifier: Notifier):
        self._notifiers.remove(notifier)

    def notify(self, message: str):
        for notifier in self._notifiers:
            notifier.notify(message)

    # Бізнес-логіка
    def addBook(self, book: Book):
        self.catalog.addBook(book)
        self.notify(f"Нова книга доступна: '{book.title}'")

    def updateBook(self, bookId: int, title: str = None, author: str = None,
                   year: int = None, isbn: str = None, totalCopies: int = None):
        for book in self.catalog.books:
            if book.id == bookId:
                if title is not None:
                    book.title = title
                if author is not None:
                    book.author = author
                if year is not None:
                    book.year = year
                if isbn is not None:
                    book.isbn = isbn
                if totalCopies is not None:
                    delta = totalCopies - book.totalCopies
                    book.totalCopies = totalCopies
                    book.availableCopies = max(0, book.availableCopies + delta)
                self.notify(f"Книга '{book.title}' оновлена")
                return book
        return None

    def removeBook(self, bookId: int):
        self.catalog.removeBook(bookId)
        self.notify(f"Книга з ID={bookId} видалена")

    def searchBooks(self, title: str):
        return self.catalog.findBooksByTitle(title)

    def getOverdueBorrowings(self, currentDate: date):
        return [
            b
            for b in self.borrowings
            if b.status == "active" and b.dueDate < currentDate
        ]

    # Інтерфейс BorrowingService
    def processBorrowing(self, reader: Reader, book: Book):
        if book.isAvailable():
            book.availableCopies -= 1

            borrowing = Borrowing(
                len(self.borrowings) + 1,
                reader,
                book,
                date.today(),
                date.today(),
            )

            self.borrowings.append(borrowing)
            self.notify(f"Книга '{book.title}' видана читачу {reader.fullName}")

            return borrowing

        return None

    def processReturn(self, borrowingId: int):
        for b in self.borrowings:
            if b.id == borrowingId and b.status == "active":
                b.markAsReturned()
                b.book.availableCopies += 1
                self.notify(
                    f"Книга '{b.book.title}' повернена читачем "
                    f"{b.reader.fullName}"
                )
                return True
        return False
