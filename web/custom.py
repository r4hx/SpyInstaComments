import re

import requests
from django.core.exceptions import ValidationError
from requests.adapters import HTTPAdapter


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

def validate_keyword(name):
    if not name.isalpha():
        raise ValidationError('Ключевое слово {} содержит символы'.format(name))


def validate_username(name):
    result = re.findall(r'^[A-Za-z0-9._]+$', name)
    if not result:
        raise ValidationError('Имя пользователя {} содержит запрещенные символы'.format(name))
    else:
        response = req.get("https://www.instagram.com/{}/?__a=1".format(name))
        try:
            user_id = response.json()['graphql']['user']['id']
            if not user_id.isdigit():
                raise ValidationError('Пользователь {} не существует'.format(name))
        except ValueError:
            raise ValidationError('Пользователь {} не существует'.format(name))
