# Korea travel planning with Kakao evidence

## Evidence chain

For each important stop, retain:

- the exact Kakao `place_name` and `id`;
- road address and district;
- longitude/latitude;
- Kakao place URL;
- the query used and whether a nearby center constrained it.

For each driving leg, retain observation time, origin/destination IDs or coordinates, route priority, distance, duration, and route result message. Future predictions and current-traffic estimates are not guarantees.

## Quality rules

- Resolve hotels, stations, airports, restaurants, and similarly named branches before calculating routes.
- A straight-line `distance` in a place-search response is not route distance or travel time.
- Do not infer opening hours, closed days, ticket inventory, accessibility, or last admission from Local API data.
- Do not present driving duration as walking, taxi pickup time, bus/subway duration, or total door-to-door time.
- Add practical buffers separately and label them as planning assumptions.
- For islands or separated road networks, route APIs may fail; report that rather than estimating from coordinates.
- Prefer Korean names in API searches, but present the itinerary in the user's language and preserve Korean place names for navigation.

## Concise itinerary contract

For each day, give a logical stop order and explain the one or two important routing decisions. For each leg, label the mode and evidence source. Include verified Kakao place links where useful. End with uncertainties that need a current non-Kakao check, especially business hours, reservation status, transit timetables, and weather.
