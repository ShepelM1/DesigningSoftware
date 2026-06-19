from interfaces import Notifier


class NotificationScheduler(Notifier):
    def __init__(self, libraryManager):
        self.libraryManager = libraryManager
        self.notificationLog = []

    def notify(self, message: str):
        self.notificationLog.append(message)

    def checkOverdueBooks(self, currentDate):
        overdue = []
        try:
            overdue = self.libraryManager.getOverdueBorrowings(currentDate)
        except Exception:
            return []

        messages = []
        for b in overdue:
            msg = (
                f"Прострочено: '{b.book.title}' (ID:{b.book.id}) - читач: "
                f"{b.reader.fullName}, термін: {b.dueDate}"
            )
            self.notificationLog.append(msg)

            if hasattr(b.reader, 'notify'):
                try:
                    b.reader.notify(msg)
                except Exception:
                    print(msg)
            else:
                print(msg)
            messages.append(msg)

        return messages

class EmailAlert(Notifier):
    def __init__(self, email):
        self.email = email

    def notify(self, message: str):
        print(f"EmailAlert на {self.email}: {message}")
