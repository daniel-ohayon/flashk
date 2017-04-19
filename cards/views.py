from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Card, Score

from random import sample


def home_page(request):
    graded_cards = Card.objects.annotate(grade=Avg('score__value'))
    data = {
        'total': Card.objects.count(),
        'new': Card.objects.annotate(num_scores=Count('score')).filter(num_scores=0).count(),
        'poor': graded_cards.filter(grade__gt=2.5).count(),
        'average': graded_cards.filter(grade__gt=1.5).filter(grade__lte=2.5).count(),
        'good': graded_cards.filter(grade__lte=1.5).count()
    }

    return render(request, 'cards/index.html', data)


def cards_list(request, option):
    query_set = Card.objects.annotate(grade=Avg('score__value'), num_scores=Count('score'))
    if option == 'new':
        query_set = query_set.filter(num_scores=0)
    elif option == 'good':
        query_set = query_set.filter(grade__lte=1.5)
    elif option == 'poor':
        query_set = query_set.filter(grade__gt=2.5)
    return render(request, 'cards/list.html', {'cards': query_set})


@ensure_csrf_cookie
def question(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    return render(request, 'cards/card.html', {'card': card})


@ensure_csrf_cookie
def review(request):
    return render(request, 'cards/card.html')


def get_cards(request):
    # TODO implement choice based on scores?
    cards = sample(Card.objects.all(), 10)
    cards_json = [{'question': c.question, 'answer': c.answer, 'id': c.id} for c in cards]
    return JsonResponse({'output': cards_json})


def post_score(request, card_id):
    score = request.POST['score']
    card = get_object_or_404(Card, pk=card_id)
    score = Score(card=card, value=score)
    score.save()
    return HttpResponse('success!')
