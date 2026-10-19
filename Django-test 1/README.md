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

## Тесты

```powershell
python manage.py test
```
