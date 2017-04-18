import re
import csv

from django.core.management.base import BaseCommand
from cards.models import Card

# use `python manage.py flush` to clear database


def remove_tags(raw_html):
    # replace div tags by newline
    raw_html = raw_html.replace('<div>', '\n')
    raw_html = raw_html.replace('&nbsp;', ' ')
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


class Command(BaseCommand):
    help = 'Import questions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    def handle(self, *args, **options):
        with open(options['csv_file'], 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for i, row in enumerate(reader, 1):
                self.stdout.write("Processing row %d..." % i)
                row = [remove_tags(e) for e in row]
                card = Card()
                card.question = row[1]
                card.answer = row[0]
                card.save()
