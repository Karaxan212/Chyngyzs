from django.urls import path

from tours import views


app_name = "tours"

urlpatterns = [
    path("", views.tour_list, name="tour_list"),
    path("register/", views.register, name="register"),
    path("review/", views.leave_review, name="review_create"),
    path("<int:pk>/", views.tour_detail, name="tour_detail"),
    path("<int:pk>/book/", views.book_tour, name="booking_create"),
]