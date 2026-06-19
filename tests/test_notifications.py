import io
import unittest
import sys
import os
from unittest.mock import Mock
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notifications import NotificationScheduler  # noqa: E402
from borrowing import Borrowing  # noqa: E402


class TestNotifications(unittest.TestCase):

    def test_checkOverdueBooks_logs_and_notifies(self):
        # Створено mock LibraryManager
        mock_lib = Mock()
        # Створено mock reader з notify
        mock_reader = Mock()
        mock_reader.fullName = 'Ivan'
        # Створеено об'єкт книги
        book = Mock()
        book.title = 'Old Book'
        book.id = 5

        bor = Borrowing(
            1,
            mock_reader,
            book,
            date.today() - timedelta(days=10),
            date.today() - timedelta(days=1),
        )
        mock_lib.getOverdueBorrowings.return_value = [bor]

        scheduler = NotificationScheduler(mock_lib)
        messages = scheduler.checkOverdueBooks(date.today())

        self.assertEqual(len(messages), 1)
        self.assertEqual(len(scheduler.notificationLog), 1)
        mock_reader.notify.assert_called()

    def test_checkOverdueBooks_reader_without_notify_prints_and_logs(self):
        mock_lib = Mock()

        class SimpleReader:
            def __init__(self):
                self.fullName = 'NoNotify'

        reader = SimpleReader()
        book = Mock()
        book.title = 'NoNotify Book'
        book.id = 7

        bor = Borrowing(
            2,
            reader,
            book,
            date.today() - timedelta(days=5),
            date.today() - timedelta(days=1),
        )
        mock_lib.getOverdueBorrowings.return_value = [bor]

        scheduler = NotificationScheduler(mock_lib)
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            messages = scheduler.checkOverdueBooks(date.today())
        finally:
            sys.stdout = old

        self.assertEqual(len(messages), 1)
        self.assertEqual(len(scheduler.notificationLog), 1)
        out = buf.getvalue()
        self.assertIn('Прострочено', out)

    def test_checkOverdueBooks_reader_notify_raises_exception_prints(self):
        mock_lib = Mock()
        mock_reader = Mock()
        mock_reader.fullName = 'BadReader'

        def raise_exc(msg):
            raise RuntimeError('boom')

        mock_reader.notify.side_effect = raise_exc

        book = Mock()
        book.title = 'Bad Book'
        book.id = 9

        bor = Borrowing(
            3,
            mock_reader,
            book,
            date.today() - timedelta(days=4),
            date.today() - timedelta(days=1),
        )
        mock_lib.getOverdueBorrowings.return_value = [bor]

        scheduler = NotificationScheduler(mock_lib)
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            messages = scheduler.checkOverdueBooks(date.today())
        finally:
            sys.stdout = old

        mock_reader.notify.assert_called()
        self.assertEqual(len(messages), 1)
        self.assertEqual(len(scheduler.notificationLog), 1)
        out = buf.getvalue()
        self.assertIn('Прострочено', out)


if __name__ == '__main__':
    unittest.main()
