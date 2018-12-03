#!/bin/bash

current_date=$(date +'%m-%d-%Y')
db_name="scidash"
db_user="scidash_admin"
outfile="$current_date.backup"

docker exec scidash_scidash-postgres_1 bash -lc 'pg_dump $db_name -U $db_user' > ./$outfile
