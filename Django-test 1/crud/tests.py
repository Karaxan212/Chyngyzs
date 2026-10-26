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
        response = self.client.get(reverse("crud:item_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.title)
        self.assertContains(response, reverse("crud:item_create"))

    def test_detail_displays_item(self):
        response = self.client.get(
            reverse("crud:item_detail", args=[self.item.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.title)
        self.assertContains(response, self.item.description)

    def test_create_item(self):
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

    def test_update_item(self):
        response = self.client.post(
            reverse("crud:item_update", args=[self.item.pk]),
            {"title": "Updated item", "description": "Updated description"},
        )

        self.assertRedirects(response, reverse("crud:item_list"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Updated item")
        self.assertEqual(self.item.description, "Updated description")

    def test_delete_requires_confirmation_and_deletes_on_post(self):
        delete_url = reverse("crud:item_delete", args=[self.item.pk])
        response = self.client.get(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Item.objects.filter(pk=self.item.pk).exists())

        response = self.client.post(delete_url)

        self.assertRedirects(response, reverse("crud:item_list"))
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())

    def test_unknown_item_returns_404(self):
        response = self.client.get(
            reverse("crud:item_detail", args=[self.item.pk + 100])
        )

        self.assertEqual(response.status_code, 404)
