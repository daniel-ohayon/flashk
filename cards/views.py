from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Card, Score

from random import choice


class IndexView(generic.ListView):
    template_name = 'cards/index.html'
    context_object_name = 'latest_cards'

    def get_queryset(self):
        return Card.objects.order_by('-creation_date')[:3]


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
