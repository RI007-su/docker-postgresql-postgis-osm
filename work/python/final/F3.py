import os
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 100)

def query_geopandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    sql = "WITH \
            day AS \
                (SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom \
                    FROM pop AS d \
                    INNER JOIN pop_mesh AS p \
                        ON p.name = d.mesh1kmid \
                    WHERE d.dayflag='0' AND \
                        d.year='2019' AND \
                        d.month='01') \
            SELECT poly.name_2, day.population/day.geom AS popg, poly.geom \
                FROM day, adm2 AS poly \
                WHERE poly.name_1='Tokyo' AND \
                    st_within(day.geom,poly.geom) AND \
            GROUP BY poly.name_2, poly.geom \
            ORDER BY popg DESC LIMIT 10;"

    query_result_gdf = gpd.GeoDataFrame.from_postgis(
        sql, conn, geom_col='geom') #geom_col='way' when using osm_kanto, geom_col='geom' when using gisdb
    return query_result_gdf


def main():

    out = query_pandas('gisdb') #specify db name
    print(out)

if __name__ == '__main__':
    main()