# 성적 CSV 읽기 프로그램 (load_scores)

## ① 무엇을 하나요 (What)

성적 CSV 파일을 읽어 0~100점 사이의 유효한 점수만 골라 내고, 건너뛴 줄은 줄 번호와 이유를 함께 돌려줍니다.

## ② 왜 만들었나요 (Why)

10주차에 AI가 만든 코드 네 가지를 실제 scores.csv로 돌려 보니, 읽는 데 성공한 버전조차 105점과 -5점을 그대로 넣었고 다른 버전들은 헤더를 잘못 짐작해 한 줄도 읽지 못했습니다.
실제 파일에는 빈 점수·"결석"·열이 세 개인 줄이 꼭 섞여 있어서, 멈추지 않고 건너뛰되 몇 번째 줄을 왜 건너뛰었는지 알려 주는 함수가 필요했습니다.
같은 이름은 동명이인일 수 있어 함수가 지우지 않고 둘 다 남깁니다.

## ③ 어떻게 쓰나요 (How)

```bash
python -m pip install pytest pytest-cov

# 실행
python load_scores.py scores.csv
```

## ④ 어떻게 테스트하나요

```bash
python -m pytest test_load_scores.py -v
python -m pytest test_load_scores.py --cov=load_scores --cov-report=term-missing
```

```
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
load_scores.py      45      9    80%   77-86
----------------------------------------------
TOTAL               45      9    80%
12 passed
```

## ⑤ 파일 구성

| 파일 | 하는 일 |
| --- | --- |
| load_scores.py | 성적 CSV를 읽어 (kept, skipped)를 돌려주는 함수 |
| scores.csv | 정상 5명 + 문제 줄 5개 + 빈 줄 1개 |
| empty.csv | 헤더만 있는 파일 |
| weird.csv | 빈 이름·공백·소수점 등 이상한 줄 모음 |
| test_load_scores.py | 직접 설계한 정상·예외·경계값 테스트 (함수 7개, 12회 실행) |
| test_ai_A.py | AI에게 코드를 주고 받은 테스트 |
| test_ai_B.py | AI에게 명세를 주고 받은 테스트 |
| test_ai_C_버그.py | 버그 있는 find_max를 주고 받은 테스트 (함정 실험) |
| bug3_logic.py | 8주차 find_max 버그 파일 |
| prompts.txt | A/B/함정 프롬프트 원문 |

## ⑥ 만든 사람 · AI를 어디에 썼는지

- 만든 사람 : 신우석 (2026100314)
- AI를 쓴 곳 : test_ai_A·B·C 생성, 테스트 코드 문법 보조, README 초안 정리
- 내가 직접 판단한 것 : 설계표 여덟 케이스(명세 기준), 커버리지에서 빠진 줄의 이유와 추가 테스트, 세 벌 비교와 ★ 판정, 커밋 메시지

## 라이선스

MIT License (LICENSE 파일 참고)