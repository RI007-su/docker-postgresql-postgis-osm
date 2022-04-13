https://qiita.com/hiyuzawa/items/ba1b9de36bf911145c1c

# 1. create db
```
createdb -U postgres osm_kanto
```
# 2. connect to db
```
psql -U postgres osm_kanto
```
# 3. activate postgis extension
```
create extension postgis;
```
# 4. disconnect db
```
\q
```
# 5. create table schema
At working directory where [osm data](http://download.geofabrik.de/asia/japan.html) and [default.style](https://learnosm.org/files/default.style) are located:
```
osm2pgsql --create --database=osm_kanto --slim --style=./default.style -U postgres -H localhost kanto-latest.osm.pbf
```
# 6. wait & wait & wait