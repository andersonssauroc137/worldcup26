from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from games.models import Game
from .models import Score


def global_ranking(request):
    ranking = (
        Score.objects
        .values("player__nickname")
        .annotate(total_score=Sum("best_score"))
        .order_by("-total_score")[:50]
    )

    context = {
        "ranking": ranking,
    }

    return render(request, "rankings/global_ranking.html", context)


def game_ranking(request, slug):
    game = get_object_or_404(Game, slug=slug, is_published=True)
    ranking = Score.objects.filter(game=game).select_related("player").order_by("-best_score")[:50]

    context = {
        "game": game,
        "ranking": ranking,
    }

    return render(request, "rankings/game_ranking.html", context)