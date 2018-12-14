from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from myblog.models import User
from myblog.models import Article
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import time
from . import utils
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.db import transaction
from .forms import LoginForm


# Create your views here.
def home(request):
    return render(request, 'myblog/home.html')


def logincheck(func, *args, **kwargs):
    def wrapper(request):
        is_login = request.session.get('email')
        print(is_login)
        if is_login:
            return func(request)
        else:
            return redirect(reverse('myblog:login'))

    return wrapper


@logincheck
def index(request):
    print(request.session['email'])
    id = request.session['id']
    print(id)
    lastarticle = Article.objects.filter(user_id=id).first()
    print(lastarticle)
    return render(request, 'myblog/index.html', {'article': lastarticle})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('e').strip()
        pwd = request.POST.get('pwd').strip()

        print(email, pwd)
        try:
            u = User.objects.get(email=email)
            if u is not None:
                if check_password(pwd, u.password):
                    print(u, u.id, u.email, u.password)
                    request.session['email'] = u.email
                    request.session['id'] = u.id

                    request.session.set_expiry(0)
                    return redirect(reverse('myblog:index'))
                else:
                    print('pwd error')
                    return redirect(reverse('myblog:loginfault'))

            else:
                print('user not exist')
                return redirect(reverse('myblog:login'))

        except Exception as e:
            print(e)
            return redirect(reverse('myblog:login'))

    else:
        return render(request, 'myblog/login.html')


def loginfault(request):
    return render(request, 'myblog/loginfault.html')


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password = make_password(password)
            u = User(username=username, email=email, password=password)
            u.save()
            return redirect(reverse('myblog:registersuccess'))
        except Exception as e:
            print(e)
            return redirect(reverse('myblog:registerfault'))
    else:
        return render(request, 'myblog/register.html')


def registerfault(request):
    return render(request, 'myblog/registerfault.html')


def registersuccess(request):
    return render(request, 'myblog/registersuccess.html')


def showarticlelist(request):
    id = request.session['id']
    article_list = Article.objects.filter(user__id=id, is_delete=False)
    return render(request, 'myblog/showarticlelist.html', {'article_list': article_list})


@logincheck
def addarticle(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            content = request.POST.get('content')
            user_id = request.session['id']
            pub_date = datetime.now()
            # article = Article(title=title, content=content, user_id=user_id, publish_date=publish_data)
            # article.save
            Article.objects.create(title=title, content=content, user_id=user_id, pub_date=pub_date)
            return redirect(reverse('myblog:addsuccess'))
        except Exception as e:
            print(e)
            return render(request, 'myblog/addarticle.html')

    else:
        return render(request, 'myblog/addarticle.html')


def addsuccess(request):
    return render(request, 'myblog/addsuccess.html')


def articledetail(request, id):
    print(id)
    try:
        article = Article.objects.get(id=id)
        return render(request, 'myblog/articledetail.html', {'article': article})

    except Exception as e:
        print(e)


def articleedit(request, id):
    if request.method == 'GET':
        try:
            article = Article.objects.get(id=id)
            return render(request, 'myblog/articleedit.html', {'article': article})
        except Exception as e:
            print(e)
            return render(request, 'myblog/articleedit.html', {'article': None})
    elif request.method == 'POST':
        try:
            if request.session['check_code'] == request.POST.get('code'):
                print(request.session['check_code'], request.POST.get('code'))
                article = Article.objects.get(id=id)
                article.title = request.POST.get('title')
                article.content = request.POST.get('content')
                article.mod_date = datetime.now()
                article.save()
                print('ok')
                return redirect(reverse('myblog:showarticlelist'))
            else:
                return redirect(reverse('myblog:showarticlelist'))
        except Exception as e:
            print(e)
            return render(request, 'myblog/articleedit.html', {'article': None})


def articledelete(request, id):
    article = Article.objects.get(id=id)
    article.is_delete = True
    article.save()
    return redirect(reverse('myblog:showarticlelist'))


def check_code(request):
    f = BytesIO()
    img, code = utils.create_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


def search_articles(request):
    pass


@csrf_exempt
def test(request):
    if request.method == 'POST':
        articles = Article.objects.all()
        articles = serialize('json', articles)
        return HttpResponse(articles)
    return render(request, 'myblog/testajax.html')


# @transaction.Atomic
# def testtrans(request):
#     try:
#         User.objects.create(email='1',password='123',username='ccc')
#     except Exception as e:
#         print(e)
def formtest(request):
    if request.method=='GET':
        form = LoginForm()
        return render(request, 'myblog/testfrom.html',{'form':form})
    elif request.method=='POST':
        return redirect(reverse('myblog:login'))