from django.contrib import admin

from tours.models import Booking, Category, Review, RiderProfile, Tour


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "duration_hours", "is_active")
    list_filter = ("is_active", "categories")
    search_fields = ("title", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("tour", "rider", "start_at", "status")
    list_filter = ("status", "tour")
    search_fields = ("rider__username", "tour__title")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("tour", "rider", "created_at")
    search_fields = ("tour__title", "rider__username", "text")


admin.site.register(RiderProfile)