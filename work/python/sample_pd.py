import os
from sqlalchemy import create_engine
import pandas as pd
#import geopandas as gpd

def query_pandas(tbl):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/gisdb'
    conn = create_engine(DATABASE_URL)

    sql = 'select * from {} limit 3;'.format(tbl)
    #sql = 'select count(name) from pop_mesh;'

    df = pd.read_sql(sql=sql, con=conn)

    return df


def main():

    out = query_pandas('pop_mesh') #specify table name
    print(out)

if __name__ == '__main__':
    main()
