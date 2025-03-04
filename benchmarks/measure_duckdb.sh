#! /usr/bin/env bash

taskset -c 0-63 ../osv/scripts/run.py -c 64 -m 200G -e "/duckdb -f /tpch.sql 30.db"
