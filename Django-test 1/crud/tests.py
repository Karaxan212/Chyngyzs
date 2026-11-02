from django.test import TestCase
from django.urls import reverse

from crud.models import Item


class ItemCrudTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            title="Test item",
            description="Test description",
        )

    def test_list_displays_items_and_create_link(self):
        """Список показывает записи и ссылку на создание."""
        response = self.client.get(reverse("crud:item_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.title)
        self.assertContains(response, reverse("crud:item_create"))

    def test_empty_list_displays_empty_message(self):
        """Для пустого списка отображается сообщение."""
        Item.objects.all().delete()

        response = self.client.get(reverse("crud:item_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Записей пока нет.")

    def test_detail_displays_item(self):
        """Страница записи показывает ее заголовок и описание."""
        response = self.client.get(
            reverse("crud:item_detail", args=[self.item.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.title)
        self.assertContains(response, self.item.description)

    def test_create_item(self):
        """Создание сохраняет запись и перенаправляет к списку."""
        response = self.client.post(
            reverse("crud:item_create"),
            {"title": "New item", "description": "New description"},
        )

        self.assertRedirects(response, reverse("crud:item_list"))
        self.assertTrue(
            Item.objects.filter(
                title="New item",
                description="New description",
            ).exists()
        )

    def test_create_item_without_description(self):
        """Описание записи необязательно."""
        response = self.client.post(
            reverse("crud:item_create"),
            {"title": "Item without description", "description": ""},
        )

        self.assertRedirects(response, reverse("crud:item_list"))
        item = Item.objects.get(title="Item without description")
        self.assertEqual(item.description, "")

    def test_create_item_without_title_is_rejected(self):
        """Форма создания требует заголовок."""
        response = self.client.post(
            reverse("crud:item_create"),
            {"title": "", "description": "Description"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)
        self.assertEqual(Item.objects.count(), 1)

    def test_update_item(self):
        """Редактирование сохраняет изменения и перенаправляет к списку."""
        response = self.client.post(
            reverse("crud:item_update", args=[self.item.pk]),
            {"title": "Updated item", "description": "Updated description"},
        )

        self.assertRedirects(response, reverse("crud:item_list"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Updated item")
        self.assertEqual(self.item.description, "Updated description")

    def test_update_item_without_title_is_rejected(self):
        """Форма редактирования требует заголовок и не меняет запись."""
        response = self.client.post(
            reverse("crud:item_update", args=[self.item.pk]),
            {"title": "", "description": "Changed description"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Test item")
        self.assertEqual(self.item.description, "Test description")

    def test_delete_requires_confirmation_and_deletes_on_post(self):
        """GET запрашивает подтверждение, POST удаляет запись."""
        delete_url = reverse("crud:item_delete", args=[self.item.pk])
        response = self.client.get(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.title)
        self.assertTrue(Item.objects.filter(pk=self.item.pk).exists())

        response = self.client.post(delete_url)

        self.assertRedirects(response, reverse("crud:item_list"))
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())

    def test_unknown_item_returns_404(self):
        """Страницы просмотра, изменения и удаления отсутствующей записи дают 404."""
        missing_pk = self.item.pk + 100
        urls = (
            reverse("crud:item_detail", args=[missing_pk]),
            reverse("crud:item_update", args=[missing_pk]),
            reverse("crud:item_delete", args=[missing_pk]),
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
