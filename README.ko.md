# Kakao Navigation Skill

[中文](README.md) | [English](README.en.md) | **한국어**

Kakao Local 및 Kakao Mobility 공식 REST API를 활용해 대한민국의 장소를 정확히 검색하고 자동차 경로를 계획하는 AI Agent용 Skill입니다.

Agent가 한국 장소와 지점을 구분하고, 주소와 좌표를 변환하고, 주변 시설을 검색하고, 자동차 이동 시간을 비교하고, 다중 경유 경로와 미래 출발 경로를 계획하도록 돕습니다. 확인되지 않은 좌표를 추측하거나 자동차 경로를 도보·대중교통 결과로 표시하지 않습니다.

## AI Agent로 설치하기

Skill을 지원하는 Agent에게 저장소 URL을 전달합니다.

```text
이 skill을 설치해 주세요: https://github.com/baofeidyz/kakao-navigation-skill
```

```text
Install this skill: https://github.com/baofeidyz/kakao-navigation-skill
```

### AI Agent용 설치 지침

사용자가 이 저장소를 Skill로 설치해 달라고 요청하면 다음을 따릅니다.

1. `SKILL.md`가 있는 저장소 루트를 Skill 디렉터리로 사용합니다.
2. Agent의 표준 Skills 디렉터리에 `kakao-navigation`이라는 이름으로 설치합니다.
3. `.git`, 로컬 캐시, `.env`, 자격 증명을 복사하지 않습니다.
4. `KAKAO_REST_API_KEY`는 별도로 설정해야 하며, 호스트 Agent에 따라 다음 턴 또는 재시작 후 Skill이 검색될 수 있음을 알립니다.
5. REST API 키를 저장소에 커밋하도록 요청하지 않습니다.

Codex 내장 Skill Installer의 동일한 명령은 다음과 같습니다.

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo baofeidyz/kakao-navigation-skill \
  --path . \
  --name kakao-navigation
```

대상 디렉터리가 이미 있으면 설치기는 덮어쓰지 않고 중단합니다. 기존 설치의 제거 또는 업데이트는 사용자가 명시적으로 수행해야 합니다.

### 수동 설치

```bash
git clone https://github.com/baofeidyz/kakao-navigation-skill.git
mkdir -p ~/.codex/skills
rsync -a --exclude .git kakao-navigation-skill/ ~/.codex/skills/kakao-navigation/
```

설치 후 Agent를 다시 시작하거나 새 턴을 시작해 Skill을 다시 검색하게 합니다.

## Kakao API 설정

1. [Kakao Developers](https://developers.kakao.com/)에서 애플리케이션을 생성합니다.
2. REST API 키를 생성하거나 선택하고 필요한 서비스 정보 및 IP 제한을 설정합니다.
3. 키는 실행 환경에서만 제공합니다.

```bash
export KAKAO_REST_API_KEY='your-rest-api-key'
```

키를 프롬프트, 스크린샷, 셸 기록, Git에 커밋되는 `.env`, 예제 명령에 넣지 마세요. 키가 노출되었다면 Kakao Developers에서 즉시 교체하세요.

## 지원 기능

- 키워드 및 카테고리 기반 장소 검색
- 주소 지오코딩과 좌표 역지오코딩
- 행정구역 조회와 좌표계 변환
- 최대 5개 경유지를 포함한 현재 자동차 경로
- 미래 출발 시간 기준 자동차 경로
- 다중 경유지, 다중 출발지, 다중 목적지 요청
- Kakao API 근거와 계획자의 추론을 구분하는 여행 일정 작성 지침

이 Skill이 사용하는 Kakao 공개 REST API는 **도보 또는 대중교통 경로를 제공하지 않습니다**. 자동차 예상 시간을 도보, 지하철 또는 버스 결과로 바꾸어 표시하지 않습니다.

## CLI 예제

설치된 Skill 디렉터리에서 실행합니다.

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

키나 네트워크 호출 없이 요청을 확인할 수 있습니다.

```bash
python3 scripts/kakao_api.py --dry-run keyword '경복궁 맛집' \
  --x 126.9769 --y 37.5776 --radius 1500 --sort distance
```

모든 옵션 보기:

```bash
python3 scripts/kakao_api.py --help
python3 scripts/kakao_api.py directions --help
```

## 저장소 구조

```text
.
├── SKILL.md                    Agent 진입점 및 판단 지침
├── agents/openai.yaml          Skill UI 메타데이터
├── references/
│   ├── local-api.md            Kakao Local API 참고 자료
│   ├── navigation-api.md       Kakao Mobility 길찾기 참고 자료
│   └── travel-planning.md      근거 기반 여행 계획 규칙
└── scripts/
    ├── kakao_api.py            외부 의존성이 없는 REST CLI
    └── test_kakao_api.py       요청 생성 테스트
```

## 배포 전 검증

CLI는 Python 표준 라이브러리만 사용합니다.

```bash
python3 -m unittest -v scripts/test_kakao_api.py
python3 -m py_compile scripts/kakao_api.py scripts/test_kakao_api.py
python3 scripts/kakao_api.py --dry-run keyword '경복궁'
```

Codex `skill-creator`가 설치되어 있다면 다음도 실행합니다.

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
```

실제 API 테스트에는 `KAKAO_REST_API_KEY`가 필요하며 계정 할당량을 사용할 수 있습니다. 신뢰할 수 없는 Pull Request의 CI 환경에서는 실제 API 테스트를 실행하지 마세요.

## 공식 문서 및 유지보수

- [Kakao Local REST API](https://developers.kakao.com/docs/latest/ko/local/dev-guide)
- [Kakao Mobility 길찾기 API](https://developers.kakaomobility.com/guide/navi-api/start)
- [자동차 길찾기](https://developers.kakaomobility.com/guide/navi-api/directions)
- [미래 운행 정보 길찾기](https://developers.kakaomobility.com/guide/navi-api/future)

엔드포인트 호스트, 요청 필드, 제한 또는 인증 동작을 변경하기 전에 공식 문서를 다시 확인하세요. 이전 [`CaChiJ/kakao-navigation-mcp-server`](https://github.com/CaChiJ/kakao-navigation-mcp-server)는 초기 사용 사례에 참고했지만, 이 Skill은 실제 API로 지원되지 않는 도보 경로 설명을 계승하지 않습니다.

## 라이선스

[MIT](LICENSE)
