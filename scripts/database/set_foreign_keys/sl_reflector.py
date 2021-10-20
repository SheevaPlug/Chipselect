#!/usr/bin/env python
DBURL = 'postgresql://'

from pprint import pprint

from sqlalchemy import *
from sqlalchemy import inspection


if __name__ == '__main__':
    engine = create_engine(DBURL)
    metadata = MetaData(engine)
    metadata.reflect()
    #res = {table.name: [dict(row) for row in engine.execute(table.select())] for table in metadata.sorted_tables}
        
