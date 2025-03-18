# 1_📌_customer_input.py
#
#     고객 추천 모델 페이지 : 고객이 정보를 입력하면 그에 따른 차량 종류 추천하는 시스템
#         - 5개 모델 제작 : 각각 정확도는 98% 정도이지만, 추천 차량이 약간씩 다름
#             - 입력 정보 : 거주 지역, 예산, 차량 사이즈, 차량 유형, 연료 구분
#             - 출력 정보 : 추천 차종 (1~5개)
#                - 5개 모델의 연산 결과를 하나의 리스트로 제작, 해당 리스트 내 유니크한 값들을 모두 추천
#         - 신용 카드로 구매할 시 10% 포인트로 제공한다는 것 공지하면서, 가격대가 조금 더 높은 차량 목록 자연스럽게 추천
#         - 전기차가 아닌 차종 선택 시 대안이 될 수 있는 전기차 추천 동반 : 지역에 따른 보조금 차이 반영하여 추천
#
#     화면에 보여질 내용
#         - 정보 입력란 5개 : 예산, 거주 지역, 차량 사이즈, 차량 유형, 연료 구분
#             - 예산 : 직접 입력
#             - 나머지 4개 : 드롭다운 메뉴 선택
#         - 추천 받기 버튼 : 추천 결과를 보여주는 버튼
#         - 결과 출력 : 추천 결과를 1개~5개까지 보여줌 -> 순위 없이 결과 리스트 내부의 값들을 랜덤 순서로 보여줌
#         - 신용 카드 혜택 안내 : 10% 포인트 제공
#             - 팝업창 혹은 info 메시지 형태 : 약간의 딜레이(로딩 동그라미) 후 리스트 보여줌
#             - 버튼 형태 : 클릭 시 가격대 조금 더 높은 차량 N개 정보 보여줌
#         - 전기차 추천 : 전기차가 아닌 차종 선택 시 대안으로 전기차 추천
#             - 지역에 따른 보조금 차이 반영하여 자동으로 추천 : 1~3대 추천


import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import time



base_dir = os.path.dirname(os.path.abspath(__file__))


# 모델 로드
model_dir = os.path.join(base_dir, "..", "model", "models")

dtc_path = os.path.join(model_dir, "DecisionTree 모델.pkl")
rfc_path = os.path.join(model_dir, "RandomForest 모델.pkl")
gbc_path = os.path.join(model_dir, "GradientBoosting 모델.pkl")
lgb_path = os.path.join(model_dir, "LightGBM 모델.pkl")

def load_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {path}")
    return joblib.load(path)

dtc = load_model(dtc_path)
rfc = load_model(rfc_path)
gbc = load_model(gbc_path)
lgb = load_model(lgb_path)


# 데이터셋 로드
data_dir = os.path.join(base_dir, "..", "data")

data_path = os.path.join(data_dir, "고객db_전처리.csv")

def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {path}")
    return pd.read_csv(path)

df = load_data(data_path)


st.title("고객 정보 입력 & 차량 추천")


# 사용자 입력
budget = st.number_input("구매 예산을 입력하세요. (단위: 만원)", min_value=3300, max_value=200000, step=500, value=5000)
region = st.selectbox("거주 지역이 어떻게 되시나요?", ['서울특별시', '부산광역시', '인천광역시', '대구광역시', '광주광역시', '대전광역시',
        '울산광역시', '경기도 수원시', '경기도 성남시', '충청남도 천안시', '충청북도 청주시', '전라북도 전주시', '전라남도 목포시', '경상북도 포항시',
        '경상남도 창원시'])
car_size = st.selectbox("선호하시는 차량 사이즈가 무엇인가요?", ["준중형", "중형", "준대형", "대형", "프리미엄"])
car_type = st.selectbox("선호하시는 차량 유형은 무엇인가요?", ["세단", "SUV", "해치백"])
fuel_type = st.selectbox("어떤 연료 구분의 차량을 찾고 계신가요?", ["디젤", "수소", "전기", "플러그인 하이브리드", "하이브리드", "휘발유"])


