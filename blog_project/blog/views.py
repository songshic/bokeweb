#coding = utf-8
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
import logging
from .forms import *
from .models import *
from django.conf import settings
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db.models import Count
logger = logging.getLogger('blog.views')

def global_setting(request):
    # 分类信息的获取（导航数据）
    category_list = Category.objects.all()
    #浏览排行
    article_click_count = [Article_click for Article_click in Article.objects.values('id','click_count','title').order_by('-click_count')]
    #评论排行
    comment_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment')#使用了聚合函数和排序
    article_comment_count=[Article.objects.get(pk=comment['article']) for comment in comment_list]
    # 文章归档1.获取文章得月份—日期
    archive_list = Article.objects.distinct_date()
    return {
        'article_click_count':article_click_count,
        'article_comment_count':article_comment_count,
        'category_list':category_list,
        'archive_list':archive_list,
        'SITE_URL':settings.SITE_URL,
        'SITE_NAME':settings.SITE_NAME,
        'SITE_DESC':settings.SITE_DESC,
    }

def index(request):
    try:
        # 最新文章数据
        article_list = Article.objects.all()
        article_list = getPage(request,article_list)
    except Exception as e:
        logger.error(e)
    return render(request,'index.html',locals())

def archive(request):
    try :
        #先获取客户端提交的数据内容
        year = request.GET.get('year',None)
        month = request.GET.get('month',None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list = getPage(request,article_list)
    except Exception as e:
        logger.error(e)

    return render(request, 'archive.html', locals())


# 分页代码
def getPage(request,article_list):
    paginator = Paginator(article_list, 1)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (InvalidPage, EmptyPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


#文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id})
        comments = Comment.objects.filter(article=article).order_by('-date_publish')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        logger.error(e)
    article.increase_click()
    return render(request, 'article.html', locals())

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    url=reg_form.cleaned_data["url"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])