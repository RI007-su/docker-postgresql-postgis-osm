import os
from sqlalchemy import create_engine
import geopandas as gpd

def query_geopandas(table):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/gisdb'
    conn = create_engine(DATABASE_URL)

    sql = "select * from {} limit 3;".format(table)

    query_result_gdf = gpd.GeoDataFrame.from_postgis(
        sql, conn, geom_col='geom')
    return query_result_gdf


def main():

    out = query_geopandas('adm2') #specify table name
    print(out)

if __name__ == '__main__':
    main()
