#! /usr/bin/env bash

../osv/benchmarks/duckdb/duckdb/build/release/duckdb -c "CALL dbgen(sf=30)" "$XDG_DATA_HOME"/30.db
