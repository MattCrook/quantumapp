#!/bin/bash

source venv/bin/activate

python3 manage.py makemigrations
python3 manage.py migrate
