## run a container from docker-hub
```sh
## pull postgres image
## set password 
## rename to postgres-docker as container name
## expose to external port 5432
## running in the background
docker run --name postgres-docker -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```

## build customised postgres image

dockerfile
```
FROM postgres 
ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB testdb 
COPY init.sql /docker-entrypoint-initdb.d/
```

```sh
## use this command to build the image
docker build -t my-postgres-image .

## run as container
docekr run -d --name my-postgres-container -p 5555:5432 my-postgres-image
```

## how to persist data
```sh
## rename a volumn
docker run -d --name my-postgres-volume -p 7777:5432 -v postgres-volume:/var/lib/postgresql/data my-postgres-image

## use inpect to check mounted volumn
docker container inspect my-postgres-volume

## check volumn
docker volume ls 

## create first then do the mounting
docker volume create --name my-postgres-volume
docker run -d --name my-postgres-volume-2 -p 2222:5432 -v my-postgres-volume:/var/lib/postgresql/data my-postgres-image

## attach to a different volume
docker run -d --name my-postgres-volume-3 -p 3333:5432 -v my-postgres-volume:/var/lib/postgresql/data my-postgres-image

```
if we are mounting a volume to different containers, new data to one of the container may not be refreshed to others. 
**Need to stop containers and do a start**
```
$ docker stop container my-postgres-volume-2
$ docker stop container my-postgres-volume-3
$ docker start my-postgres-volume-3
```

### remove unused volumes
```
docker volume rm {volume_name}

## remove all volumes
docker volume prune
```

## run sql scripts using docker command
```
docker exec -it container_name psql -U username -W password dbname

## docker exec -i container_name psql -U user_name
```


### run scripts inside postgres container
pul sql scripts in folder `/docker-entrypoint-initdb.d`

```sql
-- init.sql
create user docker;
create databases docker;
grant all privileges on database docker to docker;	
```

Dockerfile
```sh
FROM library/postgres 
copy init.sql /docker-entrypoint-initdb.d/
```

New Dockerfile since Jul 8 2015
```
FROM library/postgres 
ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB docker
```

## using docker-compose

folder structure
```
$MYAPP_ROOT/docker-compose.yml
           /Docker/init.sql
           /Docker/db.Dockerfile
```

- docker-compose.yml

```
version: "3.3"
services:
  db:
    build:
      context: ./Docker
      dockerfile: db.Dockerfile
    volumes:
      - ./var/pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

```

- Docker/init.sql
```
CREATE USER myUser;

CREATE DATABASE myApp_dev;
GRANT ALL PRIVILEGES ON DATABASE myApp_dev TO myUser;

CREATE DATABASE myApp_test;
GRANT ALL PRIVILEGES ON DATABASE myApp_test TO myUser;

```

- Docker/db.Dockerfile

```
FROM postgres:11.5-alpine
COPY init.sql /docker-entrypoint-initdb.d/
```

how to start
```
docker-compose -f docker-compose.yml up --no-start
docker-compose -f docker-compose.yml start

```

## neat version of docker-compose
sql scripts
```bash
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER docker;
    CREATE DATABASE my_project_development;
    GRANT ALL PRIVILEGES ON DATABASE my_project_development TO docker;
    CREATE DATABASE my_project_test;
    GRANT ALL PRIVILEGES ON DATABASE my_project_test TO docker;
EOSQL
```

docker-compose file
```
version: '3.4'

services:
  postgres:
    image: postgres
    restart: unless-stopped
    volumes:
      - postgres:/var/lib/postgresql/data
      - ./init-database.sh:/docker-entrypoint-initdb.d/init-database.sh
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - 5432:5432

volumes:
  postgres:

```


## truncate all tables in postgres
```
REATE OR REPLACE FUNCTION truncate_tables(username IN VARCHAR) RETURNS void AS $$
DECLARE
    statements CURSOR FOR
        SELECT tablename FROM pg_tables
        WHERE tableowner = username AND schemaname = 'public';
BEGIN
    FOR stmt IN statements LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- SELECT truncate_tables('MYUSER');
```


if implicit cursor is required
```
CREATE OR REPLACE FUNCTION f_truncate_tables(_username text)
  RETURNS void AS
$func$
DECLARE
   _tbl text;
   _sch text;
BEGIN
   FOR _sch, _tbl IN 
      SELECT schemaname, tablename
      FROM   pg_tables
      WHERE  tableowner = _username
      AND  
      -- dangerous, test before you execute!
      RAISE NOTICE '%',  -- once confident, comment this line ...
      -- EXECUTE         -- ... and uncomment this one
         format('TRUNCATE TABLE %I.%I CASCADE', _sch, _tbl);
   END LOOP;
END
$func$ LANGUAGE plpgsql;
```

using one single query

```
CREATE OR REPLACE FUNCTION f_truncate_tables(_username text)
  RETURNS void AS
$func$
BEGIN
   -- dangerous, test before you execute!
   RAISE NOTICE '%',  -- once confident, comment this line ...
   -- EXECUTE         -- ... and uncomment this one
  (SELECT 'TRUNCATE TABLE '
       || string_agg(format('%I.%I', schemaname, tablename), ', ')
       || ' CASCADE'
   FROM   pg_tables
   WHERE  tableowner = _username
   AND    schemaname = 'public'
   );
END
$func$ LANGUAGE plpgsql;

-- SELECT truncate_tables('postgres');
```

## dump psql schema 
```sql
-- create schema dump of db
pg_dump mydb -s > schema.sql

-- drop db 
drop database mydb;

-- create db 
create database mydb;

-- import schema 
psql mydb < schema.sql	
```


## reference
https://blog.yugabyte.com/part-1-deploying-a-distributed-sql-backend-for-apache-airflow-on-google-cloud/
