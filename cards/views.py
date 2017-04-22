from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Card, Score

from random import sample
from datetime import datetime, timedelta


class Grade(object):
    NEW = 'new'
    POOR = 'poor'
    AVERAGE = 'average'
    GOOD = 'good'


def filter_by_grade(query_set, card_type):
    if card_type == Grade.NEW:
        return
    elif card_type == Grade.POOR:
        return query_set.filter(grade__gt=2.5)
    elif card_type == Grade.AVERAGE:
        return query_set.filter(grade__gt=1.5).filter(grade__lte=2.5)
    elif card_type == Grade.GOOD:
        return query_set.filter(grade__lte=1.5)


def get_cards_before(date=datetime.today()):
    return Score.objects.filter(date__lt=date).values('card').annotate(grade=Avg('value'))


def cards_stats(request):

    graded_cards = Card.objects.annotate(grade=Avg('score__value'))
    present_data = [
        ['Grade', 'Count'],
        ['New', Card.objects.annotate(num_scores=Count('score')).filter(num_scores=0).count()],
        ['Poor', filter_by_grade(graded_cards, Grade.POOR).count()],
        ['Average', filter_by_grade(graded_cards, Grade.AVERAGE).count()],
        ['Good', filter_by_grade(graded_cards, Grade.GOOD).count()]
    ]

    past_data = [['Date', 'Poor', 'Average', 'Good']]
    for n in range(1, 7):
        date = datetime.today() - timedelta(days=n)
        cards = get_cards_before(date)
        past_data.append([
            str(date).split()[0],
            filter_by_grade(cards, Grade.POOR).count(),
            filter_by_grade(cards, Grade.AVERAGE).count(),
            filter_by_grade(cards, Grade.GOOD).count()
        ])

    return JsonResponse({'current-data': present_data, 'past-data': past_data})


def home_page(request):
    return render(request, 'cards/index.html')


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
