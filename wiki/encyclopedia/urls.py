from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.get_entry,name="get_entry"),
    path("random",views.random_entry,name='random_entry'),
    path("search",views.search,name="search"),
    path("new_page",views.create_new_page,name="new_page"),
    path("edit/<str:title>",views.edit_page,name='edit_page')
]
