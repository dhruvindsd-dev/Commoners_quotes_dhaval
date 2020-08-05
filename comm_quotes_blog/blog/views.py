from django.shortcuts import render, redirect
from .models import Blog_db, Submitted_articles
from django.core.mail import send_mail
from .email_verification import send_email
from django.views import View
import random

# Create your views here.

#  NORMAL REQUESTS


def home_index(request):
    articles = Blog_db.objects.values('catagory').distinct()
    return render(request, 'index.html', {'stories': Blog_db.objects.filter(catagory='stories', featured=True)[:3], 'quotes': Blog_db.objects.filter(catagory='quotes', featured=True)[:4]
                                          })


def all_quotes(request):
    if 'authentication' in request.session:
        if request.session['authentication'] == True:
            return render(request, 'all_quotes.html', {'quotes': Blog_db.objects.filter(catagory='quotes'), 'authentication': True})
    else:
        return render(request, 'all_quotes.html', {'quotes': Blog_db.objects.filter(catagory='quotes'), 'authentication': False})


def all_stories(request):
    return render(request, 'all_stories.html', {'stories': Blog_db.objects.filter(catagory='stories')})


def all_poems(request):
    return render(request, 'all_poems.html', {'poems': Blog_db.objects.filter(catagory='poems')})


def random_article_submission(request):
    if request.POST:
        otp = str(random.randint(1, 9999)).zfill(4)
        request.session['user_otp'] = otp
        request.session['otp_auth'] = True
        send_email(
            request.POST['email'], 'OTP  Commoners Qutoes.', f'Your requested OTP is {otp}. Please do not share this with anyone.')
        return redirect('/otp_verification')
    return render(request, 'submit_article.html')


def otp_verification(request):
    if 'otp_auth' in request.session:
        if request.session['otp_auth']:
            if request.POST:
                if request.session['user_otp'] == request.POST['otp']:  # valid otp
                    request.session['user_authenticate'] = True
                    request.session['otp_auth'] = False
                    return redirect('/article')
                else:  # invalid otp
                    return render(request, 'otp_verification.html', {'err': 'Invalid OTP'})
            return render(request, 'otp_verification.html')
        else:
            return redirect('/submit_article')
    else:
        return redirect('/submit_article')


def article_submit(request):
    if 'user_authenticate' in request.session:
        if request.session['user_authenticate']:
            if request.POST:
                Submitted_articles.objects.create(name=request.POST['name'],
                                                  number=request.POST['number'],
                                                  email=request.POST['email'],
                                                  content=request.POST['article'])
                request.session['user_authenticate'] = False
                return render(request, 'after_submit.html')
            return render(request, 'main_article_submit_form.html')
        else:
            return redirect('/submit_article')
    else:
        return redirect('/submit_article')


def user_submit_articles(request, id=None):
    return render(request, 'user_submitted_articles.html', {'articles': Submitted_articles.objects.all()})

# ADMIN REQUESTS


def authentication(request):
    if 'authentication' in request.session:
        if request.session['authentication'] == True:
            return True
        else:
            return False


def admin_handle(request):
    username = 'something'
    password = 'something'
    if request.POST:
        if request.POST['username'] == username and request.POST['password'] == password:
            request.session['authentication'] = True
            return redirect('/admin_handle_loged_in')
        else:
            return render(request, 'admin_handle_login_form.html', {'err': 'incorrect usename or password'})
    return render(request, 'admin_handle_login_form.html')


def admin_handle_login(request):
    if authentication(request):
        return render(request, 'admin_handle.html', {'quotes': Blog_db.objects.filter(catagory='quotes').order_by('-id')[:4], 'stories': Blog_db.objects.filter(catagory='stories').order_by('-id')[:3], 'poems': Blog_db.objects.filter(catagory='poems').order_by('-id')[:3]})
    else:
        return redirect('/admin_handle')


