from asyncio import run

from aiopg.sa import create_engine

from .models import *

engine = run(create_engine('postgres'))
