def isNeedAddtitional(l, significent_range=5):
    """Не вычисляет последние два"""
    num_of_additional = None
    for i in range(0, len(l)-1, 2):
        r = l[i+1] - l[i]
        if r >= significent_range:
            num_of_additional = i-1
            return num_of_additional
    return num_of_additional


def createSlide(slide):
    return {
        'headword': slide.headword,
        'text': slide.text,
        'question': slide.question,
        'button_value': 'Принять'
    }
