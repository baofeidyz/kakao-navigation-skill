# Kakao Mobility Directions REST API

Official start guide: https://developers.kakaomobility.com/guide/navi-api/start

Official endpoint guide: https://developers.kakaomobility.com/guide/navi-api/directions

Use the official hostname `https://apis-navi.kakaomobility.com`; do not pin an IP address. Authenticate with `Authorization: KakaoAK ${KAKAO_REST_API_KEY}` and use `Content-Type: application/json` for POST bodies.

These are automobile-routing APIs. They are not walking or public-transit APIs.

## Endpoint selection

| Purpose | Method and path | Limit / result |
|---|---|---|
| Current driving route | `GET /v1/directions` | 1 origin, 1 destination, up to 5 waypoints; detail or summary |
| Many waypoints | `POST /v1/waypoints/directions` | Up to 30 waypoints; detail or summary |
| Many origins to one destination | `POST /v1/origins/directions` | Up to 30 origins; duration/distance summaries |
| One origin to many destinations | `POST /v1/destinations/directions` | Up to 30 destinations; duration/distance summaries |
| Future departure | `GET /v1/future/directions` | 1 origin, 1 destination, up to 5 waypoints |

The ordinary current route allows at most 5 waypoints and requires total route distance below 1,500 km. Multi-location quotas and pricing may differ by account; never assume affiliate limits apply to the standard API.

## GET route parameters

- `origin`: `x,y`, optionally followed by `name=...` or `angle=0..360` as documented.
- `destination`: `x,y`, optionally `name=...`.
- `waypoints`: join up to five `x,y` items with `|`.
- `priority`: `RECOMMEND` (default), `TIME`, or `DISTANCE`.
- `avoid`: one or more of `ferries`, `toll`, `motorway`, `schoolzone`, `uturn`, joined by `|`.
- `roadevent`: `0` reflects full road closures; `1` ignores full closures near endpoints; `2` ignores all full closures. Default is `0`.
- `alternatives`: request alternative routes.
- `road_details`: include detailed road data when details are returned.
- `car_type`: vehicle class integer; consult the official reference before changing the default.
- `car_fuel`: `GASOLINE`, `DIESEL`, or `LPG`.
- `car_hipass`: Hi-Pass availability.
- `summary`: when true, omit heavy bound/roads/guides detail.
- Future only: `departure_time` in `yyyyMMddHHmm` form according to the current official guide; interpret it in Korea time and verify the supported future range before relying on it.

Use URL encoding. Do not concatenate user text into a URL manually.

## POST body patterns

Pass JSON to `post-route` with `--body-file` or standard input. Confirm exact fields in the endpoint guide before unusual requests.

Multi-destination example:

```json
{
  "origin": {"name": "start", "x": 127.0276, "y": 37.4979},
  "destinations": [
    {"key": "a", "x": 126.9780, "y": 37.5665},
    {"key": "b", "x": 126.9850, "y": 37.5700}
  ],
  "radius": 10000,
  "priority": "TIME"
}
```

Avoid options in POST bodies are arrays, not a pipe-delimited GET string. Keys on origins/destinations identify results; choose stable unique values.

## Reading responses

For a standard route, inspect every entry in `routes`:

- `result_code` and `result_msg` indicate route-level success/failure.
- `summary.distance` is meters; `summary.duration` is seconds.
- `summary.fare.taxi` and `summary.fare.toll` are won-denominated estimates.
- `sections` split the route at waypoints. Detailed `roads` and `guides` appear only when requested and supported by `summary=false`.
- When `alternatives=true`, compare routes instead of silently picking array item zero.

Multi-origin/multi-destination endpoints return summaries for ranking candidates. Request a normal route afterward if turn-level detail is needed.
