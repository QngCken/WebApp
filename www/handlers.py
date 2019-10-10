#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers '
__author__ = 'QngCken'  '''handlers'''

import re, time, json, logging, hashlib, base64, asyncio

import markdown2

from aiohttp import web

from web import get, post
from apis import Page, APIValueError, APIPermissionError

from models import User, Comment, Blog, next_id
from config import configs

COOKIE_NAME = 'usrsession'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError:
        pass
    if p < 1:
        p = 1
    return p

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)

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
##首页显示blogs
@get('/')
async def test():
    blogs = await Blog.findAll(orderBy='created_at desc')
    return {
        '__template__': 'test.html',
        'blogs': blogs
    }

@get('/index')
async def index(*, page='1'):
    num = await Blog.findNumber('count(id)')
    page = Page(num, get_page_index(page))
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
    return {
        '__template__': 'index.html',
        'page': page,
        'blogs': blogs
    }

@get('/blog/{id}')
async def getBlog(id):
    blog = await Blog.find(id)
    # comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    # for c in comments:
    #     c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        # 'comments': comments
    }

@get('/doing')
async def doing():
    return {
        '__template__': 'doing.html',
    }