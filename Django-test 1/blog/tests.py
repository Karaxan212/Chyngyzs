from django.test import TestCase
from django.urls import reverse

from blog.models import Blog


class BlogListDetailTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(
            title="Test article",
            content="Article body for detail view.",
        )

    def test_blog_list_returns_success_and_contains_article(self):
        response = self.client.get(reverse("blog:blog_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog.title)

    def test_blog_list_context_contains_blog(self):
        response = self.client.get(reverse("blog:blog_list"))

        self.assertIn(self.blog, response.context["blogs"])

    def test_empty_blog_list_displays_empty_message(self):
        Blog.objects.all().delete()

        response = self.client.get(reverse("blog:blog_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пока нет статей.")

    def test_detail_returns_article_content_and_id(self):
        response = self.client.get(
            reverse("blog:blog_detail", args=[self.blog.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog.content)
        self.assertEqual(response.context["blog"].pk, self.blog.pk)

    def test_detail_for_unknown_id_returns_404(self):
        response = self.client.get(
            reverse("blog:blog_detail", args=[self.blog.pk + 100])
        )

        self.assertEqual(response.status_code, 404)

    def test_list_link_opens_the_matching_detail_page(self):
        list_response = self.client.get(reverse("blog:blog_list"))
        detail_url = reverse("blog:blog_detail", args=[self.blog.pk])

        self.assertContains(list_response, f'href="{detail_url}"')
        detail_response = self.client.get(detail_url)

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.blog.content)

    def test_new_blog_starts_with_zero_likes(self):
        self.assertEqual(self.blog.likes, 0)

    def test_getting_detail_increments_likes_once(self):
        self.client.get(reverse("blog:blog_detail", args=[self.blog.pk]))
        self.blog.refresh_from_db()

        self.assertEqual(self.blog.likes, 1)

    def test_each_detail_visit_increments_likes(self):
        detail_url = reverse("blog:blog_detail", args=[self.blog.pk])
        self.client.get(detail_url)
        self.client.get(detail_url)
        self.blog.refresh_from_db()

        self.assertEqual(self.blog.likes, 2)
