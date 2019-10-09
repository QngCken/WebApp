#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from web import get, post
from models import User, Comment, Blog, next_id
from config import configs

COOKIE_NAME = 'usrsession'
_COOKIE_KEY = configs.session.secret

async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/')
async def index():
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }
