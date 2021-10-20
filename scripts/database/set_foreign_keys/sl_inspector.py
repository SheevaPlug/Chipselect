#!/usr/bin/env python
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()
engine = create_engine('postgresql://')
Base.prepare(engine, reflect=True)

if __name__ == '__main__':
    print(Base)
    print(dir(Base))
    print(Base.classes)
