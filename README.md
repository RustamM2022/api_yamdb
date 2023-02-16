Описание:
Проект YaMDb собирает отзывы пользователей о фильмах, музыке, книгах (производства)

Пользователя может публиковать отзывы о произведениях, оценивать их (по шкале от 1 до 10), и обсуждать отзывы в результате

Средний рейтинг каждого продукта предлагается автоматически

Список категорий и жанров определен администратором, но может быть расширен в будущем.

Ключевые особенности:
Регистрация пользователей происходит путем передачи проверочного кода на электронную почту
Пользовательские роли: пользователь, модератор, админ
Кастомная фильтрация по жанру и категории
Кастомная аутентификация по токену JWT
Как играть проект:
Клонировать репозиторий:

git clone git@github.com:Port-tf/api_yamdb.git
Измените свою текущую дерикторию потребления:

cd /api_yamdb/
создавать и активировать окружающую среду

python -m venv venv
source venv/scripts/activate
Обновите пункт:

python3 -m pip install --upgrade pip
Установить зависимость от requirements.txt:

pip install -r requirements.txt
настроить выбор:

python manage.py migrate
Загрузить сервер:

python manage.py runserver
Полная документация прокта (redoc) доступна по адресу http://127.0.0.1:8000/redoc/
