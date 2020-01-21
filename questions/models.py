from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def get_absolute_url(self):
        return reverse("tag", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.title

class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='QuestionAuthor')
    title = models.CharField(max_length=500)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    voted_user = models.ManyToManyField(User, related_name='QuestionVote')
    rating = models.IntegerField(default=0)
    new_tag = models.CharField(max_length=50, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def post(self):
        self.creation_date = timezone.now
        self.save()

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='AnswerAuthor')
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    voted_user = models.ManyToManyField(User, related_name='AnswerVote')
    rating = models.IntegerField(default=0)

    def reply(self):
        self.creation_date = timezone.now
        self.save()

class RatingQuestion(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField()
    usage = models.BooleanField(default=0)

    def __str__(self):
        return str(self.author) + ':' + str(self.question) +':' + str(self.value)

    class Meta:
        unique_together = ('author', 'question', 'value')

class RatingAnswer(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.IntegerField()
    usage = models.BooleanField(default=0)
    
    def __str__(self):
        return str(self.author) + ':' + str(self.answer) +':' + str(self.value)

    class Meta:
        unique_together = ('author', 'answer', 'value')
