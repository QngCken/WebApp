# !user/bin/env python3
# -*- coding: utf-8 -*-
from aiohttp import web

async def index(request):
    return web.Response(text='Awesome')

app = web.Application()
app.add_routes([web.get('/', index)])
web.run_app(app, host='0.0.0.0', port=9999)
