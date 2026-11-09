from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class RiderProfile(models.Model):
    """Дополнительные данные клиента; у пользователя может быть один профиль."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rider_profile",
    )
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"


class Category(models.Model):
    """Вид активности, например конный, пеший или мототур."""

    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tour(models.Model):
    """Предлагаемый маршрут, который может относиться к нескольким категориям."""

    title = models.CharField(max_length=160)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    duration_hours = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField(Category, related_name="tours")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Бронь связывает клиента с туром в заданные дату и время."""

    class Status(models.TextChoices):
        RESERVED = "reserved", "Забронирован"
        COMPLETED = "completed", "Завершен"
        CANCELLED = "cancelled", "Отменен"

    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tour_bookings",
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    start_at = models.DateTimeField()
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.RESERVED,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["rider", "start_at"],
                name="one_booking_per_rider_datetime",
            )
        ]

    def __str__(self):
        return f"{self.rider} — {self.tour} ({self.start_at:%d.%m.%Y %H:%M})"


class Review(models.Model):
    """Отзыв клиента о завершенном туре, оставленный по конкретной брони."""

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="review",
    )
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tour_reviews",
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.booking_id:
            if self.booking.rider_id != self.rider_id:
                raise ValidationError("Отзыв может оставить только владелец брони.")
            if self.booking.tour_id != self.tour_id:
                raise ValidationError("Тур отзыва должен совпадать с туром в брони.")
            if self.booking.status != Booking.Status.COMPLETED:
                raise ValidationError("Оставить отзыв можно только после поездки.")

    def __str__(self):
        return f"Отзыв {self.rider} о туре {self.tour}"