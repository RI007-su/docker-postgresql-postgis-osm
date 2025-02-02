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
            (SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom\
            FROM pop AS d \
                INNER JOIN pop_mesh AS p \
                   ON p.name = d.mesh1kmid \
                WHERE d.dayflag='0' AND \
                    d.timezone='0' AND \
                    d.year='2019' AND \
                    d.month='01')\
            SELECT poly.name_2, day.population/day.geom AS popg, poly.geom \
                FROM day, adm2 AS poly \
                WHERE st_within(day.geom,poly.geom) AND \
                    st_within(day2.geom,poly.geom) \
            GROUP BY poly.name_2, poly.geom;"\

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
    out.plot(column='popg', ax=ax, legend=True, cmap='viridis')
    #spatial extent setting
    minx=138.5
    maxx=141
    miny=35
    maxy= 37.2
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    plt.savefig('/work/python/F4.jpg') #specify filename

if __name__ == '__main__':
    main()