# 💰 나만의 용돈 기입장 콘솔 프로그램 (Budget App)

Python 3.10+ 표준 라이브러리만을 사용하여 구현한 **고성능 대용량 데이터 처리 콘솔 가계부 애플리케이션**입니다.  
수만 건 이상의 거래 데이터 환경에서도 메모리 부담 없는 **제너레이터(Generator) 스트리밍 아키텍처**와 데이터 무결성을 보장하는 **원자적 파일 교체(Atomic File Replacement)**를 적용했습니다.

---

## 📌 1. 주요 특징 및 기술적 강점

1. **순수 파이썬 표준 라이브러리만 사용 (Zero Dependency)**
   - 별도의 `pip install` 없이 파이썬 표준 모듈(`json`, `csv`, `pathlib`, `argparse`, `dataclasses`, `datetime` 등)만으로 10대 핵심 기능을 완벽히 구현했습니다.
2. **제너레이터(Generator) 기반 메모리 효율적 스트리밍**
   - 대용량 `transactions.jsonl` 파일을 한 번에 메모리에 올리지 않고, `yield` 기반 스트리밍 파이프라인으로 처리하여 메모리 점유율을 극소화했습니다.
3. **원자적 파일 교체 (Atomic File Replacement)**
   - 데이터 수정/삭제(`update`, `delete`, `category remove`, `budget set`) 시 임시 파일(`.tmp`)을 생성한 후 `os.replace`로 원자적 교체를 수행하여, 프로세스가 비정상 종료되어도 파일 손상을 원천 방지합니다.
4. **횡단 관심사 데코레이터 패턴 (Decorators)**
   - `@handle_errors`: 파이썬 스택트레이스를 숨기고 사용자 친화적 오류 원인 및 해결 힌트 출력 후 비정상 종료 코드(`exit 1`) 반환
   - `@_atomic_rewrite`: 임시 파일 생성 및 `os.replace` 원자적 파일 교체 자동화
   - `@measure_time`: 실행 소요 시간 측정 (정밀도 1ns)

---

## 🗂️ 2. 프로젝트 디렉터리 구조

```text
B02-01/
├── data/                       # 영구 저장소 디렉터리 (JSONL 형식)
│   ├── transactions.jsonl      # 거래 내역 (Append-only 이벤트 로그)
│   ├── categories.jsonl        # 카테고리 메타데이터 (Master data)
│   └── budgets.jsonl           # 월별 예산 데이터
├── models.py                   # dataclass 기반 데이터 모델 (Transaction, Category, Budget)
├── repository.py               # 저장소 계층 (파일 I/O, 스트리밍, 원자적 교체)
├── decorators.py               # 공통 관심사 데코레이터 (@handle_errors, @_atomic_rewrite 등)
├── user_input.py               # 대화형 입력 검증 및 포맷터
├── budget_app.py               # 메인 CLI 진입점 및 argparse 서브파서 라우팅
└── README.md                   # 프로젝트 문서
```

---

## 📋 3. 영구 저장소 스키마 규격

### (1) `transactions.jsonl`
각 행(Line)마다 하나의 거래 내역이 JSON 형태로 영구 저장됩니다:
```json
{"id": "TX-000001", "type": "expense", "date": "2026-09-15", "amount": 15000, "category": "식비", "memo": "점심식사", "tags": ["식사", "외식"]}
```

### (2) `categories.jsonl`
기본 카테고리 자동 초기화 및 사용자 정의 카테고리가 저장됩니다:
```json
{"type": "expense", "name": "식비"}
{"type": "income", "name": "급여"}
```

### (3) `budgets.jsonl`
월별 설정 예산 데이터가 저장됩니다:
```json
{"ym": "2026-09", "budget": 700000}
```

### (4) CSV 가져오기/내보내기 (`import/export`) 스키마 (UTF-8, 헤더 포함)
| 컬럼명 | 필수 여부 | 형식 / 설명 |
|:---:|:---:|---|
| **date** | Y | `YYYY-MM-DD` (예: 2026-09-15) |
| **type** | Y | `income` 또는 `expense` |
| **category** | Y | 등록된 카테고리 이름 |
| **amount** | Y | 0보다 큰 양수 정수 |
| **memo** | N | 문자열 (선택) |
| **tags** | N | 쉼표(`,`)로 구분된 태그 문자열 (예: `식사,외식`) |

---

## 🚀 4. CLI 실행 가이드 (10대 핵심 기능)

