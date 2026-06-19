import unittest
import sys
import os
from unittest.mock import Mock
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library import LibraryManager
from book import Book, Catalog
from borrowing import Borrowing
from user import Reader
from interfaces import Notifier


class TestLibraryManager(unittest.TestCase):
    def setUp(self):
        LibraryManager._instance = None
        self.library = LibraryManager()

    def tearDown(self):
        LibraryManager._instance = None

    def test_singleton_unique_instance(self):
        lib1 = LibraryManager()
        lib2 = LibraryManager()
        self.assertIs(lib1, lib2)
        self.assertEqual(id(lib1), id(lib2))

    def test_attach_single_observer(self):
        mock_observer = Mock(spec=Notifier)
        self.library.attach(mock_observer)
        self.assertIn(mock_observer, self.library._notifiers)

    def test_attach_multiple_observers(self):
        mock1 = Mock(spec=Notifier)
        mock2 = Mock(spec=Notifier)
        mock3 = Mock(spec=Notifier)

        self.library.attach(mock1)
        self.library.attach(mock2)
        self.library.attach(mock3)

        self.assertEqual(len(self.library._notifiers), 3)
        self.assertIn(mock1, self.library._notifiers)
        self.assertIn(mock2, self.library._notifiers)
        self.assertIn(mock3, self.library._notifiers)

    def test_detach_observer(self):
        mock1 = Mock(spec=Notifier)
        mock2 = Mock(spec=Notifier)

        self.library.attach(mock1)
        self.library.attach(mock2)
        self.library.detach(mock1)

        self.assertNotIn(mock1, self.library._notifiers)
        self.assertIn(mock2, self.library._notifiers)

    def test_notify_all_observers(self):
        mock1 = Mock(spec=Notifier)
        mock2 = Mock(spec=Notifier)

        self.library.attach(mock1)
        self.library.attach(mock2)

        self.library.notify('Тестове повідомлення')

        mock1.notify.assert_called_once_with('Тестове повідомлення')
        mock2.notify.assert_called_once_with('Тестове повідомлення')

    def test_addBook_notifies_observers(self):
        mock_observer = Mock(spec=Notifier)
        self.library.attach(mock_observer)

        book = Book(1, 'Нова книга', 'Автор', 2024, 'ISBN-001', 2)
        self.library.addBook(book)

        # Виклик notify з повідомленням про додавання
        mock_observer.notify.assert_called()
        call_args = mock_observer.notify.call_args[0][0]
        self.assertIn('Нова книга', call_args)

    def test_addBook_adds_to_catalog(self):
        book = Book(1, 'Python 101', 'Автор', 2024, 'ISBN-001', 3)
        self.library.addBook(book)

        self.assertIn(book, self.library.catalog.books)

    def test_removeBook_notifies_observers(self):
        mock_observer = Mock(spec=Notifier)
        self.library.attach(mock_observer)

        book = Book(1, 'Книга', 'Автор', 2024, 'ISBN', 1)
        self.library.addBook(book)
        mock_observer.reset_mock()  # скинути виклики від addBook

        self.library.removeBook(1)

        mock_observer.notify.assert_called()
        call_args = mock_observer.notify.call_args[0][0]
        self.assertIn('видалена', call_args.lower() or 'removed' in call_args.lower())

    def test_processBorrowing_success(self):
        reader = Reader(1, 'Іван', 'ivan@e.com', '+380', 'адреса')
        book = Book(2, 'Книга', 'Автор', 2024, 'ISBN', 2)
        self.library.addBook(book)

        initial_copies = book.availableCopies
        borrowing = self.library.processBorrowing(reader, book)

        self.assertIsNotNone(borrowing)
        self.assertEqual(book.availableCopies, initial_copies - 1)
        self.assertEqual(borrowing.reader, reader)
        self.assertEqual(borrowing.book, book)

    def test_processBorrowing_unavailable_book_returns_none(self):
        reader = Reader(1, 'Іван', 'ivan@e.com', '+380', 'адреса')
        book = Book(2, 'Книга', 'Автор', 2024, 'ISBN', 0)  # 0 копій
        self.library.addBook(book)

        borrowing = self.library.processBorrowing(reader, book)

        self.assertIsNone(borrowing)

    def test_processReturn_success(self):
        reader = Reader(1, 'Іван', 'ivan@e.com', '+380', 'адреса')
        book = Book(2, 'Книга', 'Автор', 2024, 'ISBN', 1)
        self.library.addBook(book)

        borrowing = self.library.processBorrowing(reader, book)
        initial_copies = book.availableCopies

        result = self.library.processReturn(borrowing.id)

        self.assertTrue(result)
        self.assertEqual(borrowing.status, 'returned')
        self.assertEqual(book.availableCopies, initial_copies + 1)

    def test_processReturn_nonexistent_borrowing(self):
        result = self.library.processReturn(999)
        self.assertFalse(result)

    def test_getOverdueBorrowings(self):
        reader = Reader(1, 'Іван', 'ivan@e.com', '+380', 'адреса')
        book = Book(2, 'Книга', 'Автор', 2024, 'ISBN', 1)

        # Створення видачі з давнішньою датою
        past_date = date.today() - timedelta(days=5)
        borrowing = Borrowing(
            1,
            reader,
            book,
            past_date - timedelta(days=10),
            past_date,
        )
        self.library.borrowings.append(borrowing)

        overdue = self.library.getOverdueBorrowings(date.today())

        self.assertIn(borrowing, overdue)

    def test_searchBooks(self):
        book1 = Book(1, 'Python 101', 'Автор', 2024, 'ISBN1', 2)
        book2 = Book(2, 'Java for Dummies', 'Автор', 2024, 'ISBN2', 1)
        self.library.addBook(book1)
        self.library.addBook(book2)

        results = self.library.searchBooks('Python')

        self.assertIn(book1, results)
        self.assertNotIn(book2, results)

    def test_updateBook(self):
        """Тест 15: updateBook() оновлює параметри книги і викликає notify()."""
        mock_observer = Mock(spec=Notifier)
        self.library.attach(mock_observer)

        book = Book(1, 'Стара назва', 'Автор', 2020, 'ISBN', 2)
        self.library.addBook(book)
        mock_observer.reset_mock()

        self.library.updateBook(1, title='Нова назва')

        self.assertEqual(book.title, 'Нова назва')
        mock_observer.notify.assert_called()

    def test_updateBook_totalCopies_increase_adjusts_available(self):
        """updateBook increases totalCopies and availableCopies accordingly."""
        book = Book(10, 'Книга', 'A', 2020, 'ISBNX', 1)
        book.availableCopies = 1
        self.library.addBook(book)

        self.library.updateBook(10, totalCopies=3)

        self.assertEqual(book.totalCopies, 3)
        self.assertEqual(book.availableCopies, 3)

    def test_updateBook_totalCopies_decrease_adjusts_available_not_negative(self):
        """updateBook decreases totalCopies and availableCopies not below zero."""
        book = Book(11, 'Книга2', 'A', 2020, 'ISBNY', 3)
        book.availableCopies = 2
        self.library.addBook(book)

        self.library.updateBook(11, totalCopies=1)

        self.assertEqual(book.totalCopies, 1)
        self.assertEqual(book.availableCopies, 0)


if __name__ == '__main__':
    unittest.main()
