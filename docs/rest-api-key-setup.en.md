# Kakao REST API key setup tutorial

[中文](rest-api-key-setup.md) | **English** | [한국어](rest-api-key-setup.ko.md)

This tutorial configures the Kakao REST API key required by this skill for Kakao Local place data and Kakao Mobility automobile directions. The earlier [`CaChiJ/kakao-navigation-mcp-server`](https://github.com/CaChiJ/kakao-navigation-mcp-server) setup informed the original flow; the steps below follow Kakao's current interface and policies.

## 1. Sign in to Kakao Developers

1. Open [Kakao Developers](https://developers.kakao.com/).
2. Sign in with a Kakao account or create one.
3. Open app management.

## 2. Create an application

1. Select **App** at the top.
2. Select **Create app**.
3. Enter the required app and developer or company information, then save.

Kakao normally creates several key types. This skill uses only a **REST API key**. Do not substitute a JavaScript, Native App, or Admin key.

## 3. Activate the Kakao Map API

Place search, geocoding, and coordinate conversion are Kakao Map REST APIs:

1. Open the new application.
2. Go to **Kakao Map → Usage settings**.
3. Set the status to `ON`.

Kakao changed Map API usage and free-quota rules on July 21, 2026. The first app that activates Kakao Map API under a developer account can receive the free-quota badge. Later apps, or usage beyond the free quota, may require a connected Biz Wallet and paid API setting. Follow the status shown in your console and the [official Kakao Map guide](https://developers.kakao.com/docs/en/kakaomap/common).

## 4. Create or retrieve a REST API key

Kakao reorganized app-key menus on December 3, 2025. The current path is:

1. Go to **App → select the app → App → Platform Key**.
2. Select the existing REST API key or **Add REST API key**.
3. Give it a recognizable name, such as `kakao-navigation-local`.
4. Confirm that the key is active and copy its value.

Treat the value as a credential. Do not commit it to GitHub or place it in `SKILL.md`, a README, source code, or a public `.env` file.

### Client Secret

A new REST API key may have Client Secret enabled by default. Client Secret is mainly relevant to OAuth token requests such as Kakao Login. This skill's Local and Directions calls use the `Authorization: KakaoAK ...` header and do not require passing Client Secret to the script. An Admin key is not a substitute.

## 5. Configure allowed IP addresses

Allowed IPs reduce damage if a key leaks, but a wrong entry also blocks a local agent.

1. Go to **App → Platform Key → select the REST API key → Allowed IP address**.
2. For production, enter the server's fixed egress IP or an appropriate CIDR.
3. If a local development IP changes frequently, verify the API first and then tighten the restriction.
4. Save the setting.

Kakao currently allows up to 10 entries and accepts IPv4, CIDR, or subnet-mask forms. After registration, calls from other addresses fail. For `ip mismatched` or `-401`, check the real egress IP or temporarily remove incorrect allowed-IP entries and retest.

## 6. Check Kakao Mobility Directions access

Automobile directions use the same Kakao Developers REST API key. Check the [Kakao Mobility Directions getting-started guide](https://developers.kakaomobility.com/en/guide/navi-api/start) and your account console for pricing, quota, and service status.

Always use the official hostname; do not pin an IP or add a hosts-file mapping:

```text
https://apis-navi.kakaomobility.com
```

The public Directions REST API provides automobile routes, not walking or public-transit routes.

## 7. Configure the key locally

For the current terminal only:

```bash
export KAKAO_REST_API_KEY='your REST API key'
```

Check presence without printing the value:

```bash
test -n "$KAKAO_REST_API_KEY" && echo 'KAKAO_REST_API_KEY is set'
```

For persistent use, prefer an OS keychain, CI secret, or protected environment configuration. Do not commit `.env`; this repository ignores it.

## 8. Verify place search

From the skill root:

```bash
python3 scripts/kakao_api.py keyword '경복궁' --size 3
```

A successful response contains `documents` with `place_name`, addresses, `x` longitude, `y` latitude, and a Kakao Place URL.

Inspect the request without a key or network call:

```bash
python3 scripts/kakao_api.py --dry-run keyword '경복궁'
```

## 9. Verify automobile directions

Use coordinates returned by place search, always in `longitude,latitude` order:

```bash
python3 scripts/kakao_api.py directions \
  --origin 126.97689786832184,37.577613288258206 \
  --destination 127.027619208212,37.497952760023 \
  --priority RECOMMEND \
  --summary true
```

Success returns `result_code: 0` and `길찾기 성공` in `routes`, with distance, duration, taxi-fare, and toll estimates. Duration varies with traffic and request time.

## Troubleshooting

| Symptom | Check |
|---|---|
| `KAKAO_REST_API_KEY is not set` | Export the variable in the current terminal |
| HTTP `401` or Kakao `-401` | Wrong key type, inactive key, allowed-IP mismatch, or copy error |
| `appKeyType is ADMIN_KEY` | Replace the Admin key with a REST API key |
| Local API product/permission error | Kakao Map activation, Biz Wallet/paid setting, and quota |
| `429` | Stop retrying and inspect rate/quota state |
| Place search works but directions fail | Check Kakao Map and Kakao Mobility status, quota, and request parameters separately |
| No place results | Try the Korean name, remove an overly small radius, or add the district |

## Security checklist

- Rotate a key immediately if it appears in chat, screenshots, public logs, or Git history.
- Do not place a key in URL query parameters. This skill uses the `Authorization` header.
- Restrict production keys by allowed IP and monitor quota and anomalous calls.
- Never expose secrets to CI triggered by untrusted pull requests.

## Official documentation

- [Kakao REST API getting started](https://developers.kakao.com/docs/en/rest-api/getting-started)
- [App and REST API key settings](https://developers.kakao.com/docs/en/app-setting/app)
- [Kakao Map usage](https://developers.kakao.com/docs/en/kakaomap/common)
- [2025 app and key changes](https://developers.kakao.com/docs/en/getting-started/app-key-migration)
- [Kakao Mobility Directions getting started](https://developers.kakaomobility.com/en/guide/navi-api/start)
