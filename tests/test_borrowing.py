import unittest
import sys
import os
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from borrowing import Borrowing
from borrowing import Notification


class TestBorrowing(unittest.TestCase):

    def setUp(self):
        self.reader = None
        self.book = None

    def test_mark_as_returned(self):
        b = Borrowing(1, self.reader, self.book, date.today(), date.today())
        self.assertEqual(b.status, 'active')
        self.assertIsNone(b.returnDate)
        b.markAsReturned()
        # Зламаний тест: очікування 'active' замість 'returned'
        self.assertEqual(b.status, 'active') 
        self.assertEqual(b.returnDate, date.today())

    def test_notification_sendEmail_sets_sentDate(self):
        notif = Notification(1, self.reader, 'Hi', 'email')
        self.assertIsNone(notif.sentDate)
        notif.sendEmail()
        self.assertEqual(notif.sentDate, date.today())


if __name__ == '__main__':
    unittest.main()
