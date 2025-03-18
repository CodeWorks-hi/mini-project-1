import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import platform
from matplotlib import font_manager, rc

# Streamlit 페이지 설정
st.set_page_config(page_title="고객 분석 대시보드", layout="wide")

# 한글 폰트 설정 (OS별 적용)
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)

# 데이터 로드
df = pd.read_csv("data/고객db_전처리.csv").fillna(0)

# 🚀 **탭 생성**
tab1, tab2 = st.tabs(["고객 데이터 분석", "판매 데이터 분석"])

# 📊 **고객 데이터 분석 탭**
with tab1:
    # 📌 분석 개요 (최상단으로 이동)
    with st.expander("🔍 분석 개요 보기"):
        st.write("""
        **📌 프로젝트 목표**  
        - 고객 데이터를 분석하여 최적의 마케팅 전략을 수립하고 수요 예측을 개선하는 것  

        **📌 사용된 데이터**  
        - 차량 판매 시점, 구매 유형, 연료 구분 등  
        """)

    # 하위 탭 생성 (연령대별 고객 분포, 지역별 고객 분포 등)
    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs(
        ["연령대별 고객 분포", "지역별 고객 분포", "연령대별 선호 차량 모델", 
         "연령대별 친환경 차량 선호도", "성별 및 연령대별 차량 선호도", "고객 등급 분석"]
    )


        # 연령대 정렬을 위한 순서 지정
    age_order = [
        "20대 초반", "20대 중반", "20대 후반",
        "30대 초반", "30대 중반", "30대 후반",
        "40대 초반", "40대 중반", "40대 후반",
        "50대 초반", "50대 중반", "50대 후반",
        "60대 초반", "60대 중반", "60대 후반",
        "70대 초반"
    ]

    # 📊 연령대별 고객 분포
    with subtab1:
        st.subheader("연령대별 고객 분포")
        st.write("고객의 연령대별 분포를 히스토그램으로 표현했습니다.")  

        # 연령대 정렬 후 시각화
        df["연령대"] = pd.Categorical(df["연령대"], categories=age_order, ordered=True)
        fig1, ax = plt.subplots(figsize=(8, 5))
        sb.histplot(df.sort_values("연령대")["연령대"], kde=True, color="blue", ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_xlabel("연령대")
        ax.set_ylabel("고객 수")
        st.pyplot(fig1)



    # 🗺️ 지역별 고객 분포
    with subtab2:
        st.subheader("지역별 고객 분포")
        st.write("고객들이 거주하는 지역별 분포를 나타냅니다.") 

        fig2, ax = plt.subplots(figsize=(8, 5))
        df["거주 지역"].value_counts().plot(kind="barh", color="orange", ax=ax)
        ax.set_xlabel("지역")
        ax.set_ylabel("고객 수") 
        st.pyplot(fig2)


    # 🚗 연령대별 선호 차량 모델
    with subtab3:
        st.subheader("🚗 연령대별 선호 차량 모델")
        top_models = df.groupby(["연령대", "최근 구매 제품"]).size().reset_index(name="count")
        top_models = top_models.sort_values(["연령대", "count"], ascending=[True, False])
        top_models = top_models.groupby("연령대").head(3)

        fig, ax = plt.subplots(figsize=(10, 6))
        sb.barplot(data=top_models, x="연령대", y="count", hue="최근 구매 제품", palette="coolwarm", ax=ax)
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig)

    # ⚡ 연령대별 친환경 차량 선호도
    with subtab4:
        st.subheader("⚡ 연령대별 친환경 차량 선호도")
        eco_types = ["전기", "수소", "하이브리드"]
        ev_preference = df[df["연료 구분"].isin(eco_types)].groupby("연령대")["연료 구분"].count()

        fig, ax = plt.subplots(figsize=(8, 5))
        ev_preference.plot(kind="bar", color="lightgreen", ax=ax)
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig)

    # 🚹🚺 성별 및 연령대별 차량 선호도
    with subtab5:
        st.subheader("🚹🚺 성별 및 연령대별 차량 선호도")
        gender_df = df.groupby(["성별", "연령대"])["차량 유형"].count().reset_index()

        fig, ax = plt.subplots(figsize=(12, 8))
        sb.barplot(data=gender_df, x="연령대", y="차량 유형", hue="성별", palette="Set2", ax=ax)
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig)

    # ⭐ 고객 등급 분석
    with subtab6:
        st.subheader("⭐ 고객 등급 분석")
        customer_tier = df.groupby('연령대')['고객 등급'].value_counts().rename('등급 수').reset_index()

        fig, ax = plt.subplots(figsize=(8, 5))
        sb.barplot(data=customer_tier, x="연령대", y="등급 수", hue="고객 등급", ax=ax)
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig)

