from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create",views.CreatePage,name="create"),
    path("edit",views.EditPage,name="edit"),
    path("random",views.RandomPage,name="random")
]
