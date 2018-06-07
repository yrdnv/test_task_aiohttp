from aiohttp import web
from models import article
from init_db import init_pg, close_pg
import aiohttp_jinja2
import jinja2
from psycopg2 import DataError


app = web.Application()

app.on_startup.append(init_pg)   # create_engine on startup server
app.on_cleanup.append(close_pg)

routes = web.RouteTableDef()

aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('template'))  # connect tamplates


@routes.view('/', name='index')
@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(article.select())  # SELECT * FROM article
        articles = await cursor.fetchall()
        context = {'articles': articles}

        if request.method == 'POST':
            data = await request.post()
            text = data['article']
            if text:   # if text not empty trying save it to db
                try:
                    async with request.app['db'].acquire() as conn:
                        await conn.execute(article.insert().values(text=text))  # INSERT INTO article (text)
                except DataError as e:                                          # VALUES (text)
                    context['error'] = e    # if text length > 2048
                else:
                    return web.HTTPFound(location=app.router['index'].url_for())    # redirect if successfully
        return context



@routes.view('/{article_id}/', name='article')
@aiohttp_jinja2.template('article.html')
async def result(request):
    article_id = request.match_info['article_id']
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(article.select().where(article.c.id == article_id)) # Trying get article by ID
        data = await cursor.first()

        if not data:
            raise web.HTTPNotFound()    # redirect if ID not found

        #removing '.', ',', spaces and split words to list
        to_list = data.text.strip().replace('.', '').replace(',', '').replace('!', '').lower().split(' ')
        #sorting and collect to the string
        data_new = ' '.join(sorted(to_list, key=lambda x: (to_list.count(x), x)))

        return {'article': data,
                'article_new': data_new}


app.router.add_routes(routes)
web.run_app(app)
