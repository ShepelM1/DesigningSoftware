# Система управління бібліотекою

## Опис
Система для автоматизації роботи бібліотеки: облік книг, видача/повернення, 
сповіщення читачів.

## Функціональність
- Додавання/видалення книг
- Реєстрація читачів
- Видача та повернення книг
- Сповіщення про нові надходження (патерн Observer)

## Встановлення
```bash
git clone https://github.com/your-username/library-system.git
cd library-system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Запуск
bash
python main.py
Запуск тестів
bash
python -m unittest discover tests/
Автор
Студент групи ІПЗ-31фб Шепель Микола Русланович
text