def create_stories_and_blogs(request, cata):
    if authentication(authentication):
        if request.POST:
            title = request.POST['title']
            description = request.POST['description']
            content = request.POST['content']
            if 'featured' in request.POST:
                featured = True
            else:
                featured = False
            read_time = request.POST['read_time']
            blog = Blog_db.objects.create(featured=featured, title=request.POST['title'], subtitle=request.POST['description'], read_time=read_time,
                                          content=request.POST['content'], author=request.POST['author'], catagory=request.POST['catagory'])
            return redirect(f'/img_select/{blog.id}')
        if cata == 'stories':
            return render(request, 'stories_and_blog_create.html', {'catagory': 'stories', 'type': 'Create'})
        elif cata == 'poems':
            return render(request, 'stories_and_blog_create.html', {'catagory': 'poems', 'type': 'Create'})
    else:
        return redirect('/admin_handle')


def img_select(request, id):
    if authentication(request):
        if request.method == 'POST':
            if 'img' in request.FILES:
                blog = Blog_db.objects.get(id=id)
                blog.img = request.FILES['img']
                blog.compressImage()
                blog.img_link = None
                blog.save()
            else:
                blog = Blog_db.objects.get(id=id)
                blog.img_link = request.POST['img_link']
                blog.img = None
                blog.save()
                return redirect('/admin_handle_loged_in')

            return redirect('/admin_handle_loged_in')
        return render(request, 'img_select.html', {'id': id})
    else:
        return redirect('/admin_handle')


def create_quotes(request):
    if authentication(request):
        if request.POST:
            if 'featured' in request.POST:
                featured = True
            else:
                featured = False
            Blog_db.objects.create(
                title=request.POST['title'], author=request.POST['author'], catagory=request.POST['catagory'], featured=featured)
            return redirect('/admin_handle')
        return render(request, 'quotes_create.html', {'catagory': 'quotes', 'action': 'New'})
    else:
        return redirect('/admin_handle')


def view_stories_poems(request, id):
    if 'authentication' in request.session:
        if request.session['authentication'] == True:
            return render(request, 'view_articles_stories.html', {'article': Blog_db.objects.get(id=id), 'authenticate': True})
    else:
        return render(request, 'view_articles_stories.html', {'article': Blog_db.objects.get(id=id)})


def edit_stories_poems(request, id):
    if authentication(request):
        if request.POST:
            if 'featured' in request.POST:
                featured = True
            else:
                featured = False
            article = Blog_db.objects.get(id=id)
            article.title = request.POST['title']
            article.subtitle = request.POST['description']
            article.content = request.POST['content']
            article.author = request.POST['author']
            article.catagory = request.POST['catagory']
            article.featured = featured
            article.read_time = request.POST['read_time']
            article.save()
            if request.POST['img_redirect'] == 'true':
                return redirect(f'/img_select/{id}')
            elif request.POST['img_redirect']:
                return redirect('/admin_handle_loged_in')
        article = Blog_db.objects.get(id=id)
        return render(request, 'stories_and_blog_create.html', {'article': article, "catagory": article.catagory, 'type': 'Save changes'})
    else:
        return redirect('/admin_handle')


def edit_quote(request, id):
    if authentication(request):
        if request.POST:
            quote = Blog_db.objects.get(id=id)
            quote.title = request.POST['title']
            quote.author = request.POST['author']
            if 'featured' in request.POST:
                quote.featured = True
            else:
                quote.featured = False
            quote.save()
            return redirect('/admin_handle_loged_in')
        return render(request, 'quotes_create.html', {'catagory': 'quotes', 'quote': Blog_db.objects.get(id=id), 'action': 'Edit'})
    else:
        return redirect('/admin_handle')


def article_delete(request, id):
    if authentication(request):
        article = Blog_db.objects.filter(id=id)
        if request.POST:
            if request.POST['confirmation'] == 'true':
                cata = article[0].catagory
                article.delete()
                return redirect(f'/{cata}')
            elif request.POST['confirmation']:
                return render('/somewhere')
        return render(request, 'delete_confirm.html', {'article': article})
    else:
        return redirect('/admin_handle')
