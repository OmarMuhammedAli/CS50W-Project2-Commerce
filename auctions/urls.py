from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create_listing, name='create_listing'), 
    path('watchlist', views.watchlist, name='watchlist'),
    path('categories', views.categories, name='categories'),
    path('categories/<int:category_id>', views.category_listings, name='category_listings'),
    path('<int:listing_id>', views.listing_page, name='listing_page'),
    path('<int:listing_id>/toggle_watchlist', views.toggle_watchlist, name='toggle_watchlist'),
    path('<int:listing_id>/add_bid', views.add_bid, name='add_bid'),
    path('<int:listing_id>/close', views.close_auction, name='close'),
    path('<int:listing_id>/comment', views.add_comment, name='comment')
]
