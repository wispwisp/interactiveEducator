from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages

from iedu.forms import UserForm, UserProfileForm
from iedu.models import Slide, UserProfile, Choice, Discipline, UserSlideStatePerDiscipline, UserSlideChainState

from iedu import Utils


def index(request):
    return render(request,
                  'iedu/index.html',
                  {'disciplines':Discipline.objects.all()})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Спасибо за регистрацию!')
            return HttpResponseRedirect(reverse('iedu:index'))
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'iedu/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
            else:
                messages.error(request, 'Ваша учетная запись отключена.')
        else:
            messages.error(request, 'Неверные регистрационные данные.')
        return HttpResponseRedirect(reverse('iedu:index'))
    else:
        raise Http404


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('iedu:index'))


@login_required
def slide(request, disciplineName):
    userProfile = request.user.userprofile
    discipline = Discipline.objects.get(name=disciplineName) # Get ot Http404

    # slide state per descipline:
    slideState, slideStateCreated = UserSlideStatePerDiscipline.objects.get_or_create(
        userProfile = userProfile,
        discipline = discipline,
        defaults={
            'currentSlide': discipline.begin,},
    )

    slide = slideState.currentSlide
    if not slide:
        # TODO. star from begin for now
        slide = discipline.begin
        slideState.currentSlide = slide
        slideState.save()
        #raise Http404

    # slide chain state:
    chainState, chainStateCreated = UserSlideChainState.objects.get_or_create(
        userProfile = userProfile,
        slideChain = slide.chain,
    )

    if request.method == 'GET':
        return render(request,
                      'iedu/slide.html',
                      Utils.createSlideContext(
                          disciplineName, slide))
    # POST:
    # Slide could be without question - then just pass:
    if slide.question:
        if 'choice' not in request.POST:
            messages.error(request, 'Не дан ответ')
            return HttpResponseRedirect(reverse('iedu:slide',
                                                args=[disciplineName]))

        choice = Choice.objects.get(id=request.POST.get('choice'))
        if choice.isCorrect:
            chainState.numberOfCorrect += 1

    # slide chain save state:
    chainState.countOfProcessedSlides += 1 # TODO: change to query count
    chainState.save() # Its also save changes form choice.isCorrect

    # TODO when chain complete:
    # print("chainTriggered: ", chainState.chainTriggered)

    # save next slide
    slideState.currentSlide = slideState.currentSlide.nextSlide
    slideState.save()

    return HttpResponseRedirect(reverse('iedu:slide', args=[disciplineName]))
