from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("auction/<int:item_id>",views.auction,name="auction"),
    path("comment/<int:item_id>",views.comment,name="comment"),
    path("categories",views.categories,name="categories"),
    path("add_watchlist/<int:item_id>",views.add_watchlist,name="add_watchlist"),
    path("delete_watchlist/<int:item_id>",views.delete_watchlist,name="delete_watchlist"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("close_the_bid<int:item_id>",views.close_the_bid,name="close_the_bid"),
    path("add_like/<int:comment_id>/<int:item_id>",views.add_like,name="add_like"),
    path("remove_like/<int:comment_id>/<int:item_id>",views.remove_like,name="remove_like"),
]
