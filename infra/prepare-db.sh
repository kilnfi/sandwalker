#!/usr/bin/env bash

INPUT_SQL=${1?"Usage: $0 <input_sql> <output_db>"}
OUTPUT_DB=${2?"Usage: $0 <input_sql> <output_db>"}

sqlite3 $OUTPUT_DB < $INPUT_SQL
sqlite3 $OUTPUT_DB "CREATE TABLE new_timeline(id INTEGER PRIMARY KEY AUTOINCREMENT, account TEXT, block INTEGER, amount INTEGER);"
sqlite3 $OUTPUT_DB "INSERT INTO new_timeline(account, block, amount) SELECT account, block, amount FROM timeline WHERE txtype=0;"
sqlite3 $OUTPUT_DB "DROP TABLE timeline;"
sqlite3 $OUTPUT_DB "ALTER TABLE new_timeline RENAME TO timeline;"
