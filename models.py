import settings
from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine



DSN = "postgresql://{user}:{password}@{host}:{port}/{database}".format(user=settings.user,
                                                                       password=settings.password,
                                                                       database=settings.database,
                                                                       host=settings.host, port=settings.port)


meta = MetaData()

article = Table(
    'article', meta,

    Column('id', Integer, primary_key=True),
    Column('text', String(2048), nullable=False)
)


engine = create_engine(DSN)
meta.create_all(bind=engine)

