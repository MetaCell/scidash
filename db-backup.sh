#!/bin/bash

current_date=$(date +'%m-%d-%Y')

outfile="$current_date.backup"

pg_dump -d $db_name > $outfile
