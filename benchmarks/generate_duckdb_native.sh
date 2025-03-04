#! /usr/bin/env bash

../osv/benchmarks/duckdb/duckdb/build/release/duckdb -c "CALL dbgen(sf=$1)" "$XDG_DATA_HOME"/"$1".db