# 🏷️ **판매 데이터 분석 탭**
with tab2:
    subtab1, subtab2, subtab3, subtab4 = st.tabs(
        ["시기 및 연료 구분별 판매 대수", "고객 구분별 차량 구매 현황", "연령대 및 성별 차량 구매 대수", "분기별 차량 판매 요일"]
    )

    # 🚘 시기 및 연료 구분별 판매 대수
    with subtab1:
        st.subheader("시기 및 연료 구분별 판매 대수")
        st.write("고객들이 선호하는 연료 구분을 분석하여 그래프로 표현했습니다.")

        date_order = ["2023 1분기", "2023 2분기", "2023 3분기", "2023 4분기", "2024 1분기", "2024 2분기", "2024 3분기", "2024 4분기", "2025 1분기"]

        df["최근 구매 시점"] = pd.Categorical(df["최근 구매 시점"], categories=date_order, ordered=True)

        # 구매 기준 시점별 각 연료 구분의 개수 시각화
        fig1, ax = plt.subplots(figsize=(12, 8))
        st.pyplot(fig)

    # 🚘 고객 구분별 차량 구매 현황
    with subtab2:
        st.subheader("고객 구분별 차량 구매 현황")
        st.write("고객들의 구매 유형에 따른 차량 구매 현황을 분석하여 그래프로 표현했습니다.")

        fig, ax = plt.subplots(figsize=(12, 8))
        sb.lineplot(x="최근 구매 시점", y="연번", hue="고객 구분", data=df, marker="o", palette="Set2", lw=2, ax=ax)
        ax.set_title("고객 구분별 연료 구분별 판매 대수")
        ax.set_xlabel("구매 시점")
        ax.set_ylabel("판매 대수")
        plt.xticks(rotation=30)
        plt.grid(axis="y", linestyle="--")
        plt.legend(title="고객 구분", loc="upper left")
        st.pyplot(fig)


    # 🚘 연령대 및 성별 차량 구매 대수
    with subtab3:
        st.subheader("📊 연령대 및 성별 차량 구매 대수")
        st.write("고객들이 선호하는 구매 유형을 분석하여 그래프로 표현했습니다.")

        fig, ax = plt.subplots(figsize=(12, 8))
        df["선호 거래 방식"].value_counts().plot(kind="bar", color=["skyblue", "salmon", "lightgreen"], ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.set_xlabel("결제 방식")
        ax.set_ylabel("판매 건수")
        st.pyplot(fig)

    # 📅 분기별 차량 판매 요일
    with subtab4:
        st.subheader("📊 분기별 차량 판매 요일")
        st.write("고객들의 연령대 및 성별에 따른 차량 구매 대수를 분석하여 그래프로 표현했습니다.")

        # 연령대별 각 성별이 구매한 차량 수 합계
        gender_df = df.groupby(["성별", "연령대"])["차량 사이즈"].count().reset_index()

        df_pivot = gender_df.pivot_table(index="연령대", columns="성별", values="차량 사이즈", fill_value=0)

        colors = sb.color_palette("Set2", n_colors=len(df_pivot.columns))

        fig1, ax = plt.subplots(figsize=(12, 8))
        df_pivot.plot.bar(ax=ax, color=colors)
        ax.set_title("연령대별 성별 차량 구매 수", fontsize=16)
        ax.set_xlabel("연령대", fontsize=12)
        ax.set_ylabel("판매량", fontsize=12)
        ax.legend(title="성별")
        ax.set_xticklabels(df_pivot.index, rotation=0)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
        plt.tight_layout()
        st.pyplot(fig1)
