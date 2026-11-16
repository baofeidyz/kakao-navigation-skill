#!/usr/bin/env python3
import importlib.util
import json
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

path = Path(__file__).with_name("kakao_api.py")
spec = importlib.util.spec_from_file_location("kakao_api", path)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class RequestTests(unittest.TestCase):
    def parse(self, argv):
        return api.make_parser().parse_args(argv)

    def test_keyword_encodes_korean_and_center(self):
        args = self.parse(["--dry-run", "keyword", "경복궁 맛집", "--x", "126.978", "--y", "37.566", "--radius", "1500", "--sort", "distance"])
        method, url, body = api.build_request(args)
        self.assertEqual(method, "GET")
        self.assertIsNone(body)
        query = parse_qs(urlparse(url).query)
        self.assertEqual(query["query"], ["경복궁 맛집"])
        self.assertEqual(query["radius"], ["1500"])

    def test_route_encodes_pipe_options(self):
        args = self.parse(["directions", "--origin", "127,37", "--destination", "128,36", "--waypoint", "127.5,36.5", "--avoid", "toll", "--avoid", "ferries", "--summary", "true"])
        _, url, _ = api.build_request(args)
        query = parse_qs(urlparse(url).query)
        self.assertEqual(query["avoid"], ["toll|ferries"])
        self.assertEqual(query["waypoints"], ["127.5,36.5"])
        self.assertEqual(query["summary"], ["true"])

    def test_radius_requires_center(self):
        args = self.parse(["keyword", "카페", "--radius", "1000"])
        with self.assertRaises(ValueError):
            api.build_request(args)

    def test_post_body_must_be_object(self):
        args = self.parse(["post-route", "destinations", "--body-json", json.dumps([])])
        with self.assertRaises(ValueError):
            api.build_request(args)


if __name__ == "__main__":
    unittest.main()
