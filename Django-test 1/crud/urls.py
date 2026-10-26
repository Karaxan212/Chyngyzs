from django.urls import path

from crud.views import (
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemListView,
    ItemUpdateView,
)


app_name = "crud"

urlpatterns = [
    path("", ItemListView.as_view(), name="item_list"),
    path("create/", ItemCreateView.as_view(), name="item_create"),
    path("<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("<int:pk>/update/", ItemUpdateView.as_view(), name="item_update"),
    path("<int:pk>/delete/", ItemDeleteView.as_view(), name="item_delete"),
]
