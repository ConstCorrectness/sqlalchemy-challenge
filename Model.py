from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from sqlalchemy import inspect

import pathlib

db_path = pathlib.Path('Resources/hawaii.sqlite')
engine = create_engine(f'sqlite:///{db_path}')

session = sessionmaker(bind=engine)()

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


