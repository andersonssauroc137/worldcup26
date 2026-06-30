from django.urls import path
from . import api_views

app_name = "rankings_api"

urlpatterns = [
    path("player/register/", api_views.register_player, name="register_player"),
    path("score/submit/", api_views.submit_score, name="submit_score"),
    path("ranking/global/", api_views.global_ranking_api, name="global_ranking_api"),
    path("ranking/<slug:slug>/", api_views.game_ranking_api, name="game_ranking_api"),
]