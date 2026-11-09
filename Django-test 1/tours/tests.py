from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tours.models import Booking, Category, Review, RiderProfile, Tour


class TourWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="rider", password="StrongPass123!", email="rider@example.com"
        )
        RiderProfile.objects.create(user=self.user, phone="+996700123456")
        self.horse_category = Category.objects.create(name="Конный")
        self.walking_category = Category.objects.create(name="Пеший")
        self.tour = Tour.objects.create(
            title="Прогулка у озера",
            description="Маршрут для начинающих.",
            price=Decimal("2500.00"),
            duration_hours=2,
        )
        self.tour.categories.add(self.horse_category, self.walking_category)
        self.start_at = timezone.make_aware(datetime(2030, 6, 15, 10, 0))

    def test_registration_post_creates_user_and_one_to_one_profile(self):
        response = self.client.post(
            reverse("tours:register"),
            {
                "username": "new_rider",
                "email": "new@example.com",
                "phone": "+996555000000",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            },
        )

        self.assertRedirects(response, reverse("tours:tour_list"))
        user = get_user_model().objects.get(username="new_rider")
        self.assertEqual(user.rider_profile.phone, "+996555000000")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("tours:register"),
            {
                "username": "bad_rider",
                "email": "bad@example.com",
                "phone": "",
                "password1": "ComplexPass123!",
                "password2": "DifferentPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("password2", response.context["form"].errors)
        self.assertFalse(get_user_model().objects.filter(username="bad_rider").exists())

    def test_tour_pages_show_tour_and_many_to_many_categories(self):
        response = self.client.get(reverse("tours:tour_list"))
        detail = self.client.get(reverse("tours:tour_detail", args=[self.tour.pk]))

        self.assertContains(response, self.tour.title)
        self.assertContains(detail, "Конный")
        self.assertContains(detail, "Пеший")
        self.assertEqual(self.horse_category.tours.get(), self.tour)

    def test_booking_post_saves_authenticated_user_and_tour(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("tours:booking_create", args=[self.tour.pk]),
            {"start_at": "2030-06-15T10:00"},
        )

        self.assertRedirects(response, reverse("tours:tour_detail", args=[self.tour.pk]))
        booking = Booking.objects.get()
        self.assertEqual(booking.rider, self.user)
        self.assertEqual(booking.tour, self.tour)
        self.assertEqual(booking.start_at, self.start_at)

    def test_booking_post_rejects_second_tour_at_same_datetime(self):
        another_tour = Tour.objects.create(
            title="Поход в горы",
            description="Пеший маршрут.",
            price=Decimal("1500.00"),
            duration_hours=3,
        )
        Booking.objects.create(rider=self.user, tour=self.tour, start_at=self.start_at)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("tours:booking_create", args=[another_tour.pk]),
            {"start_at": "2030-06-15T10:00"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("start_at", response.context["form"].errors)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_post_allows_same_rider_at_a_different_time(self):
        Booking.objects.create(rider=self.user, tour=self.tour, start_at=self.start_at)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("tours:booking_create", args=[self.tour.pk]),
            {"start_at": "2030-06-15T12:00"},
        )

        self.assertRedirects(response, reverse("tours:tour_detail", args=[self.tour.pk]))
        self.assertEqual(Booking.objects.filter(rider=self.user).count(), 2)

    def test_booking_post_requires_login(self):
        response = self.client.post(
            reverse("tours:booking_create", args=[self.tour.pk]),
            {"start_at": "2030-06-15T10:00"},
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('tours:booking_create', args=[self.tour.pk])}",
        )
        self.assertEqual(Booking.objects.count(), 0)

    def test_review_post_saves_review_for_completed_booking(self):
        booking = Booking.objects.create(
            rider=self.user,
            tour=self.tour,
            start_at=self.start_at,
            status=Booking.Status.COMPLETED,
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("tours:review_create"),
            {"booking": booking.pk, "text": "Отличный маршрут!"},
        )

        self.assertRedirects(response, reverse("tours:tour_detail", args=[self.tour.pk]))
        review = Review.objects.get()
        self.assertEqual(review.rider, self.user)
        self.assertEqual(review.tour, self.tour)
        self.assertEqual(review.booking, booking)

    def test_review_post_rejects_tour_not_yet_completed(self):
        booking = Booking.objects.create(
            rider=self.user, tour=self.tour, start_at=self.start_at
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("tours:review_create"),
            {"booking": booking.pk, "text": "Еще не ездил."},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("booking", response.context["form"].errors)
        self.assertEqual(Review.objects.count(), 0)

    def test_rider_can_review_multiple_completed_tours(self):
        another_tour = Tour.objects.create(
            title="Поход в горы",
            description="Пеший маршрут.",
            price=Decimal("1500.00"),
            duration_hours=3,
        )
        first_booking = Booking.objects.create(
            rider=self.user,
            tour=self.tour,
            start_at=self.start_at,
            status=Booking.Status.COMPLETED,
        )
        second_booking = Booking.objects.create(
            rider=self.user,
            tour=another_tour,
            start_at=timezone.make_aware(datetime(2030, 6, 16, 10, 0)),
            status=Booking.Status.COMPLETED,
        )
        self.client.force_login(self.user)

        for booking in (first_booking, second_booking):
            response = self.client.post(
                reverse("tours:review_create"),
                {"booking": booking.pk, "text": f"Отзыв о {booking.tour.title}"},
            )
            self.assertEqual(response.status_code, 302)

        self.assertEqual(Review.objects.filter(rider=self.user).count(), 2)

    def test_review_post_requires_login(self):
        response = self.client.post(
            reverse("tours:review_create"),
            {"booking": 1, "text": "Текст"},
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('tours:review_create')}",
        )
        self.assertEqual(Review.objects.count(), 0)