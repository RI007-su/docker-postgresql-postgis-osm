FROM postgis/postgis:14-3.1-alpine

# install osm2pgsql
RUN apk add --no-cache --virtual .osm2pgsql-build-deps \
    make \
    g++ \
    cmake \
    zlib-dev \
    expat-dev \
    bzip2-dev \
    libpq proj-dev \
    lua5.2-dev \
    boost-dev \
    postgresql-dev \
    git \
    clang-extra-tools \
    libintl \
    \
    && mkdir /home/root \
    && wget -O /home/root/osm2pgsql.tar.gz "https://github.com/openstreetmap/osm2pgsql/archive/master.tar.gz" \
    && tar \
        --extract \
        --file /home/root/osm2pgsql.tar.gz \
        --directory /home/root \
    && rm /home/root/osm2pgsql.tar.gz \
    && cd /home/root/osm2pgsql-master \
    && mkdir build && cd build \
    && cmake -DLUA_LIBRARY=/usr/lib/lua5.2/liblua.so .. \
    && make \
    && make install



