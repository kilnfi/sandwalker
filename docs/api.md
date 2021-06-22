# API

## Reward History

Retrieves the reward history of a list of addresses between two timestamps.

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

## Success Responses

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
     http://sandwalker/api/rewards
```

```
{"accounts":{"f1829676db577682e944fc3493d451b67ff3e29f":[{"block":50,"reward":83600,"time":"Wed, 29 Jul 2020 03:00:26 GMT"},{"block":50,"reward":45100,"time":"Wed, 29 Jul 2020 03:00:26 GMT"},{"block":74,"reward":13200,"time":"Wed, 29 Jul 2020 09:00:37 GMT"},{"block":74,"reward":13200,"time":"Wed, 29 Jul 2020 09:00:37 GMT"},{"block":86,"reward":55000,"time":"Wed, 29 Jul 2020 12:00:43 GMT"},{"block":86,"reward":45100,"time":"Wed, 29 Jul 2020 12:00:43 GMT"},{"block":90,"reward":19800,"time":"Wed, 29 Jul 2020 13:00:45 GMT"},{"block":94,"reward":17600,"time":"Wed, 29 Jul 2020 14:00:47 GMT"},{"block":126,"reward":13200,"time":"Wed, 29 Jul 2020 22:01:06 GMT"}]}}
```