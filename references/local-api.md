# Kakao Local REST API

Official guide: https://developers.kakao.com/docs/latest/ko/local/dev-guide

Host: `https://dapi.kakao.com`

Authorization: `Authorization: KakaoAK ${KAKAO_REST_API_KEY}`

Default coordinate system: `WGS84`. For WGS84, `x` is longitude and `y` is latitude.

## Endpoints

| Purpose | Method and path | Required values |
|---|---|---|
| Address to coordinate | `GET /v2/local/search/address.json` | `query` |
| Coordinate to region code | `GET /v2/local/geo/coord2regioncode.json` | `x`, `y` |
| Coordinate to address | `GET /v2/local/geo/coord2address.json` | `x`, `y` |
| Coordinate conversion | `GET /v2/local/geo/transcoord.json` | `x`, `y`, usually `input_coord`, `output_coord` |
| Keyword place search | `GET /v2/local/search/keyword.json` | `query` |
| Category place search | `GET /v2/local/search/category.json` | `category_group_code`; use center `x`,`y` and `radius` for nearby search |

## Search parameters

- `x`, `y`: WGS84 center. Provide both.
- `radius`: 0–20,000 meters. Use with `x` and `y`.
- `rect`: `min_x,min_y,max_x,max_y`; do not combine casually with radius.
- `page`: 1–45.
- `size`: 1–15 for place search.
- `sort`: `accuracy` or `distance`. `distance` requires a center.
- `category_group_code`: optional filter for keyword search, required for category search.

Category group codes:

| Code | Meaning |
|---|---|
| `MT1` | Large mart |
| `CS2` | Convenience store |
| `PS3` | Kindergarten/daycare |
| `SC4` | School |
| `AC5` | Academy |
| `PK6` | Parking |
| `OL7` | Gas or charging station |
| `SW8` | Subway station |
| `BK9` | Bank |
| `CT1` | Culture facility |
| `AG2` | Real-estate agency |
| `PO3` | Public institution |
| `AT4` | Tourist attraction |
| `AD5` | Accommodation |
| `FD6` | Food/dining |
| `CE7` | Cafe |
| `HP8` | Hospital |
| `PM9` | Pharmacy |

Keyword/category documents include `id`, `place_name`, hierarchical `category_name`, phone, address, road address, `x`, `y`, `place_url`, and sometimes `distance`. Check `meta.is_end` before paging. Search ranking is relevance data, not proof that the first result is the intended place.

Address search is for address strings. For landmarks, restaurants, hotels, station names, and attractions, use keyword search first.

Coordinate conversion supports `WGS84`, `WCONGNAMUL`, `CONGNAMUL`, `WTM`, `TM`, `KTM`, `UTM`, `BESSEL`, `WKTM`, and `WUTM`; consult the official guide before using a non-WGS84 system.
