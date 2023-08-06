from pathlib import Path
from sqlmodel import SQLModel, create_engine

from . import models  # noqa
from .version import __version__  # noqa


def create_sqlite_engine(path, echo: bool = False):
    engine = create_engine(f"sqlite:///{Path(path).absolute()}", echo=echo)

    # Create tables:
    SQLModel.metadata.create_all(engine)

    return engine
