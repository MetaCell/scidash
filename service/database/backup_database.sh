#!/bin/bash
pg_dump -U postgres -Fc scidash  | gzip > /var/lib/postgresql/scidash.`date +"%Y-%m-%d_%H-%M-%S"`.db.gz