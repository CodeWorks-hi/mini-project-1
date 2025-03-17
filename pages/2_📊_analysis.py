import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sb
import os

# 현재 파일 위치를 기준으로 절대 경로 설정
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts"))
font_path = os.path.join(base_dir, "NanumGothic.ttf")  # 또는 .otf 사용 가능

# 디버깅: 폰트 경로 확인
print("폰트 경로:", font_path)
print("파일 존재 여부:", os.path.exists(font_path))

# 폰트 설정
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
else:
    print("폰트 파일을 찾을 수 없습니다.")

# 데이터 로드
df = pd.read_csv("data/고객db_전처리.csv")

# Streamlit 페이지 설정
st.set_page_config(page_title="고객 분석 대시보드", layout="wide")

# 페이지 제목
st.title("분석 대시보드")

tab1, tab2 = st.tabs(["##고객 데이터 분석", "판매 데이터 분석"])

with tab1 :
    # 고객 데이터 분석 섹션

    st.write("고객 데이터 기반의 분석 인사이트를 제공합니다.")

    # 분석 개요 섹션
    with st.expander("분석 개요 보기"):
        st.write("""
        **프로젝트 목표**  
        - 고객의 연령대, 거주 지역, 구매 선호도를 분석하여 비즈니스 인사이트 제공  
        - 전기차 및 내연기관차의 트렌드 변화 확인  
        - 데이터 기반으로 마케팅 전략 최적화  

        **사용된 데이터**  
        - 고객 연령대, 거주 지역, 선호 차량 모델, 연료 유형, 최근 구매 날짜 등  
        """)

    st.text("")

    # 연령대 정렬을 위한 순서 지정
    age_order = [
        "20대 초반", "20대 중반", "20대 후반",
        "30대 초반", "30대 중반", "30대 후반",
        "40대 초반", "40대 중반", "40대 후반",
        "50대 초반", "50대 중반", "50대 후반",
        "60대 초반", "60대 중반", "60대 후반",
        "70대 초반"
    ]

    col1, col2 = st.columns([0.9, 1])  # 좌우 여백 추가
    with col1:
        # ---- 연령대별 고객 분포 ----
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

        st.write("""
        **분석 결과 및 활용 방안**  
        - 특정 연령대(30~40대)에 고객이 집중됨  
        - 이 연령대에 맞춘 타겟 마케팅 전략이 효과적일 가능성 높음  
        - 가족 단위 차량 프로모션, 장기 렌트 혜택 제공 가능
        """)
    with col2:
        # ---- 지역별 고객 수 분석 ----
        st.subheader("지역별 고객 분포")
        st.write("고객들이 거주하는 지역별 분포를 나타냅니다.") 

        fig2, ax = plt.subplots(figsize=(8, 5))
        df["거주 지역"].value_counts().plot(kind="barh", color="orange", ax=ax)
        ax.set_xlabel("지역")
        ax.set_ylabel("고객 수") 
        st.pyplot(fig2)

        st.write("""
        **분석 결과 및 활용 방안**  
        - 특정 지역(서울, 경기)에 고객이 집중됨  
        - 해당 지역에서 차량 전시회 및 시승 이벤트 기획 가능  
        - 지방 거주 고객 대상, 비대면 서비스(라이브 상담, 온라인 계약 등) 확대 필요
        """)

    st.markdown("---")
    
    # 연령대별 상위 3개 차량 모델 선정
    top_models = df.groupby(["연령대", "최근 구매 제품"]).size().reset_index(name="count")
    top_models = top_models.sort_values(["연령대", "count"], ascending=[True, False])
    top_models = top_models.groupby("연령대").head(3)  # 각 연령대에서 상위 3개 모델 선택

    eco_friendly_types = ["전기", "수소", "하이브리드", "플러그인하이브리드"]
    ev_preference = df[df["연료 구분"].isin(eco_friendly_types)].groupby("연령대")["연료 구분"].count()

    col1, col2 = st.columns([1, 1])  # 좌우 여백 추가
    with col1:
        # ---- 차량 브랜드 & 모델별 선호도 분석 ----
        st.subheader("고객 연령대별 선호 차량 모델 분석")
        st.write("연령대별로 선호하는 상위 3개 차량 모델을 선정하여 시각화했습니다.")

        fig1, ax = plt.subplots(figsize=(10, 6))
        sb.barplot(data=top_models, x="연령대", y="count", hue="최근 구매 제품", palette="coolwarm", ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_xlabel("연령대")
        ax.set_ylabel("선호 차량 모델 수")
        ax.set_title("연령대별 선호 차량 모델 (상위 3개)")
        st.pyplot(fig1)

        st.text("")
        
        st.markdown("""
        **📊 연령대별 선호 차량 모델 분석**  
        - **20~30대 초반**: 소형 세단 및 스포츠카 선호 → 경제성 및 개성 중시.  
        - **30대 후반~40대 후반**: 중형 세단 및 SUV 선호 → 패밀리카 및 실용성 강조.  
        - **50대 후반 이상**: 대형 세단 및 프리미엄 차량 선호 → 승차감 및 브랜드 가치 중시.  
        - **친환경 차량 증가**: 30~50대 고객층에서 전기차 및 하이브리드 차량 선호도 상승.  
        - **마케팅 활용**: 연령별 선호 모델을 반영한 맞춤형 금융 혜택 및 차량 프로모션 전략 필요.  

        참고 자료 출처: KATECH Insight, 국토교통부 자동차 등록 통계, 현대차·기아 연구 보고서  
        """)

    with col2:
        # ---- 연령대별 친환경 차량 선호도 분석 ----
        st.subheader("연령대별 친환경 차량 선호도")
        st.write("각 연령대별 친환경 차량(전기, 수소, 하이브리드, 플러그인하이브리드)의 선호도를 분석했습니다.")   

        fig2, ax = plt.subplots(figsize=(8, 5))
        ev_preference.plot(kind="bar", color="lightgreen", ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_xlabel("연령대")
        ax.set_ylabel("친환경 차량 구매 수")
        ax.set_title("연령대별 친환경 차량 구매 선호도")
        st.pyplot(fig2)
    
        st.markdown("""
        **📊 연령대별 친환경 차량 선호도 분석**  
        - **30~50대 고객층**: 전기차 및 하이브리드 차량 선호도 높음 → 연료비 절감 및 환경 보호 인식 증가.  
        - **친환경 차량 인프라 확대**: 충전소 및 유지보수 지원 정책 강화 필요.  
        - **정부 지원 활용**: 친환경 차량 보조금 및 세금 감면 혜택을 강조한 마케팅 필요.  
        - **맞춤형 차량 옵션 제공**: 연령대별 주행 패턴을 고려한 친환경 차량 추천 전략 필요.  

        참고 자료 출처: KATECH Insight, 국토교통부 자동차 등록 통계, 현대차·기아 연구 보고서  
        """)

    st.markdown("---")

    category_df=df[["성별", "연령대", "최근 구매 당시 나이", "최근 구매 제품", "차량 사이즈", "차량 유형", "최근 거래 금액"]]
    type_df=category_df.groupby(["성별", "연령대", "차량 유형"])[["최근 거래 금액"]].count().reset_index()

    size_df=df[["성별","연령대","차량 사이즈","최근 거래 금액"]]
    size_df=size_df.groupby(["성별","연령대","차량 사이즈"])[["최근 거래 금액"]].count().reset_index()

    col1, col2 = st.columns([1, 1])  # 좌우 여백 추가
    with col1:
        # ---- 성별에 따른 연령대별 선호 차량 유형 분석 ----
        st.subheader("남성 고객 연령대별 선호 차량 유형 분석")
        st.write("남성 고객들의 연령대별 선호 차량 유형을 분석하여 그래프로 표현했습니다.")

        type_man=type_df[type_df["성별"]=="남"]

        df_pivot = type_man.pivot_table(index='연령대', columns='차량 유형', values='최근 거래 금액', aggfunc='sum', fill_value=0)

        colors = sb.color_palette("Set2", n_colors=len(df_pivot.columns))

        fig1, ax = plt.subplots(figsize=(12, 8))
        df_pivot.plot(kind='bar', ax=ax, color=colors)
        ax.set_title('연령대별 선호 차량 유형 (남)', fontsize=16)
        ax.set_xlabel('연령대', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_ylabel('판매량', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig1)

        st.markdown("""
        **📊 남성 고객 연령대별 선호 차량 사이즈 분석**  
        - **20~30대 초반**: 준중형 & 중형 차량 선호 → 경제성 및 실용성이 중요.  
        - **30대 후반~50대 초반**: 중형 & 대형 차량 선호 → 가족 및 업무용 수요 증가.  
        - **50대 후반 이상**: 프리미엄 & 대형 차량 선호 → 승차감 및 브랜드 가치 중시.  
        - **중형 차량의 지속적인 인기**: 실용성과 가격 대비 성능이 균형을 이루는 선택지.  
        - **마케팅 활용**: 연령별 니즈를 반영한 맞춤형 차량 추천 및 프로모션 전략 필요.  

        참고 자료 출처: KATECH Insight, 국토교통부 자동차 등록 통계, 현대차·기아 연구 보고서  
        """)


    with col2:
        ## ---- 성별에 따른 연령대별 선호 차량 사이즈 분석 ----
        st.subheader("남성 고객 연령대별 선호 차량 사이즈 분석")
        st.write("남성 고객들의 연령대별 선호 차량 사이즈를 분석하여 그래프로 표현했습니다.")

        size_man=size_df[size_df["성별"]=="남"]

        df_pivot = size_man.pivot_table(index='연령대', columns='차량 사이즈', values='최근 거래 금액', aggfunc='sum', fill_value=0)

        colors = sb.color_palette("Set2", n_colors=len(df_pivot.columns))

        fig1, ax = plt.subplots(figsize=(12, 8))
        df_pivot.plot(kind='bar', ax=ax, color=colors)
        ax.set_title('연령대별 선호 차량 사이즈 (남)', fontsize=16)
        ax.set_xlabel('연령대', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_ylabel('판매량', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig1)

        st.markdown("""
        **📊 남성 고객 연령대별 선호 차량 유형 분석**  
        - **20~30대 초반**: 세단 선호도 높음 → 경제성 및 유지비 고려.  
        - **30대 후반~50대 초반**: SUV 선호도 증가 → 가족 및 레저 활동 수요 반영.  
        - **50대 후반~60대 이후**: SUV 선호 유지 → 운전 편의성과 안정성 중요.  
        - **SUV 인기 요인**: 공간 활용성, 높은 시야 확보, 하이브리드·전기차 옵션 증가.  
        - **마케팅 전략**: 연령대별 니즈 반영한 맞춤형 프로모션 및 차량 추천 필요.  

        참고 자료 출처: KATECH Insight, 국토교통부 자동차 등록 통계, 현대차·기아 연구 보고서  
        """)



    st.markdown("---")

    col1, col2 = st.columns([1, 1])  # 좌우 여백 추가
    with col1:
        ## ---- 성별에 따른 연령대별 선호 차량 유형 분석 ----
        st.subheader("여성 고객 연령대별 선호 차량 유형 분석")
        st.write("여성 고객들의 연령대별 선호 차량 유형을 분석하여 그래프로 표현했습니다.")
        
        type_woman=type_df[type_df["성별"]=="여"]

        df_pivot = type_woman.pivot_table(index='연령대', columns='차량 유형', values='최근 거래 금액', aggfunc='sum', fill_value=0)

        colors = sb.color_palette("Set2", n_colors=len(df_pivot.columns))

        fig2, ax = plt.subplots(figsize=(12, 8))
        df_pivot.plot(kind='bar', ax=ax, color=colors)
        ax.set_title('연령대별 선호 차량 유형 (여)', fontsize=16)
        ax.set_xlabel('연령대', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_ylabel('판매량', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig2)

        st.markdown("""
        **📊 여성 고객 연령대별 선호 차량 유형 분석**  
        - **20~30대 초반**: SUV 선호도 높음 → 높은 시야 확보 및 주행 안전성 고려.  
        - **30대 후반~50대 초반**: 세단 선호도 증가 → 경제성과 유지비 절감 요인이 작용.  
        - **50대 후반~60대 이후**: 세단 유지, SUV 수요 증가 → 장거리 운전 및 편의성 중시.  
        - **SUV 인기 요인**: 레저·패밀리카 수요 증가, 전기차·하이브리드 선택 확대.  
        - **마케팅 전략**: 연령별 라이프스타일 맞춤형 차량 추천 및 프로모션 제공.  

        참고 자료 출처: KATECH Insight, 국토교통부 자동차 등록 통계, 현대차·기아 연구 보고서  
        """)

    with col2:
        ## ---- 성별에 따른 연령대별 선호 차량 사이즈 분석 ----
        st.subheader("여성 고객 연령대별 선호 차량 사이즈 분석")
        st.write("여성 고객들의 연령대별 선호 차량 사이즈를 분석하여 그래프로 표현했습니다.")

        size_woman=size_df[size_df["성별"]=="여"]

        df_pivot = size_woman.pivot_table(index='연령대', columns='차량 사이즈', values='최근 거래 금액', aggfunc='sum', fill_value=0)

        colors = sb.color_palette("Set2", n_colors=len(df_pivot.columns))

        fig1, ax = plt.subplots(figsize=(12, 8))
        df_pivot.plot(kind='bar', ax=ax, color=colors)
        ax.set_title('연령대별 선호 차량 사이즈 (여)', fontsize=16)
        ax.set_xlabel('연령대', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_ylabel('판매량', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig1)

        st.markdown("""
        **📊 여성 고객 연령대별 선호 차량 사이즈 분석**  
        - **20~30대 초반**: 준중형 차량 선호 → 경제성 및 도심 운전 편리성 중시.  
        - **30대 후반~50대 초반**: 중형 차량 선호 증가 → 가족 이동 수요 증가 반영.  
        - **50대 후반~60대 이후**: 중형 및 준중형 유지, 일부 프리미엄 차량 선택 증가.  
        - **선호 요인**: 경제성, 유지비 절감, 주차 및 도심 운전 편의성.  
        - **마케팅 전략**: 연령별 차량 특성을 고려한 맞춤형 프로모션 및 혜택 제공.  

        참고 자료 출처: KATECH Insight, 국토교통부 자동차 등록 통계, 현대차·기아 연구 보고서  
        """)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])  # 좌우 여백 추가
    with col1:
        pass



st.markdown("---")




with tab2 :
    # 판매 데이터 분석 섹션
    st.header("판매 데이터 분석")
    st.write("판매 데이터 기반의 분석 인사이트를 제공합니다.")

    col1, col2 = st.columns([1, 1])  # 좌우 여백 추가
    with col1:
        # ---- 구매 유형별 선호도 ----
        st.subheader("시기 및 연료 구분별 판매 대수")
        st.write("고객들이 선호하는 연료 구분을 분석하여 그래프로 표현했습니다.")

        date_order = ["2023 1분기", "2023 2분기", "2023 3분기", "2023 4분기", "2024 1분기", "2024 2분기", "2024 3분기", "2024 4분기", "2025 1분기"]

        df["최근 구매 시점"] = pd.Categorical(df["최근 구매 시점"], categories=date_order, ordered=True)

        # 구매 기준 시점별 각 연료 구분의 개수 시각화
        fig1, ax = plt.subplots(figsize=(12, 8))

        sb.lineplot(x="최근 구매 시점", y="연번", hue="연료 구분", data=df, marker="o", palette="Set2", lw=2, ax=ax)
        ax.set_title("구매 기준 시점별 연료 구분별 판매 대수")
        ax.set_xlabel("최근 구매 시점")
        ax.set_ylabel("판매 대수")
        ax.set_xticks(range(len(date_order)))
        ax.set_xticklabels(date_order, rotation=30)
        ax.grid(axis="y", linestyle="--")
        ax.legend(title="연료 구분", loc="upper left")
        st.pyplot(fig1)

        st.write("""
        **분석 결과**
        """)
    with col2:
        pass



    # ---- 구매 유형별 선호도 ----
    st.subheader("구매 유형별 선호도")
    st.write("고객들이 선호하는 구매 유형을 분석하여 그래프로 표현했습니다.")

    fig, ax = plt.subplots(figsize=(8, 5))
    df["선호 거래 방식"].value_counts().plot(kind="bar", color=["skyblue", "salmon", "lightgreen"], ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_xlabel("구매 유형")
    ax.set_ylabel("고객 수")
    st.pyplot(fig)

    st.write("""
    **분석 결과 및 활용 방안**  
    - 대다수 고객이 온라인 및 대리점을 통한 구매를 선호  
    - 온라인 프로모션 강화 및 대리점별 특화 혜택 제공 필요  
    - 오프라인 고객 대상, 추가적인 서비스 패키지 제공 가능
    """)

    # # ---- 전기차 vs. 내연기관차 구매 트렌드 비교 ----
    # st.subheader("최근 3년간 전기차 구매 증가율 vs. 내연기관 차량 구매율 비교")
    # st.write("최근 3년간 전기차와 내연기관 차량의 구매 트렌드를 비교했습니다.")

    # recent_years = df[df["최근 구매 날짜"] >= (df["최근 구매 날짜"].max() - pd.DateOffset(years=3))]
    # ev_vs_ice = recent_years["연료 구분"].value_counts()
    # fig, ax = plt.subplots(figsize=(8, 5))
    # ev_vs_ice.plot(kind="bar", color=["green", "gray"], ax=ax)
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    # ax.set_xlabel("차량 유형")
    # ax.set_ylabel("구매 수")
    # ax.set_title("최근 3년간 전기차 vs. 내연기관차 구매 비교")
    # st.pyplot(fig)

    # st.write("""
    # **분석 결과 및 활용 방안**  
    # - 최근 3년간 전기차 판매량이 꾸준히 증가   
    # - 내연기관차보다 전기차 구매 비율이 높아지는 추세 
    # - 전기차 관련 금융 혜택 및 충전소 인프라 확장 필요
    # """)

    st.warning("근거가 부족한 분석, 다시 확인 필요")


    # ---- 연령대 및 성별 차량 구매 대수 ----
    st.subheader("지역별 고객 분포")
    st.write("고객들이 거주하는 지역별 분포를 나타냅니다.") 

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
    plt.tight_layout()
    st.pyplot(fig1)

    st.markdown("""
    **📊 분석 결과**  
    - 내용
    """)