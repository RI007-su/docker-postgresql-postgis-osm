# Tutorial

## 1. 境界データのインポート
はじめに、QGISでの描画で使用した`JAPAN_data`のうち、`JPN_adm2.shp`をインポートしてみよう。 
`JAPAN_data`を`/gis/pop_data`に保存しましょう。

### 1.1 データベースの作成
`gisdb`というデータベースを作成する。
```sh
createdb -U postgres gisdb
```
### 1.2. postgis extensionの有効化
```sql
psql -U postgres gisdb -c "create extension postgis"
```

### 1.3. sqlコマンドの作成
`shp2pgsql`でshpファイルをpostGISにインポートするためのsqlコマンドを作成する。

```sh
shp2pgsql -D -I -s 4326 /gis/pop_data/JAPAN_data/JPN_adm/JPN_adm2.shp adm2 > /gis/pop_data/adm2.sql
```
-D: ダンプ形式にする  
-I: 空間インデックスを作成  
-s: 座標系を定義（4326はespgコードで、WGS84）  
`JPN_adm2.shp`はがインポートするshpファイル  
`adm2`は追加するテーブル名  
`/gis/pop_data/adm2.sql`は変換するsqlコマンドが記載されたファイル  

### 1.4. DBへの追加
1.3で作成したsqlコマンドを用いてgisdb DBへデータを追加する。 

```sh
psql -U postgres -d gisdb -f /gis/pop_data/adm2.sql
```
### 1.5 QGISで描写
QGISのDB Managerからアクセスし描写してみよう。

## 2. openstreetmapデータベースの構築
openstreetmapで取得し、データを入力してみよう。 
かなりの時間がかかる（私の環境では3時間程）ので余裕をもって実施すること。
### 2.1. OSMデータの取得
[osm data](http://download.geofabrik.de/asia/japan.html)から関東地域のデータ(.osm.pbf)をダウンロードし、 `/gis/osm` に保存する。 

### 2.2. スキーマの作成とデータ入力
[osm data](http://download.geofabrik.de/asia/japan.html)と[default.style](https://learnosm.org/files/default.style)のあるディレクトリ `/gis/osm` をカレントディレクトリとし、以下を実行する。

```sh
osm2pgsql --create --database=gisdb --slim --style=./default.style -U postgres -H localhost kanto-latest.osm.pbf
```
（注意）かなり時間がかかります。 
もし、データベース作成にエラーが発生したりした場合は、データ量の少ない四国地域のデータで講義に取り組んでも大丈夫です。 


## 3. 人流データのインポート

データはG空間情報センターより取得している。 
データ数が多いので、サンプルデータとして 
https://www.geospatial.jp/ckan/dataset/mlit-1km-fromto  


### 3.1. meshデータ
[サンプルデータ](https://drive.google.com/file/d/1PqhdZpRe3HFKoOnYXq3qclbFfjUFgdQl/view?usp=sharing)を入手し、中にある`mesh1.zip`を解凍し、`/gis/pop_data`内に保存する。
#### 3.1.1. sqlコマンドの作成
shp2pgsqlでshpファイルをpostGISにインポートするためのsqlコマンドを作成する。

```sh
shp2pgsql -D -I -s 4326 /gis/pop_data/mesh1/mesh1.shp pop_mesh > /gis/pop_data/mesh1.sql
```
-D: ダンプ形式にする  
-I: 空間インデックスを作成  
-s: 座標系を定義（4326はespgコードで、WGS84）  
`/gis/pop_data/mesh1/mesh1.shp`はがインポートするshpファイル  
`pop_mesh`は追加するテーブル名  
`/gis/pop_data/mesh1.sql`は変換するsqlコマンドが記載されたファイル  

#### 3.1.2. DBへの追加
1で作成したsqlコマンドを用いてgisdb DBへデータを追加する。 

```sh
psql -U postgres -d gisdb -f /gis/pop_data/mesh1.sql
```

### 3.2. 人流データ(csv)のインポート
一月ごとの集計データが入手可能。 
[サンプルデータ](https://drive.google.com/file/d/1PqhdZpRe3HFKoOnYXq3qclbFfjUFgdQl/view?usp=sharing)を入手し、中にある`prefs.zip`を解凍し、`/gis/pop_data`内に保存する。 
この講義では負荷軽減のため2019年1月、2020年1月の集計データのみを使用する。  

#### 3.2.1. gisdbにアクセス
```
psql -U postgres -d gisdb
```

#### 3.2.2. テーブル作成
```sql
CREATE TABLE "pop" (
    "mesh1kmid" varchar(80),
    "prefcode" varchar(80),
    "citycode" varchar(80),
    "year"  varchar(80),
    "month" varchar(80),
    "dayflag" varchar(80),
    "timezone" varchar(80),
    "population" numeric
);

```
#### 3.2.3. csvデータのインポート
`pop_data`には1都6県の月別人流データが別々にzipで固まっている。 
zipを解凍してcsvファイルを取り出し、かつpostgresqlにインポートするためのsqlコマンドを作成するshellスクリプト（`copy_csv.sh`）を作成し、`/gis/pop_data`に配置する。


```sh
#!/bin/sh

for entry in /gis/pop_data/prefs/*/*/*/*.zip
do
  datapath=`echo $(dirname $entry)`
  unzip -o $entry -d $datapath
  csvname=`echo $datapath'/monthly_mdp_mesh1km.csv'`
  echo $csvname
  echo "COPY pop FROM '$csvname' with (format csv, header true, null '', force_null(population));" >> /gis/pop_data/copy_csv.sql
done

```
`copy_csv.sh`を実行する。
```sh
sh /gis/pop_data/copy_csv.sh
```

`copy_csv.sql`を実行する.
```sh
psql -U postgres -d gisdb -f /gis/pop_data/copy_csv.sql
```

これですべてのでcsvデータが`pop`テーブルにインポートされる。

#### 3.2.4. meshとcsvデータの結合
定義書より、  
集計期間(平休日) `dayflag`は“0”:休日 “1”:平日 “2”:全日  
集計期間(時間帯) `timezone`は“0”:昼 “1”:深夜 “2”:終日  
である。
ここでは2019年1月の休日・昼を考えてみよう。   

以下をQGISのDB Managerで実行する。
```
SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom FROM pop AS d INNER JOIN pop_mesh AS p ON p.name = d.mesh1kmid WHERE d.dayflag='0' AND d.timezone='0' AND d.year='2019';

```

#### 3.2.5. レコード数のチェック
上記の問い合わせ処理のビューを作成してみる。
 ```sql

CREATE VIEW pop201901 AS SELECT p.name, d.prefcode, d.year, d.month, d.population, p.geom FROM pop AS d INNER JOIN pop_mesh AS p ON p.name = d.mesh1kmid WHERE d.dayflag='0' AND d.timezone='0' AND d.year='2019';

```

```sql
select count(name) from pop_mesh;
select count(name) from pop201901;
```