모든 명령은 리눅스 표준인 `--` 옵션을 사용하며, **`python -m budget_app <command> [options]`** 형태로 실행합니다.

```bash
# 전체 사용법 및 도움말 확인
python -m budget_app --help
python -m budget_app <command> --help
```

### 1. 거래 추가 (`add`)
날짜, 타입, 카테고리, 금액, 메모, 태그를 순차적으로 입력받아 새로운 고유 ID(`TX-XXXXXX`)를 자동 발급합니다.
```bash
python -m budget_app add
```

### 2. 거래 목록 조회 (`list`)
최신순(역순) 스트리밍으로 거래 내역을 테이블 형태로 출력합니다.
```bash
python -m budget_app list
python -m budget_app list --limit 5    # 최근 5건만 조회
```

### 3. 거래 조건 검색 (`search`)
기간, 카테고리, 수입/지출, 메모 키워드, 태그 등 다양한 다중 조건 필터링 검색을 지원합니다.
```bash
python -m budget_app search --category 식비 --from 2026-09-01 --to 2026-09-30
python -m budget_app search --type expense --q 점심
python -m budget_app search --tag 식사
```

### 4. 거래 수정 (`update`)
거래 ID를 지정하여 대화형으로 원하는 항목만 선택 수정합니다. (카테고리 수정 시 수입/지출 타입 자동 동기화 지원)
```bash
python -m budget_app update --id TX-000001
```

### 5. 거래 삭제 (`delete`)
거래 ID를 지정하여 안전한 원자적 파일 교체 방식으로 영구 삭제합니다.
```bash
python -m budget_app delete --id TX-000001
```

### 6. 카테고리 관리 (`category`)
카테고리 목록 조회, 추가, 삭제 기능을 제공합니다. 기존 거래 내역에서 사용 중인 카테고리는 삭제가 안전하게 차단됩니다.
```bash
python -m budget_app category list                          # 목록 조회
python -m budget_app category add --name 운동 --type expense  # 추가 (대화형도 지원)
python -m budget_app category remove --name 운동             # 삭제 (사용 중 시 차단)
```

### 7. 월별 예산 관리 (`budget`)
월별 예산을 설정하거나 조회합니다. 이미 존재하는 월은 새로운 금액으로 자동 갱신(Upsert)됩니다.
```bash
python -m budget_app budget set --month 2026-09 --amount 700000  # 예산 설정/수정
python -m budget_app budget list                                 # 설정된 예산 목록
```

### 8. 월별 재정 요약 및 예산 분석 (`summary`)
해당 월의 총 수입, 총 지출, 순 잔액, 지출 카테고리 TOP N 순위, 예산 대비 사용률 및 초과 경고를 출력합니다.
```bash
python -m budget_app summary --month 2026-09
python -m budget_app summary --month 2026-09 --top 3             # TOP 3 카테고리 지정
python -m budget_app summary                                   # 대화형 연월 입력
```

### 9. CSV 파일 내보내기 (`export`)
기간 조건(`--month` 또는 `--from`/`--to`)을 필수로 받아 조건에 맞는 거래 데이터를 CSV로 스트리밍 내보내기합니다.
```bash
python -m budget_app export --out backup.csv --month 2026-09
python -m budget_app export --out range.csv --from 2026-01-01 --to 2026-06-30
```

### 10. CSV 파일 가져오기 (`import`)
외부 CSV 파일을 읽어 유효성 검사 후 새 ID를 부여하여 일괄 등록합니다.
```bash
python -m budget_app import --from backup.csv
# 출력: [가져오기 완료] 성공 : 6건, 건너뜀: 0건 (imported=6, skipped=0)
```

### 11. 저장 폴더 변경 옵션 (`--data-dir`)
기본 `./data` 폴더 외에 다른 디렉터리를 지정하여 실행할 수 있습니다.
```bash
python -m budget_app --data-dir ./my_data list
```

---

## 🛡️ 5. 예외 처리 및 종료 코드 규격
* **정상 종료**: 종료 코드 `0` 반환
* **사용자 작업 취소 (Ctrl+C, Ctrl+D)**: 종료 코드 `0` 반환 및 안내 문구 출력
* **오류 발생**: 파이썬 스택트레이스를 출력하지 않고 `[오류] 원인` 및 `[힌트] 해결책`을 출력한 뒤 비정상 종료 코드(`exit 1`) 반환
