import logging
from datetime import datetime
from random import randint
from math import floor
from django.core.management import BaseCommand
from app.models import *

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = "insert generated data to database"

    def add_arguments(self, parser):
        parser.add_argument(
            'ratio', type=int
        )

    def handle(self, *args, **options):
        profile_size = tag_size = size = options.get("ratio", 10000)
        question_size = size * 10
        answer_size = size * 100
        like_size = size * 200
        self.fill_users(profile_size)
        self.fill_profiles(profile_size)
        self.fill_likes(like_size)
        self.fill_tags(tag_size)
        self.fill_questions(question_size, profile_size, like_size, tag_size)
        self.fill_answers(profile_size, like_size)

    def bulk_create(self,manager,objects):
        size = len(objects)
        if (size <= 10000):
            manager.bulk_create(objects)
        else:
            offset = 0
            limit = 10000
            for i in range(floor(size / 10000)):
                manager.bulk_create(objects[offset:limit])
                offset = limit
                limit += 10000
            last_objects = objects[offset:-1]
            if len(last_objects) != 0:
                manager.bulk_create(last_objects)

    def fill_users(self, profile_size):
        users = []
        for i in range(profile_size):
            users.append(User(
                username=f'username {i + 1}',
                email=f'email@{i + 1}.com',
                password=f'password {i + 1}'
            ))
        self.bulk_create(User.objects,users)
    def fill_profiles(self, profile_size):
        profiles = []
        users = User.objects.all().order_by('id')
        i = 1
        for u in users:
            profiles.append(Profile(
                user_id=u.id,
                nick_name=f'nickname {i}'
            ))
            i += 1
        self.bulk_create(Profile.objects,profiles)


    def fill_likes(self, like_size):
        likes = []
        for i in range(like_size):
            _like = randint(0, 1000)
            _dislike = randint(0, 500)
            likes.append(Like(
                like=_like,
                dislike=_dislike,
                rating=_like - _dislike
            ))
        self.bulk_create(Like.objects,likes)

    def fill_tags(self, tag_size):
        tags = []
        for i in range(tag_size):
            tags.append(Tag(
                id=i + 1,
                name=f'tags {i + 1}'
            ))
        self.bulk_create(Tag.objects,tags)

    def fill_questions(self, question_size, profile_size, like_size, tag_size):
        questions = []
        for i in range(question_size):
            questions.append(Question(
                profile_id=randint(1, profile_size),
                title=f' question title {i + 1}',
                content=f'question content {i + 1}',
                published_date=datetime.today(),
                like_id=randint(1, like_size),
                count_answers=randint(0, 21)
            ))
        self.bulk_create(Question.objects,questions)
        for q in Question.objects.all():
            for _ in range(randint(0, 12)):
                tag = Tag.objects.get(pk=randint(1, tag_size))
                tag.questions.add(q)

    def fill_answers(self, profile_size, like_size):
        answers = []
        content = 1
        for q in Question.objects.all():
            for i in range(q.count_answers):
                answers.append(Answer(
                    profile_id=randint(1, profile_size),
                    content=f"Answer content {content}",
                    question=q,
                    is_correct=randint(0, 1),
                    published_date=datetime.today(),
                    like_id=randint(1, like_size)
                ))
                content += 1
        self.bulk_create(Answer.objects,answers)
