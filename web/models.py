import logging
from datetime import datetime

import requests
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import get_current_timezone
from requests.adapters import HTTPAdapter

from .custom import validate_keyword, validate_username

logging.basicConfig(level=logging.DEBUG)

global req

req = requests.Session()
headers = {
    'origin': 'https://www.instagram.com',
    'referer': 'https://www.instagram.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    'x-instagram-ajax': '1',
    'x-requested-with': 'XMLHttpRequest',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'ru-ru,ru;q=0.8,en-us;q=0.6,en;q=0.4',
    'accept': '*/*',
    'connection': 'keep-alive',
}
req.headers.update(headers)
req.mount('https://', HTTPAdapter(max_retries=5))


class Update(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    last = models.DateTimeField(auto_now_add=True, verbose_name="Последнее обновление")

    class Meta:
        verbose_name_plural = 'Обновления'
        verbose_name = 'Обновление'
        ordering = ['last']

    def save(self, *args, **kwargs):
        self.last = datetime.now(tz=get_current_timezone())
        super(Update, self).save(*args, **kwargs)


class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    url = models.URLField(null=True, verbose_name='Ссылка')
    uid = models.BigIntegerField(null=True, verbose_name='ID')
    full_name = models.CharField(null=True, blank=True, max_length=100, verbose_name='Имя')
    username = models.CharField(null=True, validators=[validate_username], max_length=50, verbose_name='Пользователь')
    pic_url = models.CharField(null=True, max_length=250, verbose_name='Аватар')
    biography = models.CharField(null=True, blank=True, max_length=250, verbose_name='Биография')
    external_url = models.CharField(null=True, blank=True, max_length=250, verbose_name='Внешняя ссылка')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Аккаунты'
        verbose_name = 'Аккаунт'
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.url = "https://www.instagram.com/{}/".format(self.username)
        self.r = req.get('{}?__a=1'.format(self.url))
        self.uid = self.r.json()['graphql']['user']['id']
        self.full_name = self.r.json()['graphql']['user']['full_name']
        self.pic_url = self.r.json()['graphql']['user']['profile_pic_url']
        self.biography = self.r.json()['graphql']['user']['biography']
        self.external_url = self.r.json()['graphql']['user']['external_url']
        Update.objects.get_or_create(owner=self.owner)
        super(Account, self).save(*args, **kwargs)
        self.i = 0
        while True:
            try:
                self.post_url = "https://www.instagram.com/p/{}/".format(
                    self.r.json()['graphql']['user']['edge_owner_to_timeline_media']['edges'][self.i]['node']['shortcode']
                )
                self.req_post = req.get('{}?__a=1'.format(self.post_url))
                self.post_uid = self.req_post.json()['graphql']['shortcode_media']['id']
                self.post_pic_url = self.req_post.json()['graphql']['shortcode_media']['display_url']
                self.post_text = self.req_post.json()['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
                self.timestamp = self.req_post.json()['graphql']['shortcode_media']['taken_at_timestamp']
                self.post_result = Post.objects.filter(
                    owner=self.owner,
                    username=Account.objects.get(uid=self.uid, owner=self.owner),
                    uid=self.post_uid,
                    url=self.post_url,
                ).count()
                if self.post_result == 0:
                    post = Post()
                    post.owner = self.owner
                    post.username = Account.objects.get(uid=self.uid, owner=self.owner)
                    post.uid = self.post_uid
                    post.url = self.post_url
                    post.timestamp = datetime.fromtimestamp(self.timestamp, tz=get_current_timezone())
                    post.pic_url = self.post_pic_url
                    post.text = self.post_text
                    post.save()
                else:
                    post = Post.objects.get(
                        owner=self.owner,
                        username=Account.objects.get(uid=self.uid, owner=self.owner),
                        uid=self.post_uid,
                        url=self.post_url,
                    )
                    post.timestamp = datetime.fromtimestamp(self.timestamp, tz=get_current_timezone())
                    post.pic_url = self.post_pic_url
                    post.text = self.post_text
                    post.save()
                self.i += 1
            except IndexError:
                break


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    username = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    uid = models.BigIntegerField(null=True, verbose_name='ID')
    timestamp = models.DateTimeField(null=True, verbose_name='Таймштамп')
    url = models.URLField(null=True, verbose_name='Ссылка')
    pic_url = models.CharField(null=True, max_length=500, verbose_name='Фото')
    text = models.CharField(null=True, max_length=5000, verbose_name='Текст')

    def __str__(self):
        return self.text[0:10]

    class Meta:
        verbose_name_plural = 'Публикации'
        verbose_name = 'Публикация'
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        self.i = 0
        self.r = req.get('{}?__a=1'.format(self.url))
        while True:
            try:
                self.comment_text = self.r.json()['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][self.i]['node']['text']
                self.comment_uid = self.r.json()['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][self.i]['node']['id']
                self.comment_username = self.r.json()['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][self.i]['node']['owner']['username']
                self.timestamp = self.r.json()['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][self.i]['node']['created_at']
                self.mode = 'comment'
                comment = Comment.objects.get_or_create(
                    uid=self.comment_uid,
                    owner=self.owner,
                    mode=self.mode,
                    post=Post.objects.get(uid=self.uid, owner=self.owner),
                    username=self.comment_username,
                )[0]
                comment.text = self.comment_text
                comment.timestamp = datetime.fromtimestamp(self.timestamp, tz=get_current_timezone())
                comment.save()
                self.a = 0
                while True:
                    try:
                        self.comment_text = self.r.json()['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][self.i]['node']['edge_threaded_comments']['edges'][self.a]['node']['text']
                        self.replay_uid = self.r.json()['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][self.i]['node']['edge_threaded_comments']['edges'][self.a]['node']['id']
                        self.comment_username = self.r.json()['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][self.i]['node']['edge_threaded_comments']['edges'][self.a]['node']['owner']['username']
                        self.timestamp = self.r.json()['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][self.i]['node']['edge_threaded_comments']['edges'][self.a]['node']['created_at']
                        self.mode = 'reply'
                        comment = Comment.objects.get_or_create(
                            uid=self.comment_uid,
                            replay_uid=self.replay_uid,
                            owner=self.owner,
                            mode=self.mode,
                            post=Post.objects.get(uid=self.uid, owner=self.owner),
                            username=self.comment_username,
                        )[0]
                        comment.text = self.comment_text
                        comment.timestamp = datetime.fromtimestamp(self.timestamp, tz=get_current_timezone())
                        comment.save()
                        self.a += 1
                    except IndexError:
                        break
                self.i += 1
            except IndexError:
                break


class Keyword(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    name = models.CharField(max_length=100, validators=[validate_keyword], verbose_name='Ключевое слово')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ключевые слова'
        verbose_name = 'Ключевое слово'
        ordering = ['id']


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    uid = models.BigIntegerField(null=True, verbose_name='ID комментария')
    timestamp = models.DateTimeField(verbose_name='Таймштамп', null=True)
    mode = models.CharField(null=True, max_length=25, verbose_name='Тип комментария')
    replay_uid = models.BigIntegerField(null=True, verbose_name='ID ответа')
    username = models.CharField(null=True, max_length=100, verbose_name='Пользователь')
    text = models.CharField(null=True, max_length=5000, verbose_name='Комментарий')
    match = models.BooleanField(default=False, verbose_name="Совпадение")
    read = models.BooleanField(default=False, verbose_name="Прочитано")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        try:
            self.keywords = [b.name for b in Keyword.objects.filter(owner=self.owner)]
            if self.username != str(self.post.username):
                for self.k in self.keywords:
                    if self.k.lower() in self.text.lower():
                        self.match = True
                        break
        except AttributeError:
            pass
        super(Comment, self).save(*args, **kwargs)
        req.close()
