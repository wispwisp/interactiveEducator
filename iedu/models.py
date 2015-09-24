from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    currentSlide = models.ForeignKey('Slide',
                                     related_name='current_slide',
                                     blank=True, null=True,
                                     on_delete=models.SET_NULL)
    nextSlide = models.ForeignKey('Slide',
                                  related_name='next_slide',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username


class Theme(models.Model):
    theme = models.TextField()

    def __str__(self):
        return self.theme


class Question(models.Model):
    theme = models.ForeignKey(Theme)
    text = models.TextField()

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question)
    text = models.TextField()
    isCorrect = models.BooleanField(default=False)


class Slide(models.Model):
    headword = models.TextField()
    text = models.TextField()
    question = models.ForeignKey(Question, blank=True, null=True,
                                 on_delete=models.SET_NULL)
    nextSlide = models.ForeignKey('self', blank=True, null=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return self.headword


class AdditionalSlide(Slide):
    theme = models.ForeignKey(Theme)
    difficultyLevel = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.theme.theme


class Progress(models.Model):
    user = models.ForeignKey(UserProfile)
    theme = models.ForeignKey(Theme)
    score = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.theme.theme + ": " + str(self.score)
