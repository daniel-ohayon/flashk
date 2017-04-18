from django.db.models import Count, Avg
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Card, Score

from random import choice


def stats(request):
    graded_cards = Card.objects.annotate(grade=Avg('score__value'))
    data = {
        'total': Card.objects.count(),
        'new': Card.objects.annotate(num_scores=Count('score')).filter(num_scores=0).count(),
        'poor': graded_cards.filter(grade__lte=1.5).count(),
        'average': graded_cards.filter(grade__gt=1.5).filter(grade__lte=2.5).count(),
        'good': graded_cards.filter(grade__gt=2.5).count()
    }

    return render(request, 'cards/index.html', data)


@ensure_csrf_cookie
def question(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    return render(request, 'cards/card.html', {'card': card})


def pick_question(request):
    # TODO implement choice based on scores
    card = choice(Card.objects.all())
    # TODO is this the right way? it feels like URLs shouldn't be hardcoded here
    return HttpResponseRedirect('/cards/%d' % card.id)


def post_score(request, card_id):
    score = request.POST['score']
    card = get_object_or_404(Card, pk=card_id)
    score = Score(card=card, value=score)
    score.save()
    return HttpResponse('success!')
