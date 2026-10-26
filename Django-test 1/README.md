# Django Blog

Учебный Django-проект со списком статей, страницей подробностей и счетчиком
просмотров. Каждый GET-запрос страницы статьи увеличивает счетчик на единицу.

## Запуск

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Список статей доступен по адресу `/`, страница статьи — `/blogs/<id>/`.

## CRUD-заготовка

Приложение `crud` — отдельный пример полного CRUD-цикла для модели `Item`:

- список и просмотр записи;
- создание и редактирование через `ModelForm`;
- удаление с подтверждением.

Страницы доступны с префиксом `/crud/`. Это приложение можно использовать как
основу для следующих заданий: создайте приложение командой
`python manage.py startapp имя_приложения`, скопируйте структуру `crud`,
замените модель `Item` и обновите регистрацию приложения в `INSTALLED_APPS`
и `blog_project/urls.py`.

После изменения модели создайте и примените миграции:

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Тесты

```powershell
python manage.py test
```
