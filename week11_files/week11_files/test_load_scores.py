import os
import pytest
from load_scores import load_scores

여기 = os.path.dirname(os.path.abspath(__file__))


def 파일(이름):
    return os.path.join(여기, 이름)


# ── 정상 ─────────────────────────────────────────

def test_정상_파일을_읽는다():
    kept, skipped = load_scores(파일("scores.csv"))
    assert len(kept) == 5
    assert len(skipped) == 5


def test_빈_줄은_건너뛴다():
    kept, skipped = load_scores(파일("scores.csv"))
    기록된_줄번호 = [줄번호 for 줄번호, 원본, 이유 in skipped]
    assert 10 not in 기록된_줄번호


def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores(파일("scores.csv"))
    assert ("최,네번", 77) in kept


# ── 예외 ─────────────────────────────────────────

def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores(파일("없는파일.csv"))


def test_헤더만_있으면_빈_결과():
    kept, skipped = load_scores(파일("empty.csv"))
    assert kept == []
    assert skipped == []


# ── 경계값 ───────────────────────────────────────

def 쓰기(경로, 점수):
    with open(경로, "w", encoding="utf-8") as f:
        f.write("name,score\n")
        f.write(f"테스트,{점수}\n")


@pytest.mark.parametrize("점수, 유효한가", [
    (-1,  False),
    (0,   True),
    (1,   True),
    (99,  True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, 점수, 유효한가):
    임시 = tmp_path / "임시.csv"
    쓰기(임시, 점수)
    kept, skipped = load_scores(str(임시))
    assert (len(kept) == 1) == 유효한가


# ── 커버리지 보고 추가한 테스트 ──────────────────

def test_이름이_비면_건너뛰고_기록한다():
    kept, skipped = load_scores(파일("weird.csv"))
    이유들 = [이유 for 줄번호, 원본, 이유 in skipped]
    assert "이름이 비어 있음" in 이유들
    assert kept == [("한겨울", 77), ("윤보람", 88)]