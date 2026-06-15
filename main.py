# Головний модуль main.py
# Модулі:
# book.py – книги та каталог
# library.py – Singleton + інтерфейси
# notifications.py – реалізації Notifier
# user.py – Reader реалізує інтерфейс Notifier

from datetime import date
from book import Book
from library import LibraryManager
from notifications import EmailAlert
from user import Reader, Librarian, UserManager


def register_notifiers(manager, notifiers):
    # Підписка об'єктів, які реалізують інтерфейс Notifier
    for notifier in notifiers:
        manager.attach(notifier)


def main():
    # Отримуємо єдиний екземпляр бібліотеки
    library = LibraryManager()

    user_manager = UserManager()

    reader = user_manager.registerReader(
        fullName="Shepel Mykola",
        email="shepel_ak24@test.com",
        phone="+380980000000",
        address="м.Рівне"
    )

    librarian = user_manager.registerLibrarian(
        fullName="Librarian",
        email="librarian@example.com",
        phone="+380999999999",
        employeeNumber="1"
    )

    email_alert = EmailAlert("admin@library.com")

    register_notifiers(library, [reader, email_alert])

    print("\nДемонстрація роботи через інтерфейс Notifier:")

    book = Book(
        1,
        "Чиста архітектура",
        "Роберт Мартін",
        2018,
        "111-222",
        2
    )

    librarian.add_book(library, book)
    print(f"Кількість книг у каталозі: {len(library.catalog.books)}")

    found = reader.search_books(library, "архітектура")
    print(f"Знайдено {len(found)} книгу(и) за заголовком 'архітектура'.")

    borrowing = reader.borrow_book(library, book)
    if borrowing:
        print(f"{reader.fullName} взяв книгу на абонемент: {book.title}")

    librarian.send_reminder(email_alert, "Нагадування: будь ласка, поверніть книгу")

    if borrowing:
        returned = reader.return_book(library, borrowing.id)
        if returned:
            print(f"{reader.fullName} повернув книгу: {book.title}")

    librarian.edit_book(library, book.id, title="Чиста архітектура. Видання 2")
    librarian.remove_book(library, book.id)

    overdue = librarian.track_overdue(library, date.today())
    print(f"Прострочених книг: {len(overdue)}")

    


if __name__ == "__main__":
    main()