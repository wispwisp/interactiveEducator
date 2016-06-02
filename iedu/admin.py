from django.contrib import admin
from iedu.models import Slide, Question, Choice, Theme, Discipline, SlideChain


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
admin.site.register(Question, QuestionAdmin)


admin.site.register(Discipline)
admin.site.register(Slide)
admin.site.register(SlideChain)
admin.site.register(Theme)
