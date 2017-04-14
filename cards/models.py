# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Card(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s / %s' % (self.question, self.answer)


class Score(models.Model):
    card = models.ForeignKey(Card)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s -> %d' % (self.card.question, self.value)
