import os
from sqlalchemy import create_engine
import geopandas as gpd
import matplotlib.pyplot as plt

def query_geopandas(db):
    DATABASE_URL='postgresql://postgres:postgres@postgis_container:5432/{}'.format(db)
    conn = create_engine(DATABASE_URL)

    sql = "select * from planet_osm_polygon;"

    query_result_gdf = gpd.GeoDataFrame.from_postgis(
        sql, conn, geom_col='way') #geom_col='way' when using osm_kanto, geom_col='geom' when using gisdb
    return query_result_gdf


def main():

    out = query_geopandas('osm_kanto') #specify db name
    print(out)

    #mapping
    #mapping options: https://geopandas.org/en/stable/docs/user_guide/mapping.html
    out.plot()

    plt.savefig('/work/python/sample_mapping2.jpg') #specify filename

if __name__ == '__main__':
    main()
