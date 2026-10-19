from django.urls import path

from blog.views import BlogDetailView, BlogListView


app_name = "blog"

urlpatterns = [
    path("", BlogListView.as_view(), name="blog_list"),
    path("blogs/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
]
