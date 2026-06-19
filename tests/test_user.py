import os
import sys
import unittest
from unittest.mock import Mock
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user import UserManager, Reader  # noqa: E402
from book import Book  # noqa: E402
from interfaces import Notifier, BorrowingService  # noqa: E402


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.reader = self.user_manager.registerReader(
            'Владислав',
            'vladyslav@e.com',
            '+380',
            'вул. Рівненська',
        )
        self.mock_library = Mock(spec=BorrowingService)
        self.mock_notifier = Mock(spec=Notifier)
        self.book1 = Book(101, 'Head First Python', 'Пол Беррі', 2010, 'ISBN-101', 2)
        self.book2 = Book(102, 'Чистий код', 'Роберт Мартін', 2008, 'ISBN-102', 1)

    def test_initial_state_of_reader(self):
        self.assertEqual(self.reader.fullName, 'Владислав')
        self.assertEqual(self.reader.email, 'vladyslav@e.com')
        self.assertEqual(self.reader.phone, '+380')
        self.assertEqual(self.reader.address, 'вул. Рівненська')
        self.assertGreater(self.reader.id, 0)

    def test_successful_borrow_book_calls_library(self):
        mock_borrowing = Mock()
        self.mock_library.processBorrowing.return_value = mock_borrowing

        result = self.reader.borrow_book(
            self.mock_library,
            self.book1,
        )

        self.mock_library.processBorrowing.assert_called_once_with(
            self.reader,
            self.book1,
        )
        self.assertEqual(result, mock_borrowing)

    def test_borrow_unavailable_book_returns_none(self):
        self.mock_library.processBorrowing.return_value = None

        result = self.reader.borrow_book(self.mock_library, self.book1)

        self.assertIsNone(result)

    def test_borrow_multiple_books(self):
        bor1 = Mock()
        bor2 = Mock()
        self.mock_library.processBorrowing.side_effect = [bor1, bor2]

        r1 = self.reader.borrow_book(self.mock_library, self.book1)
        r2 = self.reader.borrow_book(self.mock_library, self.book2)

        self.assertEqual(self.mock_library.processBorrowing.call_count, 2)
        self.assertEqual(r1, bor1)
        self.assertEqual(r2, bor2)

    def test_successful_return_book_calls_library(self):
        self.mock_library.processReturn.return_value = True

        result = self.reader.return_book(self.mock_library, 1)

        self.mock_library.processReturn.assert_called_once_with(1)
        self.assertTrue(result)

    def test_return_nonexistent_borrowing_returns_false(self):
        self.mock_library.processReturn.return_value = False

        result = self.reader.return_book(self.mock_library, 999)

        self.mock_library.processReturn.assert_called_once_with(999)
        self.assertFalse(result)

    def test_reader_notify_implementation(self):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            self.reader.notify('Тестове сповіщення')
        finally:
            sys.stdout = old_stdout
        output = buf.getvalue()
        self.assertIn('Повідомлення для', output)
        self.assertIn('Владислав', output)

    def test_librarian_register_reader(self):
        librarian = self.user_manager.registerLibrarian(
            'Іван',
            'ivan@lib.com',
            '+380',
            'emp-001',
        )

        new_reader = librarian.register_reader(
            self.user_manager, 'Петро', 'petro@e.com', '+380123', 'адреса'
        )

        self.assertIsInstance(new_reader, Reader)
        self.assertEqual(new_reader.fullName, 'Петро')

    def test_librarian_send_reminder_calls_notifier(self):
        librarian = self.user_manager.registerLibrarian(
            'Іван',
            'ivan@lib.com',
            '+380',
            'emp-001',
        )

        librarian.send_reminder(
            self.mock_notifier,
            'Нагадування: поверніть книгу!',
        )

        self.mock_notifier.notify.assert_called_once_with(
            'Нагадування: поверніть книгу!'
        )

    def test_reader_search_books_delegates_to_library(self):
        mock_results = [self.book1, self.book2]
        mock_lib_search = Mock()
        mock_lib_search.searchBooks.return_value = mock_results

        result = self.reader.search_books(mock_lib_search, 'Python')

        mock_lib_search.searchBooks.assert_called_once_with('Python')
        self.assertEqual(result, mock_results)


if __name__ == '__main__':
    unittest.main()
