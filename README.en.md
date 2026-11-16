# Kakao Navigation Skill

[中文](README.md) | **English** | [한국어](README.ko.md)

An agent skill for reliable South Korea place research and automobile route planning with the official Kakao Local and Kakao Mobility REST APIs.

It helps AI agents resolve Korean places, disambiguate branches, geocode addresses, find nearby facilities, compare driving times, plan multi-stop routes, and use future-departure estimates without inventing unsupported walking or public-transit results.

## Install with an AI agent

Give the repository URL to a skill-capable coding agent. For example:

```text
帮我安装这个 skill：https://github.com/baofeidyz/kakao-navigation-skill
```

```text
Install this skill: https://github.com/baofeidyz/kakao-navigation-skill
```

### Instructions for AI agents

When a user asks to install this repository as a skill:

1. Treat the repository root as the skill directory because `SKILL.md` is at the root.
2. Install it as `kakao-navigation` in the agent's normal skills directory.
3. Do not copy `.git`, local caches, `.env` files, or credentials.
4. Tell the user that `KAKAO_REST_API_KEY` must be configured separately and that the skill becomes discoverable on the agent's next turn or session, according to the host agent.
5. Never ask the user to commit a REST API key to this repository.

For Codex installations using the built-in skill installer, the equivalent deterministic command is:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo baofeidyz/kakao-navigation-skill \
  --path . \
  --name kakao-navigation
```

If `CODEX_HOME` is unset, it normally defaults to `~/.codex`. The installer aborts rather than overwriting an existing skill; remove or update the existing installation deliberately.

### Manual installation

```bash
git clone https://github.com/baofeidyz/kakao-navigation-skill.git
mkdir -p ~/.codex/skills
rsync -a --exclude .git kakao-navigation-skill/ ~/.codex/skills/kakao-navigation/
```

Restart the agent or begin a new turn so it can discover the new skill.

## Configure Kakao access

1. Create an application in [Kakao Developers](https://developers.kakao.com/).
2. Create or select a REST API key and configure its allowed service information/IP restrictions as appropriate.
3. Export it only in the runtime environment:

```bash
export KAKAO_REST_API_KEY='your-rest-api-key'
```

Do not put the key in prompts, screenshots, shell history, `.env` files committed to Git, or example commands. If a key is exposed, rotate it in Kakao Developers.

## What the skill supports

- Keyword and category-based Kakao place search
- Address geocoding and reverse geocoding
- Administrative-region lookup and coordinate conversion
- Current automobile directions with up to five waypoints
- Future-departure automobile directions
- Multi-waypoint, multi-origin, and multi-destination route requests
- Travel-planning guidance that separates API evidence from planner assumptions

The public Kakao REST APIs covered here do **not** provide pedestrian or public-transit routing. The skill will not relabel automobile estimates as walking, subway, or bus results.

## CLI examples

Run commands from the installed skill directory:

```bash
python3 scripts/kakao_api.py keyword '경복궁' --size 3

python3 scripts/kakao_api.py category FD6 \
  --x 126.97689786832184 \
  --y 37.577613288258206 \
  --radius 1500 \
  --sort distance

python3 scripts/kakao_api.py directions \
  --origin 126.97689786832184,37.577613288258206 \
  --destination 127.027619208212,37.497952760023 \
  --priority RECOMMEND \
  --summary true
```

Inspect a request without a key or network call:

```bash
python3 scripts/kakao_api.py --dry-run keyword '경복궁 맛집' \
  --x 126.9769 --y 37.5776 --radius 1500 --sort distance
```

For all options:

```bash
python3 scripts/kakao_api.py --help
python3 scripts/kakao_api.py directions --help
```

## Repository layout

```text
.
├── SKILL.md                    Agent entry point and decision guidance
├── agents/openai.yaml          Skill UI metadata
├── references/
│   ├── local-api.md            Kakao Local API reference
│   ├── navigation-api.md       Kakao Mobility Directions reference
│   └── travel-planning.md      Evidence-based itinerary rules
└── scripts/
    ├── kakao_api.py            Dependency-free REST CLI
    └── test_kakao_api.py       Request-construction tests
```

## Validate before release

The CLI uses only the Python standard library.

```bash
python3 -m unittest -v scripts/test_kakao_api.py
python3 -m py_compile scripts/kakao_api.py scripts/test_kakao_api.py
python3 scripts/kakao_api.py --dry-run keyword '경복궁'
```

If Codex's `skill-creator` is installed, also run:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
```

Live API tests require `KAKAO_REST_API_KEY` and may consume account quota. Never run them in CI with an untrusted pull request context.

## Sources and maintenance

The endpoint assumptions are based on the current official documentation:

- [Kakao Local REST API](https://developers.kakao.com/docs/latest/ko/local/dev-guide)
- [Kakao Mobility Directions API](https://developers.kakaomobility.com/guide/navi-api/start)
- [Driving directions](https://developers.kakaomobility.com/guide/navi-api/directions)
- [Future driving directions](https://developers.kakaomobility.com/guide/navi-api/future)

Before changing endpoint hosts, request fields, limits, or authentication behavior, verify them against the official documentation. The older [`CaChiJ/kakao-navigation-mcp-server`](https://github.com/CaChiJ/kakao-navigation-mcp-server) informed the initial use cases, but this skill does not inherit its unsupported claim of walking-route support.

## License

[MIT](LICENSE)
