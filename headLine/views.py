from profile import Profile

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.urls import reverse, reverse_lazy

from headLine.forms import ProfileForm, BaseForm, LoginForm,CategoryForm, PreferenceForm,ArticleForm, ModifyProfilePhotoForm
from headLine.models import UserProfile, Category, Article


def register(request):
    logout(request)
    if request.method == 'POST':

        base_form = BaseForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        print(request.FILES)

        if base_form.is_valid() and profile_form.is_valid():
            user = base_form.save()
            user.set_password(base_form.cleaned_data['password'])
            user.save()
            profile = UserProfile.objects.get(user=user)
            profile.date_of_birth = profile_form.cleaned_data['date_of_birth']
            profile.profile_photo = profile_form.cleaned_data['profile_photo']
            profile.save()
            subject = ' Welcome to News App'
            message = ' Thank you for your registration!'
            fmail = settings.EMAIL_HOST_USER
            send_mail(subject,message,fmail,[user.email], fail_silently=True)
            return redirect(reverse('headline:home'))

    else:

        base_form = BaseForm()
        profile_form = ProfileForm()

    return render(request, 'register1.html', {'base_form': base_form, 'profile_form': profile_form})


def addArticle(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            
            
            article_title = article_form.cleaned_data['article_title']
            article_summary = article_form.cleaned_data['article_summary']
            article_body = article_form.cleaned_data['article_body']
            categ = Category.objects.get(id=1)
            ar = Article(article_title=article_title,article_summary=article_summary,article_body=article_body,category=categ)
            ar.save()
            

    return render(request, 'addAr.html')


def addCategory(request):
    if request.method == 'POST':
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            
            category_name = cat_form.cleaned_data['category_name']
            category_description = cat_form.cleaned_data['category_description']
            
            cat = Category(category_name=category_name,category_description=category_description)
            cat.save()
            print(category_name)
            print(category_description)

    return render(request, 'addCat.html')


def login_user(request):
    if request.method == 'POST':

        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('headline:home'))
                else:
                    login_form.add_error(None, 'User is not active')
            else:
                login_form.add_error(None, 'Username/Password is not valid')


    else:
        login_form = LoginForm()

    return render(request, 'login1.html', {'login_form': login_form})


def logout_user(request):
    logout(request)
    return redirect(reverse('headline:login'))


@login_required(login_url=reverse_lazy('headline:login'))
def home(request):
    categories = list(
        map(lambda c: {'id': c.id, 'name': c.category_name}, Category.objects.filter(selected_by=request.user)))
    return render(request, 'home.html', {'userData': {'userId': request.user.id, 'selectedCategories': categories}})


@login_required(login_url=reverse_lazy('headline:login'))
def profile(request):
    categories = Category.objects.all()
    choices = [(category.id, category.category_name) for category in categories]

    if request.method == 'POST':
        preference_form = PreferenceForm(request.POST, choices=choices)
        profile_photo_form = ModifyProfilePhotoForm(request.POST, request.FILES)
        if request.POST.get('photoDelete'):
            request.user.profile.profile_photo = None
            request.user.profile.save()
            profile_photo_form = ModifyProfilePhotoForm()

        elif request.POST.get('photoChange') and profile_photo_form.is_valid():
            request.user.profile.profile_photo = profile_photo_form.cleaned_data.get('profile_photo')
            request.user.profile.save()
            profile_photo_form = ModifyProfilePhotoForm()


        elif request.POST.get('preference') and preference_form.is_valid():
            for category in Category.objects.all():
                category.selected_by.remove(request.user)
                if str(category.id) in preference_form.cleaned_data.get('selected_categories'):
                    category.selected_by.add(request.user)
                    category.save()

        else:
            print("SOMETHING HAS GONE HORRIBLY WRONG")

    else:
        selected = [category.id
                    for category in categories.filter(selected_by=request.user.id)]
        preference_form = PreferenceForm(choices=choices, selected=selected)
        profile_photo_form = ModifyProfilePhotoForm()

    return render(request, 'profile.html',
                  {'preference_form': preference_form, 'profile': request.user.profile,
                   'profile_form': profile_photo_form})


@login_required(login_url=reverse_lazy('headline:login'))
def article(request, id):
    selected_article = Article.objects.get(id=id)
    print("Loading article: " + selected_article.article_title)
    comments = list(map(lambda x: x.id, selected_article.comments.all()))
    return render(request, 'article.html',
                  {'article_data': {'id': selected_article.id},
                   'user_data': request.user.id})
