# Docker image for postgis with osm2pgsql & shp2pgsql


## Prerequisites
- DockerとVScodeのインストール  
- Docker Extensionのインストール  
- [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)  のインストール
- 任意の作業ディレクトリの作成  

## 起動
VScodeを立ち上げ、作業ディレクトリ内で以下をTerminalで実行する。　

```sh
docker-compose up -d --build
```

## PosgreSQL / postGISへのアクセス
1. VScodeのDocker extensionよりdocker-postgisのコンテナを確認、その下にある`docker-postgis_osm_db`を右クリックし、`Attach Visual Studio Code`を選択する。
1. 新たなVScodeが立ち上がり、dockerコンテナ内にアクセスすることができるようになる。
1. 新たな作業フォルダを `/gis` とする（ctrl (もしくはcommand) + o）。

## 停止
Dockerコンテナを停止するには、起動する際に用いたローカルの作業ディレクトリでTerminalで以下を実行する。
```
docker-compose down
```
もしくは、Docker extensionより、docker-postgisのコンテナの下にある`docker-postgresql-postgis-osm_db`を右クリックし、`stop`を実行する。

## Tutorial
詳細なチュートリアルは`/gis/pop_data/tutorial.md`を参照のこと