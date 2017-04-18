from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.stats, name='index'),
    url(r'^(?P<card_id>[0-9]+)/$', views.question, name='question'),
    url(r'^random/$', views.pick_question, name='random_question'),
    url(r'^(?P<card_id>[0-9]+)/score/$', views.post_score, name='score')
]