# 추천 버튼
if st.button("추천 받기"):

    with st.spinner("추천 결과를 생성 중입니다..."):
        time.sleep(3)
        st.success("추천 결과가 생성되었습니다.")

    region_list = {
        "경기도 성남시": [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "경기도 수원시": [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "경상남도 창원시": [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
        "경상북도 포항시": [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        "광주광역시": [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
        "대구광역시": [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
        "대전광역시": [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
        "부산광역시": [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        "서울특별시": [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        "울산광역시": [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
        "인천광역시": [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
        "전라남도 목포시": [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
        "전라북도 전주시": [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
        "충청남도 천안시": [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        "충청북도 청주시": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    }

    car_size_list = {
        "대형": [1,0,0,0,0],
        "준대형": [0,1,0,0,0],
        "준중형": [0,0,1,0,0],
        "중형": [0,0,0,1,0],
        "프리미엄": [0,0,0,0,1]
    }

    car_type_list = {
        "SUV": [1,0,0],
        "세단": [0,1,0],
        "해치백": [0,0,1]
    }

    fuel_type_list = {
        "디젤": [1,0,0,0,0,0],
        "수소": [0,1,0,0,0,0],
        "전기": [0,0,1,0,0,0],
        "플러그인 하이브리드": [0,0,0,1,0,0],
        "하이브리드": [0,0,0,0,1,0],
        "휘발유": [0,0,0,0,0,1]
    }


    # 사용자 입력 데이터를 모델이 예측할 수 있는 형태로 변환
    user_data = np.hstack([budget * 10000, region_list[region], car_size_list[car_size], car_type_list[car_type],
                          fuel_type_list[fuel_type]]).reshape(1, -1)[0]
    
    user_data = np.array(user_data).reshape(1, 30)


    # 각 모델을 통해 추천 결과 생성
    recom_list = []
    recom_list.append(dtc.predict(user_data)[0])
    recom_list.append(rfc.predict(user_data)[0])
    recom_list.append(gbc.predict(user_data)[0])
    recom_list.append(lgb.predict(user_data)[0])


    # 중복 제거 및 정렬
    recom_list = list(set(recom_list))


    # 차량 정보 리스트
    car_list = {
            "Avante (CN7 N)": "아반떼 CN7 N\n - 가격: 2,485만원\n - 연비: 15.1km/L\n - 배기량: 1,598cc\n - 최대출력: 123마력\n - 최대토크: 15.0kg.m",
            "Avante (CN7 HEV)": "아반떼 CN7 HEV\n - 가격: 2,785만원\n - 연비: 19.2km/L\n - 배기량: 1,598cc\n - 최대출력: 105마력\n - 최대토크: 17.0kg.m\n",
            "Grandeur (GN7 HEV)": "그랜저 GN7 HEV\n - 가격: 3,785만원\n - 연비: 14.6km/L\n - 배기량: 1,999cc\n - 최대출력: 159마력\n - 최대토크: 19.3kg.m\n",
            "G80 (RG3)": "G80 RG3\n - 가격: 6,750만원\n - 연비: 10.5km/L\n - 배기량: 3,778cc\n - 최대출력: 315마력\n - 최대토크: 40.0kg.m\n",
            "Santa-Fe ™": "Santa-Fe ™\n - 가격: 3,870만원\n - 연비: 14.6km/L\n - 배기량: 1,598cc\n - 최대출력: 159마력\n - 최대토크: 19.3kg.m\n",
            "Santa-Fe (MX5 PHEV)": "Santa-Fe MX5 PHEV\n - 가격: 4,785만원\n - 연비: 15.1km/L\n - 배기량: 1,598cc\n - 최대출력: 123마력\n - 최대토크: 15.0kg.m\n",
            "Tucson (NX4 PHEV)": "Tucson NX4 PHEV\n - 가격: 3,785만원\n - 연비: 19.2km/L\n - 배기량: 1,598cc\n - 최대출력: 105마력\n - 최대토크: 17.0kg.m\n",
            "Palisade (LX2)": "Palisade LX2\n - 가격: 3,785만원\n - 연비: 14.6km/L\n - 배기량: 1,999cc\n - 최대출력: 159마력\n - 최대토크: 19.3kg.m\n",
            "IONIQ (AE EV)": "IONIQ AE EV\n - 가격: 6,750만원\n - 연비: 10.5km/L\n - 배기량: 3,778cc\n - 최대출력: 315마력\n - 최대토크: 40.0kg.m\n",
            "IONIQ 6 (CE)": "IONIQ 6 CE\n - 가격: 3,870만원\n - 연비: 14.6km/L\n - 배기량: 1,598cc\n - 최대출력: 159마력\n - 최대토크: 19.3kg.m\n",
            "NEXO (FE)": "NEXO FE\n - 가격: 4,785만원\n - 연비: 15.1km/L\n - 배기량: 1,598cc\n - 최대출력: 123마력\n - 최대토크: 15.0kg.m\n",
            "G90 (HI)": "G90 HI\n - 가격: 3,785만원\n - 연비: 19.2km/L\n - 배기량: 1,598cc\n - 최대출력: 105마력\n - 최대토크: 17.0kg.m\n",
            "G70 (IK)": "G70 IK\n - 가격: 3,785만원\n - 연비: 14.6km/L\n - 배기량: 1,999cc\n - 최대출력: 159마력\n - 최대토크: 19.3kg.m\n",
            "i30 (PD)": "i30 PD\n - 가격: 6,750만원\n - 연비: 10.5km/L\n - 배기량: 3,778cc\n - 최대출력: 315마력\n - 최대토크: 40.0kg.m\n",
            "GV80 (RS4)": "GV80 RS4\n - 가격: 3,870만원\n - 연비: 14.6km/L\n - 배기량: 1,598cc\n - 최대출력: 159마력\n - 최대토크: 19.3kg.m\n",
            "G90 (RS4)": "G90 RS4\n - 가격: 4,785만원\n - 연비: 15.1km/L\n - 배기량: 1,598cc\n - 최대출력: 123마력\n - 최대토크: 15.0kg.m\n"
    }
    
    # 최소 가격 리스트
    min_price_list = {
        "Avante (CN7 N)": "3,309만원",
        "Avante (CN7 HEV)": "2,485만원",
        "Grandeur (GN7 HEV)": "4,267만원",
        "G80 (RG3)": "8,275만원",
        "Santa-Fe ™": "3,492만원",
        "Santa-Fe (MX5 PHEV)": "3,870만원",
        "Tucson (NX4 PHEV)": "3,205만원",
        "Palisade (LX2)": "4,383만원",
        "IONIQ (AE EV)": "6,715만원",
        "IONIQ 6 (CE)": "3,695만원",
        "NEXO (FE)": "6,950만원",
        "G90 (HI)": "1억 2,960만원",
        "G70 (IK)": "4,398만원",
        "i30 (PD)": "1,855만원",
        "GV80 (RS4)": "6,945만원",
        "G90 (RS4)": "1억 7,520만원"
    }
    
    # 결과 출력
    st.subheader("추천 차량 리스트")

    # 차량 개수에 따라 컬럼을 동적으로 생성 (예: 3개씩 한 줄)
    columns_per_row = 3  
    num_cars = len(recom_list)

    # Markdown 테이블 헤더 생성 (열 개수에 맞게)
    header_titles = [f"추천 차량 {i+1}" for i in range(min(columns_per_row, num_cars))]
    table_header = "| " + " | ".join(header_titles) + " |\n"
    table_header += "| " + " | ".join(["---"] * min(columns_per_row, num_cars)) + " |\n"

    # 이미지 행 및 텍스트 행 생성
    img_rows = []
    text_rows = []

    for idx, car_name in enumerate(recom_list):
        # 차량 이미지 URL 가져오기
        image_url = df.loc[df['최근 구매 제품'] == car_name, '모델 사진'].to_numpy()[0]
        img_tag = f'<img src="{image_url}" width="250">' if image_url else "이미지 없음"

        # 차량 정보 정리
        fuel_type = df.loc[df['최근 구매 제품'] == car_name, '연료 구분'].to_numpy()[0]
        price = f"{min_price_list.get(car_name, '가격 정보 없음')}~"
        mileage = df.loc[df['최근 구매 제품'] == car_name, '차량 연비'].to_numpy()[0]
        engine = df.loc[df['최근 구매 제품'] == car_name, '배기량'].to_numpy()[0]
        power = df.loc[df['최근 구매 제품'] == car_name, '최대 출력'].to_numpy()[0]

        # 차량 정보 요약 생성 (HTML <br> 사용)
        summary = f"**{car_name}**<br>연료 구분: {fuel_type}<br>가격: {price}<br>연비: {mileage}<br>배기량: {engine}<br>최대 출력: {power}"

        # 행 데이터를 리스트에 추가
        img_rows.append(img_tag)
        text_rows.append(summary)

        # 줄바꿈 처리 (3개씩 한 줄)
        if (idx + 1) % columns_per_row == 0 or idx == num_cars - 1:
            img_row = "| " + " | ".join(img_rows) + " |\n"
            text_row = "| " + " | ".join(text_rows) + " |\n"
            table_header += img_row + text_row  # 테이블에 추가
            img_rows, text_rows = [], []  # 리스트 초기화

    # Markdown을 사용하여 테이블 출력 (HTML 허용)
    st.markdown(table_header, unsafe_allow_html=True)
    
    st.subheader("")
    

    # 추가 혜택 제공 (예: 신용카드 혜택 안내)
    # 사용자가 설정한 예산의 150% 수준의 차량 추천
    st.info("신용카드로 구매 시 10% 포인트 적립 혜택을 받을 수 있습니다!")

    cred_data = np.hstack([budget * 15000, region_list[region], car_size_list[car_size], car_type_list[car_type],
                          fuel_type_list[fuel_type]]).reshape(1, -1)[0]
    
    cred_data = np.array(cred_data).reshape(1, 30)

    cred_list = []
    cred_list.append(dtc.predict(cred_data)[0])
    cred_list.append(rfc.predict(cred_data)[0])
    cred_list.append(gbc.predict(cred_data)[0])
    cred_list.append(lgb.predict(cred_data)[0])


    # 중복 제거 및 정렬
    cred_list = list(set(cred_list))


    # 가격대 조금 더 높은 제품 추천
    # 최초 추천 리스트와 동일한 결과 나올 경우 실시 X
    # 실시하더라도 최초 추천 리스트에는 존재하지 않는 차종만 추천
    if cred_list != recom_list:
        st.subheader("추천 차량 리스트")
        with st.spinner("추천 결과를 생성 중입니다..."):
            time.sleep(3)
            st.success("아래 차량은 어떠신가요?")

        # 차량 개수에 따라 컬럼을 동적으로 생성 (한 줄에 3개씩 표시)
        columns_per_row = 3
        filtered_cred_list = [i for i in cred_list if i not in recom_list]
        num_cars = len(filtered_cred_list)

        # 추천 차량 번호를 포함한 테이블 헤더 생성
        header_titles = [f"추천 차량 {i+1}" for i in range(min(columns_per_row, num_cars))]
        table_header = "| " + " | ".join(header_titles) + " |\n"
        table_header += "| " + " | ".join(["---"] * min(columns_per_row, num_cars)) + " |\n"

        # 이미지 행 및 텍스트 행 생성
        img_rows = []
        text_rows = []

        for idx, car_name in enumerate(filtered_cred_list):
            # 차량 이미지 URL 가져오기
            image_url = df.loc[df['최근 구매 제품'] == car_name, '모델 사진'].to_numpy()[0]
            img_tag = f'<img src="{image_url}" width="250">' if image_url else "이미지 없음"

            # 차량 정보 정리
            fuel_type = df.loc[df['최근 구매 제품'] == car_name, '연료 구분'].to_numpy()[0]
            price = f"{min_price_list.get(car_name, '가격 정보 없음')}~"
            mileage = df.loc[df['최근 구매 제품'] == car_name, '차량 연비'].to_numpy()[0]
            engine = df.loc[df['최근 구매 제품'] == car_name, '배기량'].to_numpy()[0]
            power = df.loc[df['최근 구매 제품'] == car_name, '최대 출력'].to_numpy()[0]

            # 차량 정보 요약 생성 (HTML <br> 사용)
            summary = f"**{car_name}**<br>연료 구분: {fuel_type}<br>가격: {price}<br>연비: {mileage}<br>배기량: {engine}<br>최대 출력: {power}"

            # 행 데이터를 리스트에 추가
            img_rows.append(img_tag)
            text_rows.append(summary)

            # 줄바꿈 처리 (3개씩 한 줄)
            if (idx + 1) % columns_per_row == 0 or idx == num_cars - 1:
                img_row = "| " + " | ".join(img_rows) + " |\n"
                text_row = "| " + " | ".join(text_rows) + " |\n"
                table_header += img_row + text_row  # 테이블에 추가
                img_rows, text_rows = [], []  # 리스트 초기화

        # Markdown을 사용하여 테이블 출력 (HTML 허용)
        st.markdown(table_header, unsafe_allow_html=True)

    st.subheader("")
    

    # 전기차 추천
    # 사용자가 전기차가 아닌 차종을 선택한 경우 대안으로 전기차 추천
    if fuel_type in ["전기", "플러그인 하이브리드", "하이브리드"]:
        pass
    else:
        st.info("전기차가 아닌 차종을 선택하셨습니다. 보조금도 받고, 전기차로 구매하시는 건 어떠신가요?")

        elec_car_compen = {
            "서울특별시": 9000000,
            "부산광역시": 10500000,
            "대구광역시": 11000000,
            "인천광역시": 10600000,
            "광주광역시": 11000000,
            "대전광역시": 12000000,
            "울산광역시": 10500000,
            "경기도 수원시": 10500000,
            "경기도 성남시": 11000000,
            "충청북도 청주시": 14000000,
            "충청남도 천안시": 14000000,
            "전라북도 전주시": 15000000,
            "전라남도 목포시": 15500000,
            "경상북도 포항시": 13000000,
            "경상남도 창원시": 13000000
        }


        # 숫자를 천 단위로 쉼표로 구분하는 함수
        def comma(x):
            return format(x, ',')
        
        st.info(f"{region}의 전기차 보조금은 {comma(elec_car_compen[region])}원입니다.")

        compen = elec_car_compen[region]
        recom_elec = df.loc[(df["최근 거래 금액"] <= budget * 10000 + compen) & (df["연료 구분"].isin(["전기", "플러그인 하이브리드", "하이브리드"])), "최근 구매 제품"].to_numpy()[0:3]

        st.subheader("추천 차량 리스트")
        with st.spinner("추천 결과를 생성 중입니다..."):
            time.sleep(3)
            st.success("아래 차량은 어떠신가요?")

        # 한 줄에 몇 개의 차량을 표시할지 결정 (예: 3개)
        columns_per_row = 3  
        num_cars = len(recom_elec)

        if num_cars > 0:
            st.subheader("전기차 추천 리스트")

            # 추천 차량 번호를 포함한 테이블 헤더 생성
            header_titles = [f"추천 차량 {i+1}" for i in range(min(columns_per_row, num_cars))]
            table_header = "| " + " | ".join(header_titles) + " |\n"
            table_header += "| " + " | ".join(["---"] * min(columns_per_row, num_cars)) + " |\n"

            # 이미지 행 및 텍스트 행 생성
            img_rows = []
            text_rows = []

            for idx, car_name in enumerate(recom_elec):
                # 차량 이미지 URL 가져오기
                image_url = df.loc[df['최근 구매 제품'] == car_name, '모델 사진'].to_numpy()[0]
                img_tag = f'<img src="{image_url}" width="250">' if image_url else "이미지 없음"

                # 차량 정보 정리
                fuel_type = df.loc[df['최근 구매 제품'] == car_name, '연료 구분'].to_numpy()[0]
                price = f"{min_price_list.get(car_name, '가격 정보 없음')}~"
                mileage = df.loc[df['최근 구매 제품'] == car_name, '차량 연비'].to_numpy()[0]
                power = df.loc[df['최근 구매 제품'] == car_name, '최대 출력'].to_numpy()[0]

                # 차량 정보 요약 생성 (HTML <br> 사용)
                summary = f"**{car_name}**<br>연료 구분: {fuel_type}<br>가격: {price}<br>연비: {mileage}<br>최대 출력: {power}"

                # 행 데이터를 리스트에 추가
                img_rows.append(img_tag)
                text_rows.append(summary)

                # 줄바꿈 처리 (3개씩 한 줄)
                if (idx + 1) % columns_per_row == 0 or idx == num_cars - 1:
                    img_row = "| " + " | ".join(img_rows) + " |\n"
                    text_row = "| " + " | ".join(text_rows) + " |\n"
                    table_header += img_row + text_row  # 테이블에 추가
                    img_rows, text_rows = [], []  # 리스트 초기화

            # Markdown을 사용하여 테이블 출력 (HTML 허용)
            st.markdown(table_header, unsafe_allow_html=True)

        