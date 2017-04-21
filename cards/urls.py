from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^stats/$', views.cards_stats),
    url(r'^(?P<card_id>[0-9]+)/$', views.question),
    url(r'^review/$', views.review),
    url(r'^review/next/$', views.get_cards),
    url(r'^(?P<card_id>[0-9]+)/score/$', views.post_score),
    url(r'^list/(?P<option>\w+)/$', views.cards_list)
]