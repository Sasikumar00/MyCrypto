from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("about/", aboutPage, name='home'),
    path("watchlist/", wishlistPage, name='home'),
    path("pricing/", pricingPage, name='home'),
    # path("coins", coins, name='coins'),
    path("coins/<str:coin>/USD", chart, name='home'),
    path("add-to-watchlist/", addToWatchlist, name='add-to-watch'),
    path("get-watchlist/", getWatchlist, name='get-watch'),
    path("delete-watch/", deleteWatch, name='get-watch'),
]
