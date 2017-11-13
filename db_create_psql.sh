#!/bin/bash

psql -d template1 -c 'create extension hstore;'

psql <<EOF
\x
DROP DATABASE IF EXISTS scidash;
CREATE DATABASE scidash;
\c scidash;

REVOKE ALL PRIVILEGES ON DATABASE scidash FROM scidash_admin;
DROP USER IF EXISTS scidash_admin;
CREATE USER scidash_admin WITH PASSWORD 'scidash_local_password';

GRANT ALL PRIVILEGES ON DATABASE scidash TO scidash_admin;
ALTER USER scidash_admin CREATEDB
EOF
