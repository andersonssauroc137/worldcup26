from django.shortcuts import get_object_or_404, render
from .models import Game
from rankings.models import Score


def game_list(request):
    games = Game.objects.filter(is_published=True)

    context = {
        "games": games,
    }

    return render(request, "games/game_list.html", context)


def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug, is_published=True)
    ranking = Score.objects.filter(game=game).select_related("player").order_by("-best_score")[:10]
    other_games = Game.objects.filter(is_published=True).exclude(id=game.id)[:6]

    context = {
        "game": game,
        "ranking": ranking,
        "other_games": other_games,
    }

    return render(request, "games/game_detail.html", context)