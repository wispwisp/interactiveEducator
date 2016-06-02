from django.db import models
from django.contrib.auth.models import User


class SlideChain(models.Model):
    name = models.TextField()
    passingPercent = models.SmallIntegerField(default=70)
    slide = models.ForeignKey('Slide')
    nextChain = models.ForeignKey('self',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    addtitionalChain = models.ForeignKey('self',
                                         related_name='additional',
                                         blank=True, null=True,
                                         on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


#class SlideChainTriggered(models.Model):
#    userProfile = models.ForeignKey('UserProfile')
#    slideChain = models.ForeignKey('SlideChain')
#    count = models.SmallIntegerField(default=0)


class Discipline(models.Model):
    name = models.TextField()
    begin = models.ForeignKey('SlideChain')

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
    currentSlide = models.ForeignKey('Slide',
                                     #related_name='current_slide',
                                     blank=True, null=True,
                                     on_delete=models.SET_NULL)


# Slide internals:


class Question(models.Model):
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
