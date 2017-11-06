#!/bin/bash

psql <<EOF
\x
DROP DATABASE IF EXISTS scidash;
CREATE DATABASE scidash;
\c scidash;
CREATE EXTENSION IF NOT EXISTS hstore;

REVOKE ALL PRIVILEGES ON DATABASE scidash FROM scidash_admin;
DROP USER IF EXISTS scidash_admin;
CREATE USER scidash_admin WITH PASSWORD 'scidash_local_password';

GRANT ALL PRIVILEGES ON DATABASE scidash TO scidash_admin;
EOF
