import pandas as pd


def 정제(df):
    # 원본은 건드리지 않고 복사본으로 작업
    df = df.copy()
    print("시작        ", len(df))
    # 1) 점수가 빈 행 삭제
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거  ", len(df))
    # 2) 모든 열이 같은 중복 행은 하나만 남김
    df = df.drop_duplicates()
    print("중복 제거   ", len(df))
    # 3) 반, 과목의 앞뒤 공백 
    # 4) 점수가 0~100 밖인 행 삭제
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거", len(df))
    return df


def 반별평균(df):
    # 반 이름을 키로 하는 평균 점수 (소수 둘째 자리 반올림)
    return df.groupby("반")["점수"].mean().round(2)


def 반별통계(df):
    # 개수, 평균, 중앙값, 최댓값을 한 표로
    return df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)


if __name__ == "__main__":
    df = pd.read_csv("scores_2026.csv")
    print("shape:", df.shape)
    df = 정제(df)

    print("\n[B] 수학만:", len(df[df["과목"] == "수학"]))
    print("[B 응용] 1반 & 90점 이상:", len(df[(df["반"] == "1반") & (df["점수"] >= 90)]))

    print("\n[C] 반별 평균\n", df.groupby("반")["점수"].mean())
    print("\n[C] 과목x반 평균\n", df.groupby(["과목", "반"])["점수"].mean())

    print("\n[D] 반별 통계\n", 반별통계(df))

    print("\n[검증] 그룹 합의 합 / 전체 합:", df.groupby("반")["점수"].sum().sum(), df["점수"].sum())
    print("[검증] 그룹 개수의 합 / 행 수:", df.groupby("반")["점수"].count().sum(), len(df))
    print("[스팟] 1반 수학 점수:", df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"].tolist())