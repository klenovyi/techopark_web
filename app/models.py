import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import *

logging.basicConfig(level=logging.INFO)


# Create your models here.

class QuestionManager(models.Manager):

    def filter_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)

    ## будем считать горячими вопросами  с более 300 лайков и 7 ответов, отсортируем по лайкам , далее ответам
    def filter_by_hot(self):
        return self.filter(like__rating__gt=300, count_answers__gt=7).order_by("-like__rating", "-count_answers")


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


class AnswerManager(models.Manager):
    def filter_by_question(self, question_id):
        return self.filter(question__id=question_id)


class Answer(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name="answers")
    content = models.TextField()
    is_correct = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    published_date = models.DateTimeField()
    like = models.ForeignKey('Like', on_delete=models.PROTECT)
    objects = AnswerManager()


class ProfileManager(models.Manager):
    def best_members(self):
        logging.info('before sql')
        profiles = Question.objects.values('profile').annotate(rating=Sum('like__rating')).order_by('-rating')[0:10]
        ids = list(map(lambda p: p['profile'], profiles))
        return self.filter(id__in=ids)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to="uploads/", null=True, blank=True)
    nick_name = models.CharField(max_length=128)
    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):

    def best_tags(self):
        tags =  Question.objects.values('tags').annotate(Count('id')).order_by('-id__count')[0:10]
        ids = list(map(lambda  t: t['tags'],tags))
        logging.info(ids)
        return Tag.objects.filter(id__in=ids)


class Tag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()

    def __str__(self):
        return self.name


class Like(models.Model):
    like = models.IntegerField()
    dislike = models.IntegerField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return str(self.rating)
