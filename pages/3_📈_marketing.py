# 3_📈_marketing.py
#
#     마케팅 방안 정리
#         - 차량 1회만 구매한 일반 회원에 대해 차량 재구매 시 할인 혜택 제공된다는 메일 발송
#             - 데이터셋에서 일반 회원 목록 추출하는 방법 보여주기
#             - 실제 메일 발송은 X : 메일 예시 화면 만들어서 이미지로 첨부
#         - 앞으로의 차량 판매량 증가 확률이 높은 지역 몇몇에 대한 마케팅 전략 수립
#             - TOP 5 : 서울, 수원, 울산, 성남, 천안
#                 - 해당 지역 고객들의 차량 구매 패턴 파악 및 분석
#         - 이외에도 분석 내용 중 마케팅 전략으로 연결 가능한 내용 추가


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

# 차트 한글화 코드
import platform

from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')


st.title("📈 마케팅 전략")

st.write("이 페이지에서는 세그먼트에 따른 마케팅 전략을 추천합니다.")

df = pd.read_csv("data/고객db_전처리.csv")

st.markdown("---")


# 1. 일반 고객 대상 재구매 할인 혜택 제공
# 일반 고객 : 최근 6개월 이내 차량 구매 기록이 없고, 구매 이력이 1회인 고객

st.subheader("일반 고객 대상 재구매 할인 혜택 제공")

# 일반 고객 리스트 추출
normal_client = df.loc[df["고객 등급"] == "일반", ["이름", "휴대폰 번호", "이메일"]]
normal_client.reset_index(drop=True, inplace=True)

# 이메일 혹은 문자 메시지로 할인 혜택 설명
st.write("일반 고객 리스트")
st.write(normal_client)

# 메일 및 문자 예시 이미지 넣을 것

# 메일 예시
# st.image("images/email_sample.png", use_container_width=True)

# 문자 메시지 예시
# st.image("images/sms_sample.png", use_container_width=True)

st.markdown("---")

# 2. 지역/연령대별 마케팅 전략 수립

st.subheader("지역/연령대별 마케팅 전략 수립")

marketing_class = st.selectbox("마케팅 전략 구분", ["선택", "연령대별", "지역별", "고객 등급별", "거래 방식별"])

