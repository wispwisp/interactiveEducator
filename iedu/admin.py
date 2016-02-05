from django.contrib import admin
from iedu.models import Slide, Question, Choice, Theme, AdditionalSlide


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
admin.site.register(Question, QuestionAdmin)


admin.site.register(Slide)
admin.site.register(AdditionalSlide)
admin.site.register(Theme)
