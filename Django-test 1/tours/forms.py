from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from tours.models import Booking, Review, Tour


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")
    phone = forms.CharField(max_length=30, required=False, label="Телефон")

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "phone")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            from tours.models import RiderProfile

            RiderProfile.objects.create(user=user, phone=self.cleaned_data["phone"])
        return user


class BookingForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        label="Дата и время",
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Booking
        fields = ("start_at",)

    def __init__(self, *args, rider, tour, **kwargs):
        self.rider = rider
        self.tour = tour
        super().__init__(*args, **kwargs)

    def clean_start_at(self):
        start_at = self.cleaned_data["start_at"]
        if Booking.objects.filter(rider=self.rider, start_at=start_at).exists():
            raise forms.ValidationError(
                "У вас уже есть тур, забронированный на это время."
            )
        return start_at

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.rider = self.rider
        booking.tour = self.tour
        if commit:
            booking.save()
        return booking


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("booking", "text")
        labels = {"booking": "Завершенная поездка", "text": "Ваш отзыв"}
        widgets = {"text": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, rider, **kwargs):
        super().__init__(*args, **kwargs)
        self.rider = rider
        self.fields["booking"].queryset = (
            Booking.objects.filter(
                rider=rider,
                status=Booking.Status.COMPLETED,
                review__isnull=True,
            )
            .select_related("tour")
            .order_by("-start_at")
        )

    def _post_clean(self):
        booking = self.cleaned_data.get("booking")
        if booking:
            self.instance.rider = self.rider
            self.instance.tour = booking.tour
        super()._post_clean()

    def save(self, commit=True):
        review = super().save(commit=False)
        review.rider = self.rider
        review.tour = review.booking.tour
        if commit:
            review.save()
        return review