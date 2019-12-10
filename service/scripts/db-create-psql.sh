#!/bin/bash

git clone https://github.com/ddelpiano/scidash-artifacts
cd scidash-artifacts/database
gunzip `ls | head -n 1`
pg_restore --clean -d scidash `ls *db | head -n 1`
