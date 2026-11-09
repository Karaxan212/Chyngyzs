from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from tours.forms import BookingForm, RegistrationForm, ReviewForm
from tours.models import Tour


def tour_list(request):
    tours = Tour.objects.filter(is_active=True).prefetch_related("categories")
    return render(request, "tours/tour_list.html", {"tours": tours})


def tour_detail(request, pk):
    tour = get_object_or_404(
        Tour.objects.prefetch_related("categories", "reviews__rider"),
        pk=pk,
        is_active=True,
    )
    return render(request, "tours/tour_detail.html", {"tour": tour})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
            login(request, user)
            return redirect("tours:tour_list")
    else:
        form = RegistrationForm()
    return render(request, "tours/form.html", {"form": form, "title": "Регистрация"})


@login_required
def book_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk, is_active=True)
    if request.method == "POST":
        form = BookingForm(request.POST, rider=request.user, tour=tour)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                form.add_error(
                    "start_at", "У вас уже есть тур, забронированный на это время."
                )
            else:
                messages.success(request, "Тур успешно забронирован.")
                return redirect("tours:tour_detail", pk=tour.pk)
    else:
        form = BookingForm(rider=request.user, tour=tour)
    return render(
        request,
        "tours/form.html",
        {"form": form, "title": f"Бронирование: {tour.title}"},
    )


@login_required
def leave_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, rider=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Спасибо за ваш отзыв.")
            return redirect("tours:tour_detail", pk=form.instance.tour_id)
    else:
        form = ReviewForm(rider=request.user)
    return render(
        request,
        "tours/form.html",
        {"form": form, "title": "Оставить отзыв"},
    )