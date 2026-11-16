#!/usr/bin/env python3
"""Dependency-free CLI for Kakao Local and Mobility REST APIs."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

LOCAL = "https://dapi.kakao.com"
NAVI = "https://apis-navi.kakaomobility.com"
POST_PATHS = {
    "waypoints": "/v1/waypoints/directions",
    "origins": "/v1/origins/directions",
    "destinations": "/v1/destinations/directions",
}


def bool_text(value):
    value = value.lower()
    if value not in {"true", "false"}:
        raise argparse.ArgumentTypeError("expected true or false")
    return value


def add_center(p):
    p.add_argument("--x", help="center longitude")
    p.add_argument("--y", help="center latitude")
    p.add_argument("--radius", type=int, choices=range(0, 20001), metavar="0..20000")
    p.add_argument("--rect", help="min_x,min_y,max_x,max_y")
    p.add_argument("--page", type=int, choices=range(1, 46))
    p.add_argument("--size", type=int, choices=range(1, 16))
    p.add_argument("--sort", choices=["accuracy", "distance"])


def add_route_options(p, future=False):
    p.add_argument("--origin", required=True, help="x,y (longitude,latitude)")
    p.add_argument("--destination", required=True, help="x,y (longitude,latitude)")
    p.add_argument("--waypoint", action="append", default=[], help="x,y; repeat up to 5 times")
    p.add_argument("--priority", choices=["RECOMMEND", "TIME", "DISTANCE"])
    p.add_argument("--avoid", action="append", choices=["ferries", "toll", "motorway", "schoolzone", "uturn"])
    p.add_argument("--roadevent", choices=[0, 1, 2], type=int)
    p.add_argument("--alternatives", type=bool_text)
    p.add_argument("--road-details", type=bool_text)
    p.add_argument("--car-type", type=int)
    p.add_argument("--car-fuel", choices=["GASOLINE", "DIESEL", "LPG"])
    p.add_argument("--car-hipass", type=bool_text)
    p.add_argument("--summary", type=bool_text)
    if future:
        p.add_argument("--departure-time", required=True, help="Korea time, yyyyMMddHHmm")


def make_parser():
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--dry-run", action="store_true", help="print request without sending it")
    sub = root.add_subparsers(dest="command", required=True)

    p = sub.add_parser("keyword", help="search places by keyword")
    p.add_argument("query")
    p.add_argument("--category")
    add_center(p)

    p = sub.add_parser("category", help="search nearby places by category code")
    p.add_argument("category_group_code")
    add_center(p)

    p = sub.add_parser("address", help="geocode an address")
    p.add_argument("query")
    p.add_argument("--analyze-type", choices=["similar", "exact"])
    p.add_argument("--page", type=int, choices=range(1, 46))
    p.add_argument("--size", type=int, choices=range(1, 31))

    for name, help_text in [("reverse", "coordinate to address"), ("region", "coordinate to region code")]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("x")
        p.add_argument("y")
        p.add_argument("--input-coord")

    p = sub.add_parser("transcoord", help="convert coordinate systems")
    p.add_argument("x")
    p.add_argument("y")
    p.add_argument("--input-coord", default="WGS84")
    p.add_argument("--output-coord", required=True)

    p = sub.add_parser("directions", help="current automobile route")
    add_route_options(p)
    p = sub.add_parser("future-directions", help="future automobile route")
    add_route_options(p, future=True)

    p = sub.add_parser("post-route", help="advanced POST route endpoint")
    p.add_argument("kind", choices=sorted(POST_PATHS))
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--body-file", type=Path)
    source.add_argument("--body-json")
    source.add_argument("--stdin", action="store_true")
    return root


def compact(values):
    return {key: value for key, value in values.items() if value is not None}


def validate_center(params):
    x, y, radius = params.get("x"), params.get("y"), params.get("radius")
    if (x is None) != (y is None):
        raise ValueError("--x and --y must be supplied together")
    if radius is not None and x is None:
        raise ValueError("--radius requires --x and --y")
    if params.get("sort") == "distance" and x is None:
        raise ValueError("--sort distance requires --x and --y")


def build_request(a):
    d = vars(a)
    if a.command in {"keyword", "category"}:
        params = compact({key: d.get(key) for key in ("x", "y", "radius", "rect", "page", "size", "sort")})
        validate_center(params)
        if a.command == "keyword":
            params.update(compact({"query": a.query, "category_group_code": a.category}))
            path = "/v2/local/search/keyword.json"
        else:
            params["category_group_code"] = a.category_group_code
            path = "/v2/local/search/category.json"
        return "GET", LOCAL + path + "?" + urllib.parse.urlencode(params), None
    if a.command == "address":
        params = compact({"query": a.query, "analyze_type": a.analyze_type, "page": a.page, "size": a.size})
        return "GET", LOCAL + "/v2/local/search/address.json?" + urllib.parse.urlencode(params), None
    if a.command in {"reverse", "region"}:
        path = "/v2/local/geo/coord2address.json" if a.command == "reverse" else "/v2/local/geo/coord2regioncode.json"
        params = compact({"x": a.x, "y": a.y, "input_coord": a.input_coord})
        return "GET", LOCAL + path + "?" + urllib.parse.urlencode(params), None
    if a.command == "transcoord":
        params = {"x": a.x, "y": a.y, "input_coord": a.input_coord, "output_coord": a.output_coord}
        return "GET", LOCAL + "/v2/local/geo/transcoord.json?" + urllib.parse.urlencode(params), None
    if a.command in {"directions", "future-directions"}:
        if len(a.waypoint) > 5:
            raise ValueError("GET directions supports at most 5 --waypoint values")
        params = compact({
            "origin": a.origin, "destination": a.destination,
            "waypoints": "|".join(a.waypoint) if a.waypoint else None,
            "priority": a.priority, "avoid": "|".join(a.avoid) if a.avoid else None,
            "roadevent": a.roadevent, "alternatives": a.alternatives,
            "road_details": a.road_details, "car_type": a.car_type,
            "car_fuel": a.car_fuel, "car_hipass": a.car_hipass, "summary": a.summary,
            "departure_time": getattr(a, "departure_time", None),
        })
        path = "/v1/future/directions" if a.command == "future-directions" else "/v1/directions"
        return "GET", NAVI + path + "?" + urllib.parse.urlencode(params), None
    if a.body_file:
        body = json.loads(a.body_file.read_text(encoding="utf-8"))
    elif a.body_json:
        body = json.loads(a.body_json)
    else:
        body = json.load(sys.stdin)
    if not isinstance(body, dict):
        raise ValueError("POST body must be a JSON object")
    return "POST", NAVI + POST_PATHS[a.kind], body


def send(method, url, body, dry_run):
    if dry_run:
        print(json.dumps({"method": method, "url": url, "body": body}, ensure_ascii=False, indent=2))
        return 0
    key = os.environ.get("KAKAO_REST_API_KEY")
    if not key:
        print("KAKAO_REST_API_KEY is not set", file=sys.stderr)
        return 2
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "KakaoAK " + key,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "kakao-navigation-skill/1.0",
    })
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print(json.dumps(json.load(response), ensure_ascii=False, indent=2))
            return 0
    except urllib.error.HTTPError as error:
        text = error.read().decode("utf-8", "replace")
        print(json.dumps({"http_status": error.code, "reason": error.reason, "body": text}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError) as error:
        print("network error: " + str(error), file=sys.stderr)
        return 1


def main():
    a = make_parser().parse_args()
    try:
        method, url, body = build_request(a)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print("request error: " + str(error), file=sys.stderr)
        return 2
    return send(method, url, body, a.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
