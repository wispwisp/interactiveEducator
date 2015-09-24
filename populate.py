import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interactiveEducator.settings')

import django
django.setup()

from iedu.models import Slide, Question, Choice, Theme


def populate():

    ps = None
    for i in range(1,20):
        t = Theme(
            theme='theme ' + str(i),
        )
        t.save()

        q = Question(
            theme=t,
            text='question? ' + str(i),
        )
        q.save()

        c = Choice(
            question=q,
            text='option1',
            isCorrect=False,
        )
        c.save()
        c = Choice(
            question=q,
            text='option2',
            isCorrect=True,
        )
        c.save()

        s = Slide(
            headword='headword ' + str(i),
            text='text ' + str(i),
            question=Question.objects.get(id=q.id),
        )
        s.save()
        if ps:
            ps.nextSlide = s
            ps.save()
        ps = s
        
        print("- {0}".format(str(s)), ", id: ", s.id)

    lslide = Slide.objects.last()
    fslide = Slide.objects.first()
    lslide.nextSlide = fslide
    lslide.save()

if __name__ == '__main__':
    print("Starting population script...")
    populate()
