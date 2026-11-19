import pytest
from load_scores import load_scores


def make_csv(tmp_path, text, encoding="utf-8"):
    p = tmp_path / "scores.csv"
    p.write_text(text, encoding=encoding)
    return str(p)


# ---------- 정상 ----------

def test_normal_rows(tmp_path):
    path = make_csv(tmp_path, "name,score\n김하나,88\n이두리,70\n")
    kept, skipped = load_scores(path)
    assert kept == [("김하나", 88), ("이두리", 70)]
    assert skipped == []


def test_blank_lines_are_ignored_without_record(tmp_path):
    path = make_csv(tmp_path, "name,score\n\n김하나,88\n\n")
    kept, skipped = load_scores(path)
    assert kept == [("김하나", 88)]
    assert skipped == []


def test_quoted_name_with_comma(tmp_path):
    path = make_csv(tmp_path, 'name,score\n"최,네번",77\n')
    kept, skipped = load_scores(path)
    assert kept == [("최,네번", 77)]


def test_whitespace_is_stripped(tmp_path):
    path = make_csv(tmp_path, "name,score\n  한겨울 ,  77 \n")
    kept, _ = load_scores(path)
    assert kept == [("한겨울", 77)]


def test_duplicate_names_are_both_kept(tmp_path):
    path = make_csv(tmp_path, "name,score\n김하나,88\n김하나,91\n")
    kept, _ = load_scores(path)
    assert kept == [("김하나", 88), ("김하나", 91)]


def test_utf8_bom_is_handled(tmp_path):
    path = make_csv(tmp_path, "name,score\n김하나,88\n", encoding="utf-8-sig")
    kept, _ = load_scores(path)
    assert kept == [("김하나", 88)]


# ---------- 예외 ----------

def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(str(tmp_path / "없음.csv"))


def test_header_only_returns_empty(tmp_path):
    path = make_csv(tmp_path, "name,score\n")
    assert load_scores(path) == ([], [])


def test_completely_empty_file(tmp_path):
    path = make_csv(tmp_path, "")
    assert load_scores(path) == ([], [])


def test_wrong_column_count_is_skipped(tmp_path):
    path = make_csv(tmp_path, "name,score\n장미르,72,비고없음\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped == [(2, "장미르,72,비고없음", "열 개수가 2가 아님")]


def test_empty_name_is_skipped(tmp_path):
    path = make_csv(tmp_path, "name,score\n,90\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped == [(2, ",90", "이름이 비어 있음")]


def test_empty_score_is_skipped(tmp_path):
    path = make_csv(tmp_path, "name,score\n박세찬,\n")
    kept, skipped = load_scores(path)
    assert skipped == [(2, "박세찬,", "점수가 비어 있음")]


@pytest.mark.parametrize("raw", ["결석", "88.5", "7 2"])
def test_non_integer_score_is_skipped(tmp_path, raw):
    path = make_csv(tmp_path, f"name,score\n홍길동,{raw}\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "점수가 정수가 아님"


def test_line_numbers_count_blank_lines(tmp_path):
    path = make_csv(tmp_path, "name,score\n김하나,88\n\n박세찬,abc\n")
    _, skipped = load_scores(path)
    assert skipped == [(4, "박세찬,abc", "점수가 정수가 아님")]


# ---------- 경계값 ----------

@pytest.mark.parametrize("score, valid", [
    (-1, False), (0, True), (1, True), (99, True), (100, True), (101, False),
])
def test_score_boundaries(tmp_path, score, valid):
    path = make_csv(tmp_path, f"name,score\n테스트,{score}\n")
    kept, skipped = load_scores(path)
    if valid:
        assert kept == [("테스트", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped == [(2, f"테스트,{score}", "점수가 0~100 밖")]