if marketing_class == "지역별":
    st.write("")

    col1, col2 = st.columns([1, 1])
    with col1 : 
        # 연료 구분 정렬 순서 지정
        fuel_order = ["전기", "하이브리드", "플러그인 하이브리드", "휘발유", "디젤", "수소"]

        # "연료 구분"을 Categorical 타입으로 변경하여 순서 지정
        df["연료 구분"] = pd.Categorical(df["연료 구분"], categories=fuel_order, ordered=True)

        # 데이터 그룹화 및 시각화를 위한 준비
        region_df = df.groupby(["거주 지역", "연료 구분"])["연번"].count().unstack()

        fig1, ax = plt.subplots(figsize=(12, 8))
        region_df.reindex(columns=fuel_order).plot(kind="barh", stacked=True, ax=ax)

        ax.set_title("거주 지역별 판매 차량 유형")
        ax.set_xlabel("판매 대수")
        ax.set_ylabel("거주 지역")

        st.pyplot(fig1)

    with col2:
        # 스캐터 플롯 생성
        fig2, ax = plt.subplots(figsize=(10, 6))
        scatter = sb.scatterplot(data=df, x="1인당 GDP (만 원)", y="인구 밀도", hue="거주 지역", palette="Set2", s=100, ax=ax)

        # 각 점 옆에 해당 거주 지역 표시
        for i in range(len(df)):
            ax.annotate(df["거주 지역"][i], (df["1인당 GDP (만 원)"][i], df["인구 밀도"][i]), 
                        textcoords="offset points", xytext=(5,5), ha='left', fontsize=9)

        ax.set_title("1인당 GDP와 인구 밀도에 따른 거주 지역")
        ax.set_xlabel("1인당 GDP (만 원)")
        ax.set_ylabel("인구 밀도")

        st.pyplot(fig2)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("""
        **분석 결과**  
        - 차량 구매 건수 : 서울, 수원, 광주, 청주, 울산 등이 높은 편
            - 인구 밀도가 높거나 1인당 평균 소득이 높다는 점이 영향을 미친 것으로 보임
        - 전기차 및 하이브리드 차량 구매 건수 : 전반적으로 높지 않음
            - 서울, 포항, 울산 등이 그나마 많은 편
        """)
    with col2:
        st.write("""
        **분석 결과**  
        - 주요 타겟팅 할 만한 지역 선정
            - 1인당 GDP가 높거나 인구 밀도가 높은 지역 : 서울, 수원, 울산, 성남, 천안
            - 추후 차량 구매 촉진이 유리한 환경이라고 판단됨
        """)

    st.subheader("")

    # 타겟 지역 선택
    st.subheader("🎯 타겟 지역별 마케팅 전략")

    region = st.selectbox("타겟 지역 선택", ["-", "서울특별시", "경기도 수원시", "울산광역시", "경기도 성남시", "충청남도 천안시"])

    age_order = ["20대 초반", "20대 중반", "20대 후반", "30대 초반", "30대 중반", "30대 후반", "40대 초반", "40대 중반", "40대 후반",
             "50대 초반", "50대 중반", "50대 후반", "60대 초반", "60대 중반", "60대 후반", "70대 초반"]

    df["연령대"] = pd.Categorical(df["연령대"], categories=age_order, ordered=True)

    # 지역에 따른 마케팅 전략 추천
    analysis = {
        "서울특별시": "\n\n- 1. 20대 중반이 가장 많이 구매 : 주 타겟층\n   - 선호 차량 유형 : 중형 SUV/세단\n- 2. 전 연령대에 걸쳐 판매 가능성 : 40대부터 60대까지 꾸준한 소비\n   - 선호 차량 유형 : 중형 SUV/세단\n- 3. 이미 130개 이상의 대리점/지점 존재\n    - 전시장 확대보다는 더욱 다양한 차량 라인업 제공이 필요\n",
        "경기도 수원시": "\n\n- 1. 40대 초반과 60대 중반이 가장 많이 구매 : 주 타겟층\n  - 선호 차량 유형 : 준중형 세단\n- 2. 전반적으로 중형~준중형 사이즈 차량 수요 높음\n    - 차종 역시 세단 선호도가 높음\n",
        "울산광역시": "\n\n- 1. 30대 후반과 50대 중반 : 주 타겟층\n    - 중형 SUV 선호\n- 2. 비교적 전 연령대에서 고른 구매 수요를 보임\n   - 중형 SUV 및 세단 선호도 높음\n- 3. SUV의 선호도가 타지역에 비해 두드러짐\n    - SUV 라인업 확대 필요\n",
        "경기도 성남시": "\n\n- 1. 40대 초반과 50대 중후반 : 주 타겟층\n  - 중형 세단 선호\n- 2. 40대 이상의 연령대에서 주된 구매 수요를 보임\n  - 준중형/중형 세단 선호도 높음\n- 3. 30대 이하의 연령대에서 차량 구매 수요가 낮은 편\n  - 저가 전략 혹은 젊은 세대를 위한 마케팅 필요\n",
        "충청남도 천안시": "\n\n- 1. 40대 후반 : 주 타겟층\n    - 준중형 세단/해치백 선호\n- 2. 전반적인 수요가 높지 않음\n    - 사람들의 차량 구매를 유도할 수 있는 마케팅 필요\n"
    }

    strategy = {
        "서울특별시": "\n\n- SNS 광고\n     - 20대를 위한 YOUNG 마케팅이 필요\n     - 다른 연령대를 위한 차량 라인업 홍보 역시 SNS 통해 실시\n- 중형 SUV/세단 라인업 확대\n   - 전 연령대에서의 활발한 구매 촉진을 위해 판매량이 높은 차량 라인업 확대에 집중\n",
        "경기도 수원시": "\n\n- 전통적 미디어(신문, TV 등)를 통한 광고\n     - 40대와 60대를 위한 패밀리카 마케팅이 필요\n- 준중형 세단 라인업 확대\n     - 판매량이 높은 세단의 장점을 강조하는 마케팅\n",
        "울산광역시": "\n\n- 패밀리카 및 SUV 라인업 홍보\n     - 30대와 50대를 위한 SUV 위주 마케팅 필요\n- SUV 라인업 확대 필요\n    - SUV의 선호도가 높은 만큼 라인업 확대로 판매량 증대 가능\n",
        "경기도 성남시": "\n\n- 40대와 50대를 위해 친숙한 이미지 강조하는 마케팅\n   - 현대자동차의 익숙하면서도 안정적인 이미지 강조\n  - 중형 세단 라인업 홍보\n- 젊은 세대를 위한 저가 전략 마케팅\n   - 30대 이하 연령대의 저조한 구매 수요를 증대하기 위한 전략 필요\n",
        "충청남도 천안시": "\n\n- 차량 구매 유도를 위한 저가/할인 마케팅 전략\n    - 전반적으로 차량 구매 수요가 그리 높지 않기 때문에 이를 유도하기 위해 할인 혜택 마케팅 필요\n- 디자인/성능 등에서 사람들의 이목을 끌 수 있는 마케팅\n    - 차량에 관심이 낮은 사람들의 차량 구매 관심도를 조금이나마 높일 수 있는 방안\n"
    }

    col1, col2 = st.columns([1, 1])
    with col1:
        # 지역의 나이대에 따른 선호 차량 사이즈 및 유형
        # 해당 지역만 추출
        city = df.loc[df["거주 지역"] == region, :]

        # 연령대별 선호 차량 사이즈 및 유형 집계
        size_counts = city.groupby("연령대")["차량 사이즈"].value_counts().unstack()
        type_counts = city.groupby("연령대")["차량 유형"].value_counts().unstack()

        if region != "-":
            # 시각화 - 연령대별 선호 차량 사이즈
            fig, ax = plt.subplots(figsize=(10, 5))
            size_counts.plot(kind="bar", stacked=True, colormap="viridis", alpha=0.85, ax=ax)

            ax.set_title(f"{region} 연령대별 선호 차량 사이즈")
            ax.set_xlabel("연령대")
            ax.set_ylabel("선호 차량 수")
            ax.legend(title="차량 사이즈")
            ax.set_xticklabels(size_counts.index, rotation=60)
            ax.grid(axis="y", linestyle="--", alpha=0.7)

            st.pyplot(fig)        

            st.write("")

            st.write("📢 **분석 결과**:", analysis[region])
        with col2:
            # 시각화 - 연령대별 선호 차량 유형
            fig, ax = plt.subplots(figsize=(10, 5))
            type_counts.plot(kind="bar", stacked=True, colormap="plasma", alpha=0.85, ax=ax)

            ax.set_title(f"{region} 연령대별 선호 차량 유형")
            ax.set_xlabel("연령대")
            ax.set_ylabel("선호 차량 수")
            ax.legend(title="차량 유형")
            ax.set_xticklabels(type_counts.index, rotation=60)
            ax.grid(axis="y", linestyle="--", alpha=0.7)

            st.pyplot(fig)

            st.write("")

            st.write("🚀 **잠재적 마케팅 전략**:", strategy[region])
            
