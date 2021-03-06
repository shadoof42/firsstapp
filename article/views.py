from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from article.forms import CommentForm
from article.models import Article, Comments
from django.core.paginator import Paginator


# Create your views here.
def basic_one(request):
    view = "basic_one"
    html = "<html><body>This is %s view</body></html>" % view
    return HttpResponse(html)


def main_page(request):
    return render_to_response('main_page.html')


def template_two(request):
    view = "template_two"
    t = get_template('myview.html')
    html = t.render(Context({'name': view}))
    return HttpResponse(html)


def template_three_simple(request):
    view = "template_three"
    return render_to_response('myview.html', {'name': view})

#
# def goto_articles(request):
#
#     return articles(request,1)


def articles(request, page_number=1):
    all_articles = Article.objects.all()
    current_page = Paginator(all_articles, 3)
    print("Page article N  ", page_number)
    return render_to_response('articles.html',
                              {'articles': current_page.page(page_number), 'username': auth.get_user(request).username})


# def article(request, article_id=1):
#     return render_to_response('article.html', {'article': Article.objects.get(id=article_id),
#                                                'comments': Comments.objects.filter(comments_arcticle_id=article_id)})

def article(request, article_id=1,comment_page=1):
    comment_form = CommentForm
    args = {}
    args.update(csrf(request))
    args['article'] = Article.objects.get(id=article_id)
    all_comments = Comments.objects.filter(comments_article_id=article_id)
    # print("Length of comments = ", all_comments.__len__())
    current_comment_page = Paginator(all_comments,3)
    print("Page N  ",comment_page)
    args['comments'] = current_comment_page.page(comment_page)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    return render_to_response('article.html', args)


# def addlike(request, article_id):
#     try:
#         article = Article.objects.get(id=article_id)
#         article.article_likes += 1
#         article.save()
#     except ObjectDoesNotExist:
#         raise Http404
#     return redirect('/articles/all')

def addlike(request, article_id):
    back_url = request.META['HTTP_REFERER']
    try:
        if article_id in request.COOKIES:
            redirect(back_url)
        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            response = redirect(back_url)
            response.set_cookie(article_id, "test")
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect(back_url)


def addcomment(request, article_id):
    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_article = Article.objects.get(id=article_id)
            form.save()
            request.session.set_expiry(4)
            request.session['pause'] = False
        else:
            print ("Form is unvalid")
    return redirect('/articles/get/%s' % article_id)
