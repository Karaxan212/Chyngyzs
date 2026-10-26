from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crud.models import Item


class ItemListView(ListView):
    model = Item
    template_name = "crud/item_list.html"
    context_object_name = "items"


class ItemDetailView(DetailView):
    model = Item
    template_name = "crud/item_detail.html"
    context_object_name = "item"


class ItemCreateView(CreateView):
    model = Item
    fields = ("title", "description")
    template_name = "crud/item_form.html"
    success_url = reverse_lazy("crud:item_list")


class ItemUpdateView(UpdateView):
    model = Item
    fields = ("title", "description")
    template_name = "crud/item_form.html"
    success_url = reverse_lazy("crud:item_list")


class ItemDeleteView(DeleteView):
    model = Item
    template_name = "crud/item_confirm_delete.html"
    success_url = reverse_lazy("crud:item_list")
