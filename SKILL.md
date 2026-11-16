---
name: kakao-navigation
description: Research Korean places and plan evidence-based itineraries with Kakao Local and Kakao Mobility REST APIs. Use for Korean place lookup, address or coordinate resolution, nearby category search, driving-time comparison, route ordering, multi-stop driving, or future-departure estimates. Do not claim Kakao REST results for walking or public transit because the public APIs covered here provide place data and automobile routing only.
---

# Kakao Navigation

Use Kakao's Korean place index and current automobile routing data to ground travel plans. Prefer API evidence over guessed coordinates, travel times, or place identity.

## Before calling

- Run `python3 scripts/kakao_api.py ...` from this skill directory.
- Read the REST key from `KAKAO_REST_API_KEY`. Never print, persist, or place it in a URL or command argument.
- If the key is absent, explain how to create a Kakao Developers app and set the environment variable. `--dry-run` may be used without a key to inspect a request safely.
- Treat API responses as current observations. Do not imply that search ranking, road traffic, availability, or business details remain fixed.

## Choose the operation

1. Resolve user wording with `keyword`. Korean spelling usually produces the most precise results; preserve the user's original text and try Korean variants when ambiguous.
2. Use `address` only for a postal or road-address query. It is not a general POI search.
3. Use `category` for nearby facilities such as food, lodging, parking, subway stations, or attractions. It requires a center coordinate; see [references/local-api.md](references/local-api.md).
4. Use `directions` for one origin, one destination, and up to five waypoints. Default to `--summary true` unless geometry or turn guidance is needed.
5. Use `future-directions` only when the departure time is in the supported future window and include Korean timezone context.
6. Use `post-route` for multi-waypoint, multi-origin, or multi-destination requests. Read [references/navigation-api.md](references/navigation-api.md) before composing the JSON body.

Run `python3 scripts/kakao_api.py <command> --help` for flags.

## Planning workflow

- Resolve every important stop to a Kakao place result. Confirm with name, category, road address, and coordinates instead of accepting the first textual match blindly.
- Disambiguate duplicate names by searching near the city, district, hotel, or previous stop with `--x`, `--y`, and `--radius`.
- Keep coordinates in `x,y` order: longitude first, latitude second. Kakao Local returns them as strings; pass them unchanged when possible.
- Compare candidate orders with multi-destination summaries or a small number of direction calls. Optimize for the user's priorities, not distance alone: fixed reservations, meal timing, accessibility, and geographic backtracking all matter.
- Report distance in km and duration in a human-readable form, while retaining raw meter/second values when precision matters.
- Distinguish evidence: Kakao place result, Kakao driving estimate, user-provided constraint, and planner inference. A route estimate does not prove opening hours, admission rules, or transit service.

## Important boundary

The documented public REST endpoints in this skill do not provide pedestrian or public-transit routing. Never relabel automobile results as walking, subway, bus, or transit results. For those modes, say that no Kakao REST route was verified and use another authorized source if available. Read [references/travel-planning.md](references/travel-planning.md) when producing an itinerary.

## Errors and stopping conditions

- `401/403`: verify the REST API key, key status, allowed IP settings, and product access. Do not retry repeatedly.
- Empty place results: broaden wording or remove the radius once; then ask for a district, address, or Kakao Map URL.
- Route result codes or unreachable endpoints: report the returned message and do not invent a time.
- `429`: stop and report quota/rate limiting. Do not loop.
- `5xx` or network failure: retry at most twice with a brief delay, then label the result unavailable.

## References

- Read [references/local-api.md](references/local-api.md) for place, address, reverse-geocoding, coordinate, paging, and category parameters.
- Read [references/navigation-api.md](references/navigation-api.md) for automobile endpoints, limits, JSON shapes, options, and response interpretation.
- Read [references/travel-planning.md](references/travel-planning.md) for itinerary-quality rules and a concise output contract.
