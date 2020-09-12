from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.utils.timezone import get_current_timezone

from .forms import RegisterForm, AccountForm, KeywordForm
from .models import Account, Comment, Keyword, Update


@login_required
def index(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        result = Account.objects.filter(owner=request.user, username=request.POST["username"]).count()
        if result == 0 and form.is_valid():
            ff = form.save(commit=False)
            ff.owner = request.user
            ff.save()
            ff.r.close()
            messages.success(request, 'Страница {} успешно добавлена'.format(ff.username))
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Эта страница уже отслеживается или не существует')
            return redirect(reverse('index'))

    else:
        keywords_count = Keyword.objects.filter(owner=request.user).count()
        update_available = Update.objects.filter(owner=request.user, last__lte=datetime.now(tz=get_current_timezone()) - timedelta(minutes=15))
        if keywords_count == 0:
            return redirect(reverse('keywords'))
        context = {
            'comment_not_read_count': Comment.objects.filter(owner=request.user, match=True, read=False).count(),
            'account_monitoring_count': Account.objects.filter(owner=request.user).count(),
            'keywords_count': keywords_count,
            'update_available': update_available,
        }
        return render(request, "index.html", context)


@login_required
def profiles(request):
    account_monitoring_count = Account.objects.filter(owner=request.user).count()
    update_available = Update.objects.filter(owner=request.user, last__lte=datetime.now(tz=get_current_timezone()) - timedelta(minutes=15))
    if account_monitoring_count == 0:
        return redirect(reverse('index'))
    context = {
        'profiles': Account.objects.filter(owner=request.user),
        'comment_not_read_count': Comment.objects.filter(owner=request.user, match=True, read=False).count(),
        'account_monitoring_count': account_monitoring_count,
        'keywords_count': Keyword.objects.filter(owner=request.user).count(),
        'update_available': update_available,
    }
    return render(request, "profiles.html", context)


@login_required
def keywords(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        result = Keyword.objects.filter(owner=request.user, name=request.POST["name"]).count()
        if result == 0 and form.is_valid():
            ff = form.save(commit=False)
            ff.owner = request.user
            ff.save()
            messages.success(request, 'Ключевое слово {} успешно добавлено'.format(ff.name))
            return redirect(reverse('keywords'))
        else:
            messages.error(request, 'Ключевое слово уже добавлено или содержит запрещенные символы')
            return redirect(reverse('keywords'))
    else:
        update_available = Update.objects.filter(owner=request.user, last__lte=datetime.now(tz=get_current_timezone()) - timedelta(minutes=15))
        context = {
            'keywords': Keyword.objects.filter(owner=request.user).order_by('name'),
            'comment_not_read_count': Comment.objects.filter(owner=request.user, match=True, read=False).count(),
            'account_monitoring_count': Account.objects.filter(owner=request.user).count(),
            'keywords_count': Keyword.objects.filter(owner=request.user).count(),
            'update_available': update_available,
        }
        return render(request, "keywords.html", context)


@login_required
def reports(request):
    comments = Comment.objects.filter(owner=request.user, match=True, read=False)
    comment_not_read_count = Comment.objects.filter(owner=request.user, match=True, read=False).count()
    update_available = Update.objects.filter(owner=request.user, last__lte=datetime.now(tz=get_current_timezone()) - timedelta(minutes=15))
    context = {
        'comments': comments,
        'comment_not_read_count': comment_not_read_count,
        'account_monitoring_count': Account.objects.filter(owner=request.user).count(),
        'keywords_count': Keyword.objects.filter(owner=request.user).count(),
        'update_available': update_available,
    }
    return render(request, "reports.html", context)


@login_required
def keywords_delete(request, keyword):
    k = Keyword.objects.get(owner=request.user, name=keyword)
    k.delete()
    return redirect(reverse('keywords'))


@login_required
def comment_read(request, comment_id):
    c = Comment.objects.get(owner=request.user, id=comment_id)
    c.read = True
    c.save()
    return render(request, 'close.html')


@login_required
def profiles_delete(request, uid):
    a = Account.objects.get(owner=request.user, uid=uid)
    a.delete()
    return redirect(reverse('profiles'))


@login_required
def profiles_update(request):
    account = Account.objects.filter(owner=request.user)
    update = Update.objects.get_or_create(owner=request.user)[0]
    update.save()
    for acc in account:
        a = Account.objects.get(username=acc.username)
        a.save()
        a.r.close()
    return redirect(reverse('reports'))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect(reverse('register_done'))
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def register_done(request):
    return render(request, 'register_done.html')
