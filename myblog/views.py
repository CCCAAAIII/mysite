from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from myblog.models import User
from myblog.models import Article
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import json
from . import utils
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.db import transaction
from .forms import LoginForm
from django.forms.models import model_to_dict
from django.core.cache import cache
from django.core.paginator import Paginator
from django.conf import settings
# Create your views here.
def home(request):
    return render(request, 'myblog/home.html')


def logincheck(func, *args, **kwargs):
    def wrapper(request):
        is_login = request.session.get('email')
        # print(is_login)
        if is_login:
            return func(request)
        else:
            return redirect(reverse('myblog:login'))

    return wrapper


# @login_required(login_url='/myblog/login/')
@logincheck
def index(request):
    # print(request.session['user'].id)
    # print(request.session['email'])
    id = request.session['id']
    # print(id)
    lastarticle = Article.objects.filter(user_id=id, is_delete=False).order_by('pub_date').last()
    # cache.set('article',lastarticle)
    # print(cache.get('article'),'11111111111')

    # print(lastarticle)
    # 实现博客上一篇与下一篇功能
    has_prev = False
    has_next = False
    blog_prev = None
    blog_next = None
    msg = False
    if lastarticle is not None:
        msg = True
        pre1 = Article.objects.filter(user_id=id, is_delete=False, id__lt=lastarticle.id)
        nex1 = Article.objects.filter(user_id=id, is_delete=False, id__gt=lastarticle.id)
        # pre = pre1.first()
        # print(pre1)
        # print(len(nex1))
        if len(pre1) != 0:
            has_prev = True
            blog_prev = pre1.last()

        if len(nex1) != 0:
            has_next = True
            blog_next = nex1.first()
        # print(blog_prev)
        # print(blog_next)

    return render(request, 'myblog/index.html',
                  {'article': lastarticle, 'blog_prev': blog_prev, 'blog_next': blog_next, 'has_prev': has_prev,
                   'has_next': has_next, 'msg': msg})

@csrf_exempt
def check_username_pwd(request):
    email = request.POST.get('e')
    user = User.objects.filter(email=email)
    pwd = request.POST.get('pwd').strip()
    if len(user) > 0:
        u = user[0]
        if check_password(pwd, u.password):
            request.session['user'] = model_to_dict(u)
            # print(request.session['user'])
            request.session['email'] = u.email
            request.session['id'] = u.id
            request.session['username'] = u.username

            request.session.set_expiry(0)
            return JsonResponse({'msg': '1'})
        else:
            return JsonResponse({'msg': '456'})

    else:
        return JsonResponse({'msg': '123'})


def login(request):
    return render(request, 'myblog/login.html')


def loginfault(request):
    return render(request, 'myblog/loginfault.html')


def checkusername(request):
    email = request.POST.get('data')
    rs = User.objects.filter(email=email)
    if len(rs) > 0:
        msg = '0'
    else:
        msg = '1'
    return JsonResponse({'msg': msg})


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password = make_password(password)
            try:
                head_image = request.FILES['headimage']
                # print(head_image)
                u = User(username=username, email=email, password=password, avatar=head_image)
                u.save()
                return redirect(reverse('myblog:registersuccess'))
            except Exception as e:
                u = User(username=username, email=email, password=password)
                u.save()
                return redirect(reverse('myblog:registersuccess'))

        except Exception as e:
            # print('eeeeeee', e)
            # print('iiiiiiiiiiiiii111  ', head_image)

            return redirect(reverse('myblog:registerfault'))
    else:

        return render(request, 'myblog/register.html')


def registerfault(request):
    return render(request, 'myblog/registerfault.html')


def registersuccess(request):
    return render(request, 'myblog/registersuccess.html')


def showarticlelist(request,pagenow):
    # print(pagenow,type(pagenow))
    if pagenow == '':
        pagenow = 1
    # 从配置中读取每页显示的条数
    page_size = settings.PAGESIZE

    # 构建Paginator 对象

    id = request.session['id']
    article_list = Article.objects.filter(user__id=id, is_delete=False)

    paginator = Paginator(article_list,page_size)
    # 获取分页对象的列表
    plistcontent = paginator.page(pagenow)
    # 获取所有页码信息
    plist = paginator.page_range
    return render(request, 'myblog/showarticlelist.html', {'pagenow':int(pagenow),'plistcontent':plistcontent,'plist':plist})
    # return render(request, 'myblog/showarticlelist.html', {'article_list': article_list})


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
    # print(id)
    try:
        article = Article.objects.get(id=id)
        user_id = request.session['id']
        # 实现博客上一篇与下一篇功能
        has_prev = False
        has_next = False
        blog_prev = None
        blog_next = None
        pre1 = Article.objects.filter(user_id=user_id, is_delete=False, id__lt=id)
        nex1 = Article.objects.filter(user_id=user_id, is_delete=False, id__gt=id)
        # pre = pre1.first()
        if len(pre1) != 0:
            has_prev = True
            blog_prev = pre1.last()

        if len(nex1) != 0:
            has_next = True
            blog_next = nex1.first()
        print(blog_prev)
        print(blog_next)
        return render(request, 'myblog/articledetail.html',
                      {'article': article, 'blog_prev': blog_prev, 'blog_next': blog_next, 'has_prev': has_prev,
                       'has_next': has_next, })

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


def showimage(request):
    id = request.session['id']
    image = User.objects.get(id=id).avatar
    # print(image.url)
    # print(image)
    # print(image.path)
    return HttpResponse(image)
    # image = User.objects.get(id=1).avatar


def search_articles(request):
    pass


@csrf_exempt
def test(request):
    email = request.POST.get('e')
    user = User.objects.filter(email=email)
    pwd = request.POST.get('pwd').strip()
    if len(user) > 0:
        u = user[0]
        if check_password(pwd, u.password):
            request.session['user'] = model_to_dict(u)
            # print(request.session['user'])
            request.session['email'] = u.email
            request.session['id'] = u.id
            request.session['username'] = u.username

            request.session.set_expiry(0)
            return JsonResponse({'msg': '1'})
        else:
            return JsonResponse({'msg': '456'})

    else:
        return JsonResponse({'msg': '123'})


# @csrf_exempt
# def test(request):
#     if request.method == 'POST':
#         articles = Article.objects.all()
#         articles = serialize('json', articles)
#         return HttpResponse(articles)
#     return render(request, 'myblog/testajax.html')


# @transaction.Atomic
# def testtrans(request):
#     try:
#         User.objects.create(email='1',password='123',username='ccc')
#     except Exception as e:
#         print(e)
def formtest(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'myblog/testfrom.html', {'form': form})
    elif request.method == 'POST':
        return redirect(reverse('myblog:login'))


def logout(request):
    request.session.flush()
    return redirect(reverse('myblog:login'))
def updateinfo(request):
    if request.method=='POST':
        pass
    else:
        return render(request,'myblog/')