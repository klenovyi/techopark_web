from datetime import datetime
from random import randint

from django.core.management import BaseCommand

from app.models import *


class Command(BaseCommand):
    help = "insert generated data to database"

    def add_arguments(self, parser):
        parser.add_argument(
            'ratio', type=int
        )

    def handle(self, *args, **options):
        profile_size = tag_size = size = options.get("ratio", 10)
        question_size = size * 10
        answer_size = size * 100
        like_size = size * 200
        Profile.objects.first_fill_db(profile_size)
        Like.objects.first_fill_db(like_size)
        Tag.objects.first_fill_db(tag_size)
        Question.objects.first_fill_db(question_size,profile_size,like_size,tag_size)
        Answer.objects.first_fill_db(profile_size,like_size,question_size)
