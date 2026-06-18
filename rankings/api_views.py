import json

from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from players.models import Player
from games.models import Game
from rankings.models import Score


@csrf_exempt
def register_player(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        nickname = data.get("nickname", "").strip()

        if not nickname:
            return JsonResponse({"success": False, "error": "Nickname is required"}, status=400)

        if len(nickname) > 40:
            nickname = nickname[:40]

        player = Player.objects.create(nickname=nickname)

        return JsonResponse({
            "success": True,
            "player_id": str(player.public_id),
            "nickname": player.nickname,
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def submit_score(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)

        player_id = data.get("player_id")
        game_slug = data.get("game_slug")
        score_value = int(data.get("score", 0))

        if score_value < 0:
            score_value = 0

        player = Player.objects.get(public_id=player_id)
        game = Game.objects.get(slug=game_slug, is_published=True)

        score_obj, created = Score.objects.get_or_create(
            player=player,
            game=game,
            defaults={
                "best_score": score_value,
                "last_score": score_value,
                "attempts": 1,
            }
        )

        is_new_record = False

        if not created:
            score_obj.last_score = score_value
            score_obj.attempts += 1

            if score_value > score_obj.best_score:
                score_obj.best_score = score_value
                is_new_record = True

            score_obj.save()
        else:
            is_new_record = True

        return JsonResponse({
            "success": True,
            "game": game.title,
            "nickname": player.nickname,
            "best_score": score_obj.best_score,
            "last_score": score_obj.last_score,
            "attempts": score_obj.attempts,
            "is_new_record": is_new_record,
        })

    except Player.DoesNotExist:
        return JsonResponse({"success": False, "error": "Player not found"}, status=404)

    except Game.DoesNotExist:
        return JsonResponse({"success": False, "error": "Game not found"}, status=404)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def game_ranking_api(request, slug):
    try:
        game = Game.objects.get(slug=slug, is_published=True)

        ranking = Score.objects.filter(game=game).select_related("player").order_by("-best_score")[:20]

        data = [
            {
                "position": index + 1,
                "nickname": score.player.nickname,
                "score": score.best_score,
                "attempts": score.attempts,
            }
            for index, score in enumerate(ranking)
        ]

        return JsonResponse({
            "success": True,
            "game": game.title,
            "ranking": data,
        })

    except Game.DoesNotExist:
        return JsonResponse({"success": False, "error": "Game not found"}, status=404)


def global_ranking_api(request):
    ranking = (
        Score.objects
        .values("player__nickname")
        .annotate(total_score=Sum("best_score"))
        .order_by("-total_score")[:20]
    )

    data = [
        {
            "position": index + 1,
            "nickname": item["player__nickname"],
            "score": item["total_score"],
        }
        for index, item in enumerate(ranking)
    ]

    return JsonResponse({
        "success": True,
        "ranking": data,
    })