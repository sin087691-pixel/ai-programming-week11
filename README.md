# ai-programming-week11
# 성적 CSV 읽기 프로그램 (load_scores)

## ① 무엇을 하나요 (What)
성적 CSV를 읽어 0~100점의 유효한 점수만 골라 내고, 건너뛴 줄은 줄 번호와 이유를 함께 돌려줍니다.

## ② 왜 만들었나요 (Why)
10주차에 AI가 만든 코드들이 105점·-5점을 그대로 넣거나, 헤더를 잘못 짐작해서 한 줄도 읽지 못했습니다.
실제 파일에는 빈 점수·"결석"·열이 세 개인 줄이 섞여 있습니다. 그래서 멈추지 않고 건너뛰되, 왜 건너뛰었는지 알려 주는 함수가 필요했습니다.

## ③ 어떻게 쓰나요 (How)
```bash
cd week11_files/week11_files
python -m pip install pytest pytest-cov
python load_scores.py scores.csv
```

## ④ 어떻게 테스트하나요
```bash
python -m pytest test_load_scores.py -v
python -m pytest test_load_scores.py --cov=load_scores --cov-report=term-missing
```
결과: 12 passed, 커버리지 80% (77-86번 줄은 직접 실행용 코드)

## ⑤ 파일 구성
| 파일 | 하는 일 |
| --- | --- |
| load_scores.py | 성적 CSV를 읽어 (kept, skipped) 반환 |
| scores.csv · empty.csv · weird.csv | 정상 · 헤더만 · 이상한 줄 샘플 |
| test_load_scores.py | 직접 설계한 정상·예외·경계값 테스트 |
| test_ai_A.py · test_ai_B.py · test_ai_C_버그.py | AI에게 코드 / 명세 / 버그 코드를 주고 받은 테스트 |
| bug3_logic.py | 8주차 find_max 버그 파일 |
| prompts.txt | 프롬프트 원문 |

## ⑥ 만든 사람 · AI를 어디에 썼는지
- 만든 사람 : 신우석 (2026100314)
- AI를 쓴 곳 : test_ai_A·B·C 생성, 테스트 코드 문법 보조, README 초안
- 내가 직접 판단한 것 : 설계표 여덟 케이스, 커버리지 빠진 줄 이유, 세 벌 비교와 ★ 판정

## 라이선스
MIT License (LICENSE 파일 참고)
