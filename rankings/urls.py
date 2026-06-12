from django.urls import path
from . import views

app_name = "rankings"

urlpatterns = [
    path("", views.global_ranking, name="global_ranking"),
    path("<slug:slug>/", views.game_ranking, name="game_ranking"),
]