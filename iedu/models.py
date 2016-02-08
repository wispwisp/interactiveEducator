from django.db import models
from django.contrib.auth.models import User


class Discipline(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __str__(self):
        return self.user.username


# User education progress states:


class UserSlideStatePerDiscipline(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    discipline = models.ForeignKey(Discipline)
    # session slide - setup additional/prime slide
    currentSlide = models.ForeignKey('Slide',
                                     #related_name='current_slide',
                                     blank=True, null=True,
                                     on_delete=models.SET_NULL)


class UserAdditionalSlideStatePerTheme(models.Model):
    slideState = models.ForeignKey(UserSlideStatePerDiscipline)
    theme = models.ForeignKey('Theme')
    currentAdditionalSlide = models.ForeignKey('Slide',
                                               blank=True, null=True,
                                               on_delete=models.SET_NULL)


# Slide internals:


class Theme(models.Model):
    discipline = models.ForeignKey(Discipline)
    name = models.TextField()

    def __str__(self):
        return self.name


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
        return "[" + self.theme.name + "]: " + self.headword


class UserThemeScore(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    theme = models.ForeignKey(Theme)
    score = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.theme.name + ": " + str(self.score)
