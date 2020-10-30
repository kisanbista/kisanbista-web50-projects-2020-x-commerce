from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create_product, name = "create_product"),
    path("active",views.active_listings, name = "active_listings"),
    path("closed",views.closed_listings, name = "closed_listings"),
    path("watchlist/<int:product_id>",views.watchlist,name = "watchlist"),
    path("listpage/<int:product_id>",views.listpage, name = "listpage"),
    path("viewWatchlist",views.viewWatchlist, name = "viewWatchlist"),
    path("removeWatchlist/<int:product_id>",views.removeWatchlist,name = "removeWatchlist"),
    path("bidPrice/<int:product_id>",views.bidPrice, name = "bidPrice"),
    path("closeBid/<int:product_id>",views.closeBid,name = "closeBid"),
    path("categories/<int:category_id>",views.categories, name = "categories"),
    path("comments/<int:product_id>",views.comments, name = "comments"),

]
