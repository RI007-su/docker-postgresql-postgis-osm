#!/bin/sh
docker-compose exec db bash -c "chmod 775 docker-entrypoint-initdb.d/init-database.sh"
docker-compose exec db bash -c "./docker-entrypoint-initdb.d/init-database.sh"

#docker-compose exec db bash -c "chmod 775 docker-entrypoint-initdb.d/dvdrental_db.sh"
#docker-compose exec db bash -c "./docker-entrypoint-initdb.d/dvdrental_db.sh"

docker-compose exec db bash -c "chmod 775 docker-entrypoint-initdb.d/osm_db.sh"
docker-compose exec db bash -c "./docker-entrypoint-initdb.d/osm_db.sh"
