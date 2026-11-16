# Kakao REST API 키 발급 및 설정 튜토리얼

[中文](rest-api-key-setup.md) | [English](rest-api-key-setup.en.md) | **한국어**

이 문서는 Kakao Local 장소 데이터와 Kakao Mobility 자동차 길찾기에 필요한 REST API 키를 설정합니다. 초기 흐름은 [`CaChiJ/kakao-navigation-mcp-server`](https://github.com/CaChiJ/kakao-navigation-mcp-server)를 참고했으며, 아래 단계는 현재 Kakao 공식 화면과 정책을 기준으로 작성했습니다.

## 1. Kakao Developers 로그인

1. [Kakao Developers](https://developers.kakao.com/)를 엽니다.
2. Kakao 계정으로 로그인하거나 계정을 만듭니다.
3. 앱 관리 화면으로 이동합니다.

## 2. 애플리케이션 생성

1. 상단에서 **앱**을 선택합니다.
2. **앱 생성**을 선택합니다.
3. 앱 이름과 개발자 또는 회사의 필수 정보를 입력하고 저장합니다.

앱을 만들면 여러 종류의 키가 생성됩니다. 이 Skill은 **REST API 키**만 사용합니다. JavaScript 키, 네이티브 앱 키 또는 어드민 키를 대신 사용하지 마세요.

## 3. Kakao Map API 활성화

장소 검색, 주소 변환, 좌표 변환은 Kakao Map REST API입니다.

1. 생성한 앱을 엽니다.
2. **카카오맵 → 사용 설정**으로 이동합니다.
3. 상태를 `ON`으로 설정합니다.

2026년 7월 21일부터 Kakao Map API 사용 방법과 무료 쿼터 정책이 변경되었습니다. 개발자 계정에서 처음 Kakao Map API를 활성화한 앱에는 무료 쿼터 배지가 표시될 수 있습니다. 두 번째 이후 앱이나 무료 쿼터를 초과하는 사용은 비즈월렛 연결과 유료 API 설정이 필요할 수 있습니다. 콘솔 상태와 [Kakao Map 공식 안내](https://developers.kakao.com/docs/ko/kakaomap/common)를 확인하세요.

## 4. REST API 키 생성 또는 확인

Kakao는 2025년 12월 3일에 앱 키 메뉴를 개편했습니다. 현재 경로는 다음과 같습니다.

1. **앱 → 앱 선택 → 앱 → 플랫폼 키**로 이동합니다.
2. 기존 REST API 키를 선택하거나 **REST API 키 추가**를 선택합니다.
3. `kakao-navigation-local`처럼 식별하기 쉬운 이름을 지정합니다.
4. 키가 활성 상태인지 확인하고 값을 복사합니다.

키 값은 자격 증명으로 취급하세요. GitHub, `SKILL.md`, README, 소스 코드 또는 공개 `.env` 파일에 커밋하지 마세요.

### Client Secret 안내

새 REST API 키는 Client Secret이 기본 활성화될 수 있습니다. Client Secret은 주로 Kakao Login 같은 OAuth 토큰 요청에 사용됩니다. 이 Skill의 Local 및 Directions 호출은 `Authorization: KakaoAK ...` 헤더를 사용하며 스크립트에 Client Secret을 전달할 필요가 없습니다. 어드민 키는 대체 키가 아닙니다.

## 5. 호출 허용 IP 주소 설정

허용 IP는 키 유출 위험을 줄이지만 잘못 설정하면 로컬 Agent의 호출도 차단합니다.

1. **앱 → 플랫폼 키 → REST API 키 선택 → 호출 허용 IP 주소**로 이동합니다.
2. 운영 환경에서는 서버의 고정 출구 IP 또는 적절한 CIDR을 입력합니다.
3. 로컬 개발 환경의 IP가 자주 변하면 먼저 호출을 검증한 후 제한을 적용합니다.
4. 설정을 저장합니다.

현재 키당 최대 10개 항목을 등록할 수 있으며 IPv4, CIDR 또는 Subnet Mask를 지원합니다. 등록 후에는 허용된 주소에서만 호출할 수 있습니다. `ip mismatched` 또는 `-401`이면 실제 출구 IP를 확인하거나 잘못된 허용 IP 항목을 잠시 제거한 후 다시 테스트하세요.

## 6. Kakao Mobility Directions 권한 확인

자동차 길찾기는 동일한 Kakao Developers REST API 키를 사용합니다. [Kakao Mobility 길찾기 시작하기](https://developers.kakaomobility.com/guide/navi-api/start)와 계정 콘솔에서 요금, 쿼터 및 서비스 상태를 확인하세요.

IP를 고정하거나 hosts 파일에 매핑하지 말고 공식 호스트를 사용합니다.

```text
https://apis-navi.kakaomobility.com
```

공개 Directions REST API는 자동차 경로를 제공하며 도보 또는 대중교통 경로를 의미하지 않습니다.

## 7. 로컬 환경에 키 설정

현재 터미널에만 설정하려면:

```bash
export KAKAO_REST_API_KEY='복사한 REST API 키'
```

전체 값을 출력하지 않고 설정 여부를 확인합니다.

```bash
test -n "$KAKAO_REST_API_KEY" && echo 'KAKAO_REST_API_KEY is set'
```

지속적으로 사용할 때는 OS 키체인, CI Secret 또는 권한이 제한된 환경 설정을 사용하세요. `.env`를 커밋하지 마세요. 이 저장소는 `.env`를 무시합니다.

## 8. 장소 검색 검증

Skill 루트에서 실행합니다.

```bash
python3 scripts/kakao_api.py keyword '경복궁' --size 3
```

성공하면 `documents`에 `place_name`, 주소, `x` 경도, `y` 위도 및 Kakao Place URL이 포함됩니다.

키나 네트워크 호출 없이 요청을 확인할 수도 있습니다.

```bash
python3 scripts/kakao_api.py --dry-run keyword '경복궁'
```

## 9. 자동차 길찾기 검증

장소 검색에서 반환된 좌표를 `경도,위도` 순서로 사용합니다.

```bash
python3 scripts/kakao_api.py directions \
  --origin 126.97689786832184,37.577613288258206 \
  --destination 127.027619208212,37.497952760023 \
  --priority RECOMMEND \
  --summary true
```

성공하면 `routes`에 `result_code: 0`과 `길찾기 성공`이 표시되고 거리, 시간, 택시 요금 및 통행료 예상값을 반환합니다. 소요 시간은 교통 상황과 요청 시점에 따라 달라집니다.

## 문제 해결

| 증상 | 확인 항목 |
|---|---|
| `KAKAO_REST_API_KEY is not set` | 현재 터미널에서 환경 변수를 설정했는지 확인 |
| HTTP `401` 또는 Kakao `-401` | 잘못된 키 종류, 비활성 키, 허용 IP 불일치 또는 복사 오류 |
| `appKeyType is ADMIN_KEY` | 어드민 키가 아닌 REST API 키 사용 |
| Local API 제품/권한 오류 | Kakao Map 활성화, 비즈월렛/유료 설정 및 쿼터 확인 |
| `429` | 재시도를 중단하고 속도 또는 쿼터 상태 확인 |
| 장소 검색은 성공하지만 길찾기 실패 | Kakao Map과 Kakao Mobility 상태, 쿼터, 요청 파라미터를 각각 확인 |
| 검색 결과 없음 | 한국어 장소명 사용, 너무 작은 반경 제거 또는 행정구역 추가 |

## 보안 점검

- 키가 채팅, 스크린샷, 공개 로그 또는 Git 기록에 나타나면 즉시 교체합니다.
- 키를 URL 쿼리 파라미터에 넣지 마세요. 이 Skill은 `Authorization` 헤더를 사용합니다.
- 운영 키에는 허용 IP를 적용하고 쿼터와 비정상 호출을 모니터링합니다.
- 신뢰할 수 없는 Pull Request가 실행하는 CI에 Secret을 노출하지 않습니다.

## 공식 문서

- [Kakao REST API 시작하기](https://developers.kakao.com/docs/ko/rest-api/getting-started)
- [앱 및 REST API 키 설정](https://developers.kakao.com/docs/ko/app-setting/app)
- [Kakao Map 사용 방법](https://developers.kakao.com/docs/ko/kakaomap/common)
- [2025 앱 및 앱 키 변경 사항](https://developers.kakao.com/docs/ko/getting-started/app-key-migration)
- [Kakao Mobility 길찾기 시작하기](https://developers.kakaomobility.com/guide/navi-api/start)
