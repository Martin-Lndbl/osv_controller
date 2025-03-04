#! /usr/bin/env bash

../osv/scripts/run.py -c 64 -m 200G -e "/duckdb -c \"CALL dbgen(sf=$1)\" $1.db"
