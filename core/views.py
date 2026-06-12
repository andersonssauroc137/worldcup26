from django.shortcuts import render
from games.models import Game
from rankings.models import Score


def home(request):
    featured_games = Game.objects.filter(is_published=True)[:6]
    top_scores = Score.objects.select_related("player", "game").order_by("-best_score")[:10]

    context = {
        "featured_games": featured_games,
        "top_scores": top_scores,
    }

    return render(request, "core/home.html", context)