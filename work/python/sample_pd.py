import os
from sqlalchemy import create_engine
import pandas as pd
#import geopandas as gpd

def query_pandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    sql = 'select * from pop_mesh limit 3;'
    #sql = 'select count(name) from pop_mesh;'

    df = pd.read_sql(sql=sql, con=conn)

    return df


def main():

    out = query_pandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()
