from datetime import date


class Borrowing:
    def __init__(self, id: int, reader, book, borrowDate, dueDate):
        self.id = id
        self.reader = reader
        self.book = book
        self.borrowDate = borrowDate
        self.dueDate = dueDate
        self.returnDate = None
        self.status = "active"

    def markAsReturned(self):
        self.status = "returned"
        self.returnDate = date.today()


class Notification:
    def __init__(self, id: int, reader, message: str, notifType: str):
        self.id = id
        self.reader = reader
        self.message = message
        self.type = notifType
        self.sentDate = None

    def sendEmail(self):
        self.sentDate = date.today()