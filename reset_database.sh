#!/usr/bin/env bash
python manage.py flush
python manage.py loadcsv data/anki_output.csv
python manage.py loadcsv data/keep_output.csv
