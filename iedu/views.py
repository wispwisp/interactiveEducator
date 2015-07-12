from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from iedu.forms import UserForm, UserProfileForm
from iedu.models import Slide, UserProfile, Choice, Progress, AdditionalSlide

from iedu import Utils


def index(request):
    return render(request, 'iedu/index.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.currnetSlide = Slide.objects.all()[0]
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'iedu/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('iedu:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'iedu/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/iedu')


@login_required
def slide(request):
    userProfile = request.user.userprofile
    slide = userProfile.currentSlide
    contDict = Utils.createSlide(slide)
    if request.method == 'GET':
        return render(request,
                      'iedu/slide.html',
                      contDict)

    # POST
    if 'choice' not in request.POST:
        contDict['errMesg'] = 'Выберите ответ'
        return render(request, 'iedu/slide.html', contDict)

    # grading:
    progress, isCreated = request.user.progress_set.get_or_create(
        theme=slide.question.theme, defaults={'user': request.user, 'score': 0}
    )
    choice = Choice.objects.get(id=request.POST['choice'])
    if choice.isCorrect:
        progress.score += 1
        progress.save()

    userProfile.currentSlide = slide.nextSlide
    userProfile.save()

    return HttpResponseRedirect(reverse('iedu:slide'))
