#! /usr/bin/env bash

make clean

make -f conf/Makefile

make V=1 stage1 \
 | grep -wE 'gcc|g\+\+|c\+\+' \
 | grep -w '\-c' \
 | sed 's|cd.*.\&\&||g' \
 | jq -nR '[inputs|{directory:".", command:., file: match(" [^ ]+$").string[1:]}]' \
 > compile_commands.json
