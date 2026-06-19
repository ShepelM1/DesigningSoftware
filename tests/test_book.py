import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from book import Book
from library import LibraryManager
from user import Reader


class TestBook(unittest.TestCase):

    def setUp(self):
        # Скидання Singleton між тестами
        try:
            LibraryManager._instance = None
        except Exception:
            pass

        self.book = Book(1, "Test Book", "Author", 2020, "ISBN-001", totalCopies=1)
        self.library = LibraryManager()

        # Додавання книги в каталог
        self.library.addBook(self.book)

        # Читач
        self.reader = Reader(
            1,
            "Shepel Mykola",
            "user@example.com",
            "+380000000000",
            "вул. Соборна",
        )

    def test_initial_state(self):
        self.assertEqual(self.book.availableCopies, self.book.totalCopies)
        self.assertTrue(self.book.isAvailable())

    def test_successful_borrow(self):
        borrowing = self.library.processBorrowing(self.reader, self.book)
        self.assertIsNotNone(borrowing)
        self.assertEqual(self.book.availableCopies, 0)
        self.assertFalse(self.book.isAvailable())
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.reader, self.reader)

    def test_borrow_already_taken(self):
        first = self.library.processBorrowing(self.reader, self.book)
        self.assertIsNotNone(first)
        second = self.library.processBorrowing(self.reader, self.book)
        self.assertIsNone(second)
        self.assertEqual(self.book.availableCopies, 0)

    def test_successful_return(self):
        borrowing = self.library.processBorrowing(self.reader, self.book)
        self.assertIsNotNone(borrowing)
        result = self.library.processReturn(borrowing.id)
        self.assertTrue(result)
        self.assertEqual(self.book.availableCopies, 1)
        self.assertEqual(borrowing.status, "returned")

    def test_return_not_borrowed(self):
        # Немає повернень по id 999
        result = self.library.processReturn(999)
        self.assertFalse(result)
        self.assertEqual(self.book.availableCopies, self.book.totalCopies)


if __name__ == '__main__':
    unittest.main()
