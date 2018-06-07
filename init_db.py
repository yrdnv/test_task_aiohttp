import settings
import aiopg.sa


async def init_pg(app):

    engine = await aiopg.sa.create_engine(
        database=settings.database,
        user=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
    )
    app['db'] = engine



async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

