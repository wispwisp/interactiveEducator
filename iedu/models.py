from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __str__(self):
        return self.user.username


class Discipline(models.Model):
    name = models.TextField()
    begin = models.ForeignKey('SlideChain',
                              related_name='first_slide_chain',
                              blank=True, null=True,
                              on_delete=models.SET_NULL)
    def __str__(self):
        return self.name


class SlideChain(models.Model):
    discipline = models.ForeignKey(Discipline)
    name = models.TextField()
    passingPercent = models.SmallIntegerField(default=70)

    nextChain = models.ForeignKey('self',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    additionalChain = models.ForeignKey('self',
                                        related_name='additional',
                                        blank=True, null=True,
                                        on_delete=models.SET_NULL)

    def getSlide(self, idx):
        if idx > self.slide_set.count():
            return None
        return self.slide_set.get(index = idx)

    def countSlidesWithoutQuestions(self):
        return self.slide_set.exclude(question__isnull=True).count()

    def __str__(self):
        return self.name


# User education progress states:


class UserStatePerDiscipline(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    discipline = models.ForeignKey(Discipline)
    index = models.SmallIntegerField(default=0)
    currentSlideChain = models.ForeignKey(SlideChain)

    def getSlide(self):
        return self.currentSlideChain.getSlide(self.index)

    def prepareNextSlide(self):
        self.index += 1

    def rollBackToFirstSlide(self):
        self.index = 0

    def hasMoreSlides(self):
        return self.index < (self.currentSlideChain.slide_set.count() - 1)

    def switchChain(self, userChainState):
        if userChainState.needAdditionalSlideChain():
            if userChainState.triggered == 2:
                if self.currentSlideChain.additionalChain:
                    self.currentSlideChain = self.currentSlideChain.additionalChain
        else:
            if self.currentSlideChain.nextChain:
                self.currentSlideChain = self.currentSlideChain.nextChain
        self.rollBackToFirstSlide()


class UserChainState(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    slideChain = models.ForeignKey(SlideChain)

    numberOfCorrect = models.SmallIntegerField(default=0)
    triggered = models.SmallIntegerField(default=0)

    def needAdditionalSlideChain(self):
        N = self.slideChain.countSlidesWithoutQuestions()
        if N == 0:
            return False
        else:
            return (self.numberOfCorrect / N) < (self.slideChain.passingPercent / 100)


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
    chain = models.ForeignKey('SlideChain')
    index = models.SmallIntegerField(default=0)

    headword = models.TextField()
    text = models.TextField()
    question = models.ForeignKey(Question, blank=True, null=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return "[" + str(self.index) + "] " + self.chain.name + ": " + self.headword
