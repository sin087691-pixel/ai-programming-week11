import pytest
from load_scores import load_scores


@pytest.fixture
def write_csv(tmp_path):
    def _write(lines):
        p = tmp_path / "scores.csv"
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(p)
    return _write


# ---------- 정상 ----------

def test_정상_여러_명을_읽는다(write_csv):
    kept, skipped = load_scores(write_csv(["name,score", "김하나,88", "이두리,70"]))
    assert kept == [("김하나", 88), ("이두리", 70)]
    assert skipped == []


def test_반환값은_튜플이고_점수는_정수(write_csv):
    result = load_scores(write_csv(["name,score", "김하나,88"]))
    assert isinstance(result, tuple) and len(result) == 2
    assert isinstance(result[0][0][1], int)


def test_쉼표가_든_이름도_한_명으로_읽는다(write_csv):
    kept, _ = load_scores(write_csv(["name,score", '"최,네번",77']))
    assert ("최,네번", 77) in kept


def test_같은_이름은_둘_다_남긴다(write_csv):
    kept, _ = load_scores(write_csv(["name,score", "김하나,88", "김하나,91"]))
    assert kept == [("김하나", 88), ("김하나", 91)]


def test_이름과_점수의_앞뒤_공백을_제거한다(write_csv):
    kept, _ = load_scores(write_csv(["name,score", " 한겨울 , 77 "]))
    assert kept == [("한겨울", 77)]


def test_빈_줄은_기록_없이_건너뛴다(write_csv):
    kept, skipped = load_scores(write_csv(["name,score", "김하나,88", "", "이두리,70"]))
    assert len(kept) == 2
    assert skipped == []


def test_문제_줄이_있어도_멈추지_않는다(write_csv):
    kept, skipped = load_scores(write_csv(["name,score", "가,10", "나,abc", "다,20", "라,200"]))
    assert kept == [("가", 10), ("다", 20)]
    assert [s[0] for s in skipped] == [3, 5]


def test_건너뛴_줄은_원본줄_그대로_기록한다(write_csv):
    kept, skipped = load_scores(write_csv(["name,score", '"김,쉼표",1000']))
    assert skipped[0][0] == 2
    assert skipped[0][1] == '"김,쉼표",1000'


# ---------- 예외 ----------

def test_파일이_없으면_FileNotFoundError(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(str(tmp_path / "없는파일.csv"))


def test_헤더만_있으면_빈_결과(write_csv):
    assert load_scores(write_csv(["name,score"])) == ([], [])


def test_열_개수가_2가_아니면_건너뛴다(write_csv):
    kept, skipped = load_scores(write_csv(["name,score", "장미르,72,비고없음"]))
    assert kept == []
    assert len(skipped) == 1 and skipped[0][0] == 2


def test_빈_이름은_건너뛴다(write_csv):
    kept, skipped = load_scores(write_csv(["name,score", ",90"]))
    assert kept == []
    assert len(skipped) == 1


@pytest.mark.parametrize("raw", ["", "abc", "88.5", "-5", "105"])
def test_잘못된_점수는_건너뛴다(write_csv, raw):
    kept, skipped = load_scores(write_csv(["name,score", f"홍길동,{raw}"]))
    assert kept == []
    assert len(skipped) == 1


# ---------- 경계값 ----------

@pytest.mark.parametrize("score, valid", [
    (-1, False), (0, True), (50, True), (100, True), (101, False),
])
def test_점수_경계값(write_csv, score, valid):
    kept, skipped = load_scores(write_csv(["name,score", f"테스트,{score}"]))
    assert (len(kept) == 1) == valid
    assert (len(skipped) == 1) != valid