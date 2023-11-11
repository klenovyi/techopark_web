from datetime import datetime
from random import randint

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class QuestionManager(models.Manager):
    def filter_by_question(self,question_id):
        return self.filter(id=question_id).first()
    def filter_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)

    ## будем считать горячими вопросами  с более 300 лайков и 7 ответов, отсортируем по лайкам , далее ответам
    def filter_by_hot(self):
        self.filter(like__like__gt=300, count_answers__gt=7)
        return self.order_by("-like__like", "-count_answers")

    def first_fill_db(self, question_size, profile_size, like_size, tag_size):
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
        self.bulk_create(questions)
        for q in Question.objects.all():
            for _ in range(randint(0, 12)):
                tag = Tag.objects.get(pk=randint(1, tag_size))
                tag.questions.add(q)

class AnswerManager(models.Manager):
    def filter_by_question(self, question_id):
        return self.filter(question__id=question_id)

    def first_fill_db(self, profile_size, like_size, question_size):
        answers = []
        for q in Question.objects.all():
            content = 1
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
        self.bulk_create(answers)


class ProfileManager(models.Manager):
    def first_fill_db(self, profile_size):
        profiles = []
        for i in range(profile_size):
            u = User.objects.create_user(
                username=f'username {i + 1}',
                email=f'email@{i + 1}.com',
                password=f'password {i + 1}'
            )
            profiles.append(Profile(
                user=u,
                nick_name=f'nickname {i + 1}'
            ))
        self.bulk_create(profiles)


class TagManager(models.Manager):
    def first_fill_db(self, tag_size):
        tags = []
        for i in range(tag_size):
            tags.append(Tag(
                id=i + 1,
                name=f'tags {i + 1}'
            ))
        self.bulk_create(tags)


class LikeManager(models.Manager):
    def first_fill_db(self, like_size):
        likes = []
        for _ in range(like_size):
            likes.append(Like(
                like=randint(0, 1000),
                dislike=randint(0, 500)
            ))
        self.bulk_create(likes)


class Question(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name="questions")
    title = models.CharField(max_length=128)
    content = models.TextField()
    published_date = models.DateTimeField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    tags = models.ManyToManyField("Tag", related_name="questions")
    like = models.ForeignKey('Like', on_delete=models.PROTECT)
    count_answers = models.IntegerField(default=0)
    objects = QuestionManager()

    class Meta:
        ordering = ['-published_date']


class Answer(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name="answers")
    content = models.TextField()
    is_correct = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    published_date = models.DateTimeField()
    like = models.ForeignKey('Like', on_delete=models.PROTECT)
    objects = AnswerManager()


class Tag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()


class Like(models.Model):
    like = models.IntegerField()
    dislike = models.IntegerField()
    objects = LikeManager()

    def __str__(self):
        return str(self.like - self.dislike)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to="uploads/", null=True, blank=True)
    nick_name = models.CharField(max_length=128)
    objects = ProfileManager()
