#! /usr/bin/env bash

taskset -c 0-63 ../osv/benchmarks/duckdb/duckdb/build/release/duckdb -f ../osv/benchmarks/duckdb/tpch.sql "$XDG_DATA_HOME"/30.db
