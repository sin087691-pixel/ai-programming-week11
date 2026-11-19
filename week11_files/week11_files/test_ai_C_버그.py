import pytest
from bug3_logic import find_max


def test_가장_큰_값이_가운데_있을_때():
    assert find_max([70, 88, 60]) == 88


def test_가장_큰_값이_맨_앞일_때():
    assert find_max([95, 70, 60]) == 95


def test_가장_큰_값이_맨_뒤일_때():
    assert find_max([70, 85, 60, 95]) == 95


def test_원소가_하나일_때():
    assert find_max([42]) == 42


def test_원소가_두_개일_때():
    assert find_max([10, 20]) == 20


def test_음수만_있을_때():
    assert find_max([-5, -1, -3]) == -1


def test_모두_같은_값일_때():
    assert find_max([7, 7, 7]) == 7


def test_빈_리스트면_오류():
    with pytest.raises(IndexError):
        find_max([])


def test_경계값_0과_100():
    assert find_max([0, 50, 100]) == 100