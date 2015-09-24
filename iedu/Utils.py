from iedu.models import Slide, UserProfile, Progress, AdditionalSlide


def grouped(iterable, n):
    """s ->
    (s0,s1,s2,...sn-1),
    (sn,sn+1,sn+2,...s2n-1),
    (s2n,s2n+1,s2n+2,...s3n-1), ...
    """
    return zip(*[iter(iterable)] * n)


def checkProgress(themesProgress, significentRange=5):
    "return is need additional slide by theme and theme"
    def isSignificantRange(f,s):
        return f > s and f - s >= significentRange

    for f, s in grouped(themesProgress.reverse(), 2):
        if isSignificantRange(f.score, s.score):
            return (s, True)

    return (None, False)


def additionalSlide(theme):
    print('need additional slide, by theme: ', theme)
    slides = AdditionalSlide.objects.filter(theme=theme)
    if slides:
        print(slides)
        # TODO: select slide by it difficult level
        return (slides.first(), True)
    else:
        print('nope')
        return (None, False)


def createSlide(slide):
    return {
        'headword': slide.headword,
        'text': slide.text,
        'question': slide.question,
        'button_value': 'Принять'
    }
