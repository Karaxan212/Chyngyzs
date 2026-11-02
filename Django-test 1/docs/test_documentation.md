# Документация тестирования

Сформировано автоматически: 2026-11-02T15:49:07+06:00.

Документ обновляется при каждом запуске `python manage.py test`.

## Результаты

- Всего тестов: 19
- Пройдено: 19
- Не пройдено: 0
- Ошибок: 0
- Пропущено: 0
- Ожидаемых сбоев: 0

## Проверки

| Тест | Сценарий | Результат |
| --- | --- | --- |
| `blog.tests.BlogListDetailTests.test_blog_list_context_contains_blog` | blog list context contains blog | Пройден |
| `blog.tests.BlogListDetailTests.test_blog_list_returns_success_and_contains_article` | blog list returns success and contains article | Пройден |
| `blog.tests.BlogListDetailTests.test_detail_for_unknown_id_returns_404` | detail for unknown id returns 404 | Пройден |
| `blog.tests.BlogListDetailTests.test_detail_returns_article_content_and_id` | detail returns article content and id | Пройден |
| `blog.tests.BlogListDetailTests.test_each_detail_visit_increments_likes` | each detail visit increments likes | Пройден |
| `blog.tests.BlogListDetailTests.test_empty_blog_list_displays_empty_message` | empty blog list displays empty message | Пройден |
| `blog.tests.BlogListDetailTests.test_getting_detail_increments_likes_once` | getting detail increments likes once | Пройден |
| `blog.tests.BlogListDetailTests.test_list_link_opens_the_matching_detail_page` | list link opens the matching detail page | Пройден |
| `blog.tests.BlogListDetailTests.test_new_blog_starts_with_zero_likes` | new blog starts with zero likes | Пройден |
| `crud.tests.ItemCrudTests.test_create_item` | Создание сохраняет запись и перенаправляет к списку. | Пройден |
| `crud.tests.ItemCrudTests.test_create_item_without_description` | Описание записи необязательно. | Пройден |
| `crud.tests.ItemCrudTests.test_create_item_without_title_is_rejected` | Форма создания требует заголовок. | Пройден |
| `crud.tests.ItemCrudTests.test_delete_requires_confirmation_and_deletes_on_post` | GET запрашивает подтверждение, POST удаляет запись. | Пройден |
| `crud.tests.ItemCrudTests.test_detail_displays_item` | Страница записи показывает ее заголовок и описание. | Пройден |
| `crud.tests.ItemCrudTests.test_empty_list_displays_empty_message` | Для пустого списка отображается сообщение. | Пройден |
| `crud.tests.ItemCrudTests.test_list_displays_items_and_create_link` | Список показывает записи и ссылку на создание. | Пройден |
| `crud.tests.ItemCrudTests.test_unknown_item_returns_404` | Страницы просмотра, изменения и удаления отсутствующей записи дают 404. | Пройден |
| `crud.tests.ItemCrudTests.test_update_item` | Редактирование сохраняет изменения и перенаправляет к списку. | Пройден |
| `crud.tests.ItemCrudTests.test_update_item_without_title_is_rejected` | Форма редактирования требует заголовок и не меняет запись. | Пройден |
