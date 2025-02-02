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
                        d.timezone='0' AND \
                        d.year='2020' AND \
                        d.month='04'), \
            day2 AS \
                (SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom \
                    FROM pop AS d \
                    INNER JOIN pop_mesh AS p \
                        ON p.name = d.mesh1kmid \
                    WHERE d.dayflag='0' AND \
                          d.timezone='0' AND \
                          d.year='2019' AND \
                          d.month='01') \
            SELECT poly.name_2, sum(day2.population)-sum(day.population) AS dif, poly.geom \
                FROM day, day2, adm2 AS poly \
                WHERE poly.name_1='Saitama' AND \
                    st_within(day.geom,poly.geom) AND \
                    st_within(day2.geom,poly.geom) \
            GROUP BY poly.name_2, poly.geom \
            ORDER BY dif DESC;"

    query_result_gdf = gpd.GeoDataFrame.from_postgis(
        sql, conn, geom_col='geom') #geom_col='way' when using osm_kanto, geom_col='geom' when using gisdb
    return query_result_gdf


def main():

    out = query_geopandas('gisdb') #specify db name
    print(out)

    #mapping
    #mapping options: https://geopandas.org/en/stable/docs/user_guide/mapping.html
    fig, ax = plt.subplots(1, 1)
    out.plot(ax=ax)

    #updating map
    out.plot(column='dif', ax=ax, legend=True, cmap='Purples')
    #spatial extent setting
    #minx=138.5
    #maxx=141
    #miny=35
    #maxy= 37.2
    #ax.set_xlim(minx, maxx)
    #ax.set_ylim(miny, maxy)

    plt.savefig('/work/python/F1-mapping.jpg') #specify filename

if __name__ == '__main__':
    main()