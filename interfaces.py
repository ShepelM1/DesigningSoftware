from abc import ABC, abstractmethod


# Інтерфейс для сповіщення користувачів та обробників подій
class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass


# Інтерфейс для пошуку книг у каталозі
class BookSearch(ABC):
    @abstractmethod
    def findBooksByTitle(self, title: str):
        pass


# Інтерфейс для операцій видачі/повернення книг
class BorrowingService(ABC):

    @abstractmethod
    def processBorrowing(self, reader, book):
        pass

    @abstractmethod
    def processReturn(self, borrowingId: int):
        pass
