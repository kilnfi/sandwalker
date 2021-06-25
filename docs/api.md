# API

## Reward History

Retrieves the reward history of a list of addresses between two (optional) timestamps.

**URL** : `/api/rewards`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "accounts": ["pocket address", "another Pocket address"],
    "start_date": "YYYY-MM-DD HH:M:S",
    "end_date": "YYYY-MM-DD HH:M:S"
}
```

**Data example** Partial data is allowed.

```json
{
    "accounts": ["f1829676db577682e944fc3493d451b67ff3e29f"],
}
```

## Success Response

**Code** : `200 OK`

**Content example** : For the example above...

```json
{
    "accounts": {
        "f1829676db577682e944fc3493d451b67ff3e29f": [
    	    {"block": 50, "reward": 83600, "time": "Wed, 29 Jul 2020 03:00:26 GMT"},
	    {"block": 50, "reward": 45100, "time": "Wed, 29 Jul 2020 03:00:26 GMT"},
	    {"block": 74, "reward": 13200, "time": "Wed, 29 Jul 2020 09:00:37 GMT"},
	    {"block": 74, "reward": 13200, "time": "Wed, 29 Jul 2020 09:00:37 GMT"},
	    {"block": 86, "reward": 55000, "time": "Wed, 29 Jul 2020 12:00:43 GMT"},
	    {"block": 86, "reward": 45100, "time": "Wed, 29 Jul 2020 12:00:43 GMT"},
	    {"block": 90, "reward": 19800, "time": "Wed, 29 Jul 2020 13:00:45 GMT"},
	    {"block": 94, "reward": 17600, "time": "Wed, 29 Jul 2020 14:00:47 GMT"}
	  ]
    }
}
```

## Error Response

**Condition** : Invalid parameters in the request

**Code** : `400 BAD REQUEST`

**Content** : `{"error":"Invalid request: no Pocket accounts specified"}`

## Notes

- if `start_date` is not provided, it defaults to `1970-01-01 00:00:00`.
- if `end_date` is not provided, it defaults to `now`.

## Examples

### Bash

```
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"accounts": ["f1829676db577682e944fc3493d451b67ff3e29f"]}' \
     https://sandwalker.sbrk.org/api/rewards
```

```
{"accounts":{"f1829676db577682e944fc3493d451b67ff3e29f":[{"block":50,"reward":83600,"time":"Wed, 29 Jul 2020 03:00:26 GMT"},{"block":50,"reward":45100,"time":"Wed, 29 Jul 2020 03:00:26 GMT"},{"block":74,"reward":13200,"time":"Wed, 29 Jul 2020 09:00:37 GMT"},{"block":74,"reward":13200,"time":"Wed, 29 Jul 2020 09:00:37 GMT"},{"block":86,"reward":55000,"time":"Wed, 29 Jul 2020 12:00:43 GMT"},{"block":86,"reward":45100,"time":"Wed, 29 Jul 2020 12:00:43 GMT"},{"block":90,"reward":19800,"time":"Wed, 29 Jul 2020 13:00:45 GMT"},{"block":94,"reward":17600,"time":"Wed, 29 Jul 2020 14:00:47 GMT"},{"block":126,"reward":13200,"time":"Wed, 29 Jul 2020 22:01:06 GMT"}]}}
```

## Rewards by Block

Retrieves the reward history of all nodes at a given block.

**URL** : `/api/block`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "block": 1262,
}
```

## Success Response

**Code** : `200 OK`

**Content example** : For the example above...

```json
{
  "entries": [
    {"account": "5bcae50364952a5fa3a8363f93f2adffc9eff42e", "reward": 41438400, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"},
    {"account": "f1829676db577682e944fc3493d451b67ff3e29f", "reward": 5121600, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"},
    {"account": "f1889ba5d43b6dfdd8a9460b9ca45beaca901aa6", "reward": 41420600, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"},
    {"account": "f1829676db577682e944fc3493d451b67ff3e29f", "reward": 5119400, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"},
    {"account": "a322d710892c3f7d730a7f5f02656dbebe1c6e47", "reward": 40592900, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"},
    {"account": "f1829676db577682e944fc3493d451b67ff3e29f", "reward": 5017100, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"},
    {"account": "4b965a477f108a26444865c4757931f7fabcea99", "reward": 42186000, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"},
    {"account": "f1829676db577682e944fc3493d451b67ff3e29f", "reward": 5214000, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"},
    {"account": "2c3499c840dc286b74fa090e00d29555bff101cb", "reward": 41616400, "time": "Mon, 10 Aug 2020 17: 36: 33 GMT"}
  ]
]
```

## Error Response

**Condition** : Invalid parameters in the request

**Code** : `400 BAD REQUEST`

**Content** : `{"error":"Invalid request: no block specified"}`

## Notes

The current block may yield incomplete data as it is currently being
processed by the chain. If you want to ensure 100% consistency, you
must first, query the Sandwalker height, and query block rewards up to
that height.

## Examples

### Bash

```
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"block": 1262}' \
     https://sandwalker.sbrk.org/api/block
```

```
["entries":{"account":"5bcae50364952a5fa3a8363f93f2adffc9eff42e","reward":41438400,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"f1829676db577682e944fc3493d451b67ff3e29f","reward":5121600,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"f1889ba5d43b6dfdd8a9460b9ca45beaca901aa6","reward":41420600,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"f1829676db577682e944fc3493d451b67ff3e29f","reward":5119400,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"a322d710892c3f7d730a7f5f02656dbebe1c6e47","reward":40592900,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"f1829676db577682e944fc3493d451b67ff3e29f","reward":5017100,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"4b965a477f108a26444865c4757931f7fabcea99","reward":42186000,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"f1829676db577682e944fc3493d451b67ff3e29f","reward":5214000,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"2c3499c840dc286b74fa090e00d29555bff101cb","reward":41616400,"time":"Mon, 10 Aug 2020 17:36:33 GMT"},{"account":"f1829676db577682e944fc3493d451b67ff3e29f","reward":5143600,"time":"Mon, 10 Aug 2020 17:36:33 GMT"}}]
```

## Height

Retrieves the blockchain height of the Sandwalker.

**URL** : `/api/height`

**Method** : `POST`, `GET`

**Auth required** : NO

## Success Response

**Code** : `200 OK`

**Content example** : For the example above...

```json
{
  "height": 24999
}
```

## Error Response

**Condition** : Sandwalker has not initialized yet and has no complete block synced

**Code** : `503 Service Unavailable`

**Content** : `{"error":"Sandwalker has not initialized yet and has no complete block synced"}`

## Notes

The block returned may be smaller than the actual Sandwalker height,
the data up to the returned height is guaranteed to be complete.

## Examples

### Bash

```
curl --header "Content-Type: application/json" \
     --request GET \
     https://sandwalker.sbrk.org/api/height
```

```
{"height":1261}
```