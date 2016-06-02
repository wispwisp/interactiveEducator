from iedu.models import Slide, UserProfile


def grouped(iterable, n):
    """s ->
    (s0,s1,s2,...sn-1),
    (sn,sn+1,sn+2,...s2n-1),
    (s2n,s2n+1,s2n+2,...s3n-1), ...
    """
    return zip(*[iter(iterable)] * n)


def createSlideContext(discipline, slide):
    return {
        'discipline': discipline,
        'headword': slide.headword,
        'text': slide.text,
        'question': slide.question,
    }