elif marketing_class == "연령대별":
    # 연료 구분 정렬 순서 지정
    fuel_order = ["전기", "하이브리드", "플러그인 하이브리드", "휘발유", "디젤", "수소"]
    
    age_order = ["20대 초반", "20대 중반", "20대 후반", "30대 초반", "30대 중반", "30대 후반", "40대 초반", "40대 중반", "40대 후반",
              "50대 초반", "50대 중반", "50대 후반", "60대 초반", "60대 중반", "60대 후반", "70대 초반"]

    df["연료 구분"] = pd.Categorical(df["연료 구분"], categories=fuel_order, ordered=True)
    df["연령대"] = pd.Categorical(df["연령대"], categories=age_order, ordered=True)

    # 데이터 그룹화 및 시각화를 위한 준비
    age_df = df.groupby(["연령대", "연료 구분"])["연번"].count().unstack()

    fig, ax = plt.subplots(figsize=(12, 8))
    age_df.reindex(columns=fuel_order).plot(kind="barh", stacked=True, ax=ax)

    ax.set_title("연령대별 판매 차량 유형")
    ax.set_xlabel("판매 대수")
    ax.set_ylabel("연령대")

    st.pyplot(fig)

    st.write("""
    **분석 결과**  
- 휘발유 차량의 높은 점유율  
    - 전 연령대에서 휘발유 차량이 가장 많이 판매됨  
    - 특히 40대 초반~50대 초반 연령대에서 가장 큰 비중을 차지  
- 디젤 차량의 강세  
    - 60대 후반~70대 초반의 고연령층에서 디젤 차량이 높은 비중을 차지  
    - 젊은 연령층으로 갈수록 디젤 차량의 비중이 점차 감소하는 경향  
- 수소 차량의 점유율 증가  
    - 50대 이상 연령층에서 수소차 비중이 높은 편  
    - 20~30대에서는 수소 차량이 상대적으로 적음
- 젊은 층의 전기차/하이브리드 구매  
    - 젊은 층 (20~30대)에서만 일부 판매  
    - 연령대가 올라갈수록 전기차 및 하이브리드 판매 비율이 줄어듦
    """)

    st.write("")

    size_counts = df.groupby("최근 구매 연도")["고객 등급"].value_counts().unstack().fillna(0)

    # 시각화 - 고객 등급별 최근 차량 구매 연도
    fig, ax = plt.subplots(figsize=(10, 5))

    size_counts.plot(kind="line", marker="o", colormap="viridis", alpha=0.85, ax=ax)

    ax.set_xticks(size_counts.index)
    ax.set_xticklabels(size_counts.index, rotation=0)

    ax.set_title(f"연도별 차량 구매 건수")
    ax.set_xlabel("연도")
    ax.set_ylabel("선호 차량 수")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(fig)

    st.write("")

    st.write("""
    **분석 결과**
    - 일반 고객의 감소와 VIP 고객의 증가
        - 일반 고객의 감소는 기존 일반 고객의 신규 차량 구매가 활발하다는 의미
        - 차량 재구매 시 혜택을 더욱 확대할 필요가 있음
    - 신규 고객 유입 증가
        - 신규 고객의 지속적인 유입을 위한 마케팅 전략 필요
    """)

    st.subheader("")

    # 타겟 지역 선택
    st.subheader("🎯 연령대별 마케팅 전략")

    age_group = st.selectbox("타겟 연령대 선택", ["-", "20대", "30대", "40대", "50대", "60대 이상"])

    # 연령대에 따른 마케팅 전략 추천
    strategy = {
        "20대": "\n\n**분석 결과**\n- 1. 중형 세단/SUV 선호\n- 2. 전기 및 하이브리드 차량의 선호도가 낮음\n    - 연비보다는 주행 성능이나 연료 충전 편의성을 더 중요하게 생각할 가능성\n- 3.	대형 및 해치백 차량은 인기가 낮음\n    - 가격, 실용성, 유지 비용 등의 요인이 반영된 결과\n\n**잠재적 마케팅 전략**\n- 전기 및 하이브리드 차량의 장점을 강조하는 마케팅 전략\n   - 보조금 및 충전 인프라 홍보 필요\n- 중형 세단/SUV 라인업 확대\n    - 중형 세단/SUV의 선호도가 높은 만큼 라인업 확대로 판매량 증대 가능\n- 대형 및 해치백 차량 저가 모델 출시\n    - 저가형 대형 및 해치백 차량 출시로 인기 증대 가능",
        "30대": "\n\n**분석 결과**\n- 1. 중형 SUV 선호\n    - SUV에서 친환경 연료(수소) 선호도 증가\n- 2. 프리미엄 및 대형 차량 수요 증가\n    - 경제적인 여유 확보로 인한 결과물로 보임\n\n **잠재적 마케팅 전략**\n- 중형 SUV 라인업 확대\n    - 중형 SUV의 선호도가 높은 만큼 라인업 확대로 판매량 증대 가능\n- 프리미엄 및 대형 차량 라인업 확대\n    - 경제적 여유가 있는 30대를 위한 프리미엄 및 대형 차량 라인업 확대 필요",
        "40대": "\n\n**분석 결과**\n- 1.중형과 대형 차량 선호\n     - 중형 차량 중 수소 연료 선호도 높음 (친환경 차량 수요 증가)\n      - 패밀리카, 브랜드 가치, 유지비 등을 고려하는 구매 경향\n- 2. 해치백은 거의 선택되지 않음\n    - 주행 안전성과 실내 공간을 고려하는 성향\n\n**잠재적 마케팅 전략**\n- 수소 연료 차량 홍보\n     - 수소 연료 차량의 친환경성을 강조하는 마케팅\n- 패밀리카 및 브랜드 가치 강조\n     - 친숙한 이미지 기반으로 패밀리어 마케팅 실시\n- 대형 및 해치백 차량 홍보 확대\n    - 카고 공간 및 주행 안전성을 강조하는 패밀리 마케팅 전략",
        "50대": "\n\n**분석 결과**\n- 1. 친환경 연료(수소, 하이브리드) 선호도 다른 연령대에 비해 높음\n     - 연료 효율성과 유지비 절감을 고려하여 하이브리드 및 플러그인 하이브리드 선택 증가\n\n**잠재적 마케팅 전략**\n- 친환경 연료 차량 홍보\n     - 친환경 연료의 장점을 강조하는 마케팅 전략\n- 연료 효율성 및 유지비 절감을 강조하는 마케팅\n     - 연료 효율성 및 유지비 절감을 강조하는 마케팅 전략\n- 수소 및 하이브리드 차량 라인업 확대\n    - 친환경 연료 차량의 선호도가 높은 만큼 라인업 확대로 판매량 증대 가능",
        "60대 이상": "\n\n**분석 결과**\n- 1. 타 연령대에 비해 높은 디젤 선호도\n   - 디젤 차량의 연료 효율성 및 주행 안정성을 중시하는 경향\n    - 디젤 차량의 승차감에 익숙한 장년층의 특성이 반영됨\n- 2. 전기 및 하이브리드 차량의 선호도 낮음\n   - 전기 및 하이브리드 차량의 충전 인프라 부족 및 주행 거리 등의 문제로 인한 선호도 저하\n\n**잠재적 마케팅 전략**\n- 디젤 차량 홍보\n    - 디젤 차량의 연료 효율성 및 주행 안정성을 강조하는 마케팅 전략\n- 전기 및 하이브리드 차량의 장점을 강조하는 마케팅\n    - 전기 및 하이브리드 차량의 장점을 강조하는 마케팅 전략\n     - 디젤 차량 이용 시 환경 부담금 발생한다는 점 강조"
    }

    # 연령대에 따른 선호 차량 사이즈 및 유형
    # 해당 연령대만 추출
    if age_group == "60대 이상":
        gen = df.loc[(df["연령대"].str.split(" ").str[0]).isin(["60대", "70대"]), :]
    else:
        gen = df.loc[df["연령대"].str.split(" ").str[0] == age_group, :]

    # 고객 등급별 선호 차량 사이즈 및 유형 집계
    size_counts = gen.groupby("차량 사이즈")["연료 구분"].value_counts().unstack()
    type_counts = gen.groupby("차량 유형")["연료 구분"].value_counts().unstack()

    if age_group != "-":
        # 시각화 - 고객 등급별 선호 차량 사이즈
        fig, ax = plt.subplots(figsize=(10, 5))
        size_counts.plot(kind="bar", stacked=True, colormap="viridis", alpha=0.85, ax=ax)

        ax.set_title(f"{age_group} 고객 등급별 선호 차량 사이즈")
        ax.set_xlabel("차량 사이즈")
        ax.set_ylabel("선호 차량 수")
        ax.legend(title="연료 구분")
        ax.set_xticklabels(size_counts.index, rotation=0)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        st.pyplot(fig)

        st.write("")

        # 시각화 - 고객 등급별 선호 차량 유형
        fig, ax = plt.subplots(figsize=(10, 5))
        type_counts.plot(kind="bar", stacked=True, colormap="plasma", alpha=0.85, ax=ax)

        ax.set_title(f"{age_group} 고객 등급별 선호 차량 유형")
        ax.set_xlabel("차량 유형")
        ax.set_ylabel("선호 차량 수")
        ax.legend(title="연료 구분")
        ax.set_xticklabels(type_counts.index, rotation=0)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        st.pyplot(fig)

        st.write("")

        st.write("📢 추천 마케팅 전략:", strategy[age_group])
elif marketing_class == "고객 등급별":
    marketing_order = ["신규", "일반", "VIP"]
    fuel_order = ["전기", "하이브리드", "플러그인 하이브리드", "휘발유", "디젤", "수소"]

    df["고객 등급"] = pd.Categorical(df["고객 등급"], categories=marketing_order, ordered=True)
    df["연료 구분"] = pd.Categorical(df["연료 구분"], categories=fuel_order, ordered=True)

    # 데이터 그룹화 및 시각화를 위한 준비
    age_df = df.groupby(["고객 등급", "연료 구분"])["연번"].count().unstack()

    fig, ax = plt.subplots(figsize=(12, 8))
    age_df.reindex(columns=fuel_order).plot(kind="bar", stacked=True, ax=ax)

    ax.set_title("고객 등급별 판매 차량 유형")
    ax.set_xlabel("판매 대수")
    ax.set_ylabel("연령대")
    ax.set_xticklabels(age_df.index, rotation=0)

    st.pyplot(fig)

