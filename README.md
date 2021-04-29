# Sandwalker

Explorer of Pocket rewards.

## SQL Migration

Migrate the schema:

```
sqlite> CREATE TABLE new_timeline(id INTEGER PRIMARY KEY AUTOINCREMENT, account TEXT, block INTEGER, amount INTEGER);
sqlite> INSERT INTO new_timeline(account, block, amount) SELECT account, block, amount FROM timeline;
```
