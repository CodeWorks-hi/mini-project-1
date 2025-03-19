import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
import requests
import base64

st.set_page_config(page_title="현대자동차 관리자 페이지", layout="wide")

# ✅ 파일 경로 확인 및 데이터 불러오기
file_path = "data/차량정보.csv"
df = pd.read_csv(file_path)

# ✅ 전기차 보조금 데이터
ev_subsidies = {
    "서울특별시": 9000000, "부산광역시": 10500000, "대구광역시": 11000000,
    "인천광역시": 10600000, "광주광역시": 11000000, "대전광역시": 12000000,
    "울산광역시": 10500000, "경기도 수원시": 10500000, "경기도 성남시": 11000000,
    "충청북도 청주시": 14000000, "충청남도 천안시": 14000000, "전라북도 전주시": 15000000,
    "전라남도 목포시": 15500000, "경상북도 포항시": 13000000, "경상남도 창원시": 13000000
}

# ✅ 다자녀 혜택 (적용 가능한 차량)
multi_child_cars = ["Palisade (LX2)", "Santa-Fe (MX5 PHEV)", "Tucson (NX4 PHEV)"]

# ✅ 재구매 할인 데이터
rebuy_discounts = {
    "G80 (RG3)": 2000000, "GV80 (RS4)": 3000000,
    "Palisade (LX2)": 1500000, "스타리아": 1500000
}

# ✅ 법인 혜택
corporate_benefits = """
✅ 부가세 환급 및 감가상각 적용 가능  
✅ 법인 차량 단체 보험료 할인 제공  
✅ 운용 리스를 통한 유지비 절감 및 관리 편의성 제공  
"""

# ✅ PDF 생성 함수 (표 형식의 양식 적용 – FPDF 사용)
def generate_pdf(selected_model, final_price, benefits, car_image_url, promotion_info, installment_info):
    pdf = FPDF()
    pdf.add_page()
    
    # ---------- 유니코드 폰트 설정 ----------
    # fonts 디렉토리 안에 NanumGothic.ttf가 있다고 가정
    font_path = "fonts/NanumGothic.ttf"
    if not os.path.exists(font_path):
        st.error("NanumGothic.ttf 폰트 파일이 존재하지 않습니다. 'fonts' 폴더 내에 폰트 파일을 확인하세요.")
        return None
    # 일반체와 볼드체 모두 등록
    pdf.add_font("NanumGothic", "", font_path, uni=True)
    pdf.add_font("NanumGothic", "B", font_path, uni=True)
    pdf.set_font("NanumGothic", "B", 16)
    # ----------------------------------------
    
    # 제목 (중앙 정렬)
    pdf.cell(0, 10, "차량 구매 혜택 보고서", ln=True, align="C")
    pdf.ln(5)
    
    # [1] 프로모션 조회 (개인 고객) 섹션
    pdf.set_font("NanumGothic", "B", 14)
    pdf.cell(0, 10, "1. 프로모션 조회 (개인 고객)", ln=True)
    pdf.ln(3)
    
    # --- 차량 정보 테이블 ---
    pdf.set_font("NanumGothic", "B", 12)
    pdf.cell(80, 10, "항목", border=1, align="C")
    pdf.cell(0, 10, "내용", border=1, ln=True, align="C")
    
    pdf.set_font("NanumGothic", "", 12)
    pdf.cell(80, 10, "선택 차량", border=1, align="C")
    pdf.cell(0, 10, "   " + selected_model, border=1, ln=True)
    
    pdf.cell(80, 10, "최종 적용 가격", border=1,align="C")
    pdf.cell(0, 10,  "   " + f"{final_price:,.0f} 원", border=1, ln=True)
    pdf.ln(5)
    
    # --- 적용 혜택 테이블 ---
    pdf.set_font("NanumGothic", "B", 12)
    pdf.cell(80, 10, "혜택 항목", border=1, align="C")
    pdf.cell(0, 10, "내용", border=1, ln=True, align="C")
    
    pdf.set_font("NanumGothic", "", 12)
    if benefits:
        for benefit in benefits:
            pdf.cell(80, 10, benefit, border=1, align="C" )
            pdf.cell(0, 10,  "   " + "적용됨", border=1, ln=True)
    else:
        pdf.cell(80, 10, "없음", border=1)
        pdf.cell(0, 10,  "   " + "-", border=1, ln=True)
    pdf.ln(5)
    
    # --- 추가 프로모션 정보 ---
    pdf.set_font("NanumGothic", "", 12)
    pdf.multi_cell(0, 10, "추가 정보: " + promotion_info, border=1)
    pdf.ln(10)
    
    # [2] 할부/리스 계산 및 혜택 비교 섹션
    pdf.set_font("NanumGothic", "B", 14)
    pdf.cell(0, 10, "2. 할부/리스 계산 및 혜택 비교", ln=True)
    pdf.ln(3)
    
    # --- 할부 정보 테이블 ---
    pdf.set_font("NanumGothic", "B", 12)
    pdf.cell(80, 10, "항목", border=1, align="C")
    pdf.cell(0, 10, "내용", border=1, ln=True, align="C")
    
    pdf.set_font("NanumGothic", "", 12)
    for line in installment_info.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            pdf.cell(80, 10, key.strip(), border=1, align="C" )
            pdf.cell(0, 10, value.strip(), border=1, ln=True, align="C" )
        else:
            pdf.cell(80, 10, line.strip(), border=1, align="C" )
            pdf.cell(0, 10, "", border=1, ln=True, align="C" )
    pdf.ln(5)
    
    # --- 차량 이미지 삽입 (이미지 URL에서 다운로드 후 사용)
    try:
        response = requests.get(car_image_url)
        if response.status_code == 200:
            temp_image_path = "temp_car_image.jpg"
            with open(temp_image_path, "wb") as f:
                f.write(response.content)
            pdf.image(temp_image_path, x=10, w=100)
            os.remove(temp_image_path)
    except Exception as e:
        pass
    
    # PDF 저장 후 경로 리턴
    pdf_file_path = "car_promo_report.pdf"
    pdf.output(pdf_file_path, "F")
    return pdf_file_path

# UI 구성
st.title("현대자동차 관리자 페이지")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["프로모션 조회", "할부 계산 및 혜택 비교", "PDF 다운로드"])

# ✅ 탭 1: 프로모션 조회
with tab1:
    subtab1, subtab2 = st.tabs(["개인 고객", "법인 고객"])
    
    with subtab1:
        col1, col2 = st.columns([1, 1.5])
        with col1:
            is_rebuy = st.checkbox("재구매 고객 여부")
            st.text(f"{', '.join(rebuy_discounts.keys())}")
            
            has_children = st.checkbox("다자녀 혜택 적용")
            st.text(f"{', '.join(multi_child_cars)}")
            
            ev_promo = st.checkbox("전기차 프로모션 적용")
            st.text(f"{', '.join(df[df['연료 구분'].isin(['전기', '플러그인 하이브리드', '수소'])]['최근 구매 제품'].unique())}")
            customer_name = st.text_input("고객 이름")
            
            # 차량 선택 리스트 필터링
            filtered_cars = df["최근 구매 제품"].unique()  # 기본값: 모든 차량
            if has_children:
                filtered_cars = [car for car in multi_child_cars if car in filtered_cars]
            if is_rebuy:
                filtered_cars = [car for car in rebuy_discounts.keys() if car in filtered_cars]
            if ev_promo:
                filtered_cars = df[df["연료 구분"].isin(["전기", "플러그인 하이브리드", "수소"])]["최근 구매 제품"].unique()
            
            # 차량 선택 (Tab1)
            selected_model = st.selectbox("차량 모델 선택", filtered_cars, key="selected_model_tab1")
            region = st.selectbox("거주 지역 선택", list(ev_subsidies.keys()))
        
        with col2:
            st.subheader("개인 고객 혜택 상세")
            selected_car_info = df[df["최근 구매 제품"] == selected_model].iloc[0]
            car_price = selected_car_info["최근 거래 금액"]
            fuel_type = selected_car_info["연료 구분"]
            car_image_url = selected_car_info["모델 사진"]  # 차량 이미지 URL
            final_price = car_price  # 초기 가격
            
            # 다자녀 혜택 적용
            if has_children and selected_model in multi_child_cars:
                st.write("- **다자녀 가구 혜택 적용:** 무이자 할부 제공, 뒷좌석 모니터 30% 할인")
                final_price -= 1000000
            
            # 전기차 혜택 적용
            ev_subsidy = 0
            if fuel_type in ["전기", "플러그인 하이브리드", "수소"]:
                ev_subsidy = ev_subsidies.get(region, 0)
                st.write(f"- **전기차 보조금:** 최대 {ev_subsidy:,.0f} 원 적용")
                final_price -= ev_subsidy
                st.write("- **충전기 무료 설치 또는 충전 크레딧 50만 원 지급**")
                st.write("- **전기차 보험료 할인 (최대 10%) 적용 가능**")
            
            # 재구매 할인 적용
            discount = rebuy_discounts.get(selected_model, 0)
            if is_rebuy and discount > 0:
                st.write(f"- **재구매 할인:** {discount:,.0f} 원 적용")
                final_price -= discount
            
            st.image(car_image_url, caption=f"{selected_model} 이미지", use_container_width=True)
            st.write(f"**최종 적용 가격:** {final_price:,.0f} 원")
    
    with subtab2:
        col3, col4 = st.columns([1, 1.5])
        with col3:
            st.subheader("법인 고객 입력 사항")
            corporate_type = st.selectbox("법인 유형 선택", ["일반 법인", "개인 사업자", "관공서 / 공공기관"])
            operation_type = st.radio("운용 방식 선택", ["일시불 구매", "운용 리스", "금융 리스", "장기 렌트"])
            purchase_purpose = st.selectbox("차량 구매 목적", 
                                            ["직원 출퇴근용", "임원용", "업무용 (택배, 물류, 배달)", "대중교통 / 셔틀버스", "친환경 법인 차량"])
            vat_deduction = st.checkbox("부가세 환급 적용 가능")
            group_insurance = st.checkbox("법인 차량 단체 보험료 할인 적용")
            maintenance_package = st.checkbox("차량 유지보수 패키지 포함")
            lease_discount = st.checkbox("리스 / 렌트 특가 프로모션 적용")
            bulk_discount = st.checkbox("대량 구매 (3대 이상) 추가 할인")
            
            corporate_car_list = df["최근 구매 제품"].unique()
            if purchase_purpose == "친환경 법인 차량":
                corporate_car_list = df[df["연료 구분"].isin(["전기", "플러그인 하이브리드", "수소"])]["최근 구매 제품"].unique()
            elif purchase_purpose == "업무용 (택배, 물류, 배달)":
                corporate_car_list = df[df["차량 유형"].isin(["SUV", "밴", "픽업트럭"])]["최근 구매 제품"].unique()
            selected_corporate_car = st.selectbox("구매할 차량 선택", corporate_car_list)
        
        with col4:
            st.subheader("법인 고객 혜택 상세")
            selected_car_info = df[df["최근 구매 제품"] == selected_corporate_car].iloc[0]
            car_price = selected_car_info["최근 거래 금액"]
            fuel_type = selected_car_info["연료 구분"]
            car_image_url = selected_car_info["모델 사진"]
            final_price_corp = car_price  # 법인 고객의 최종 가격 (개별 계산 가능)
            
            st.markdown(f"**선택한 차량:** {selected_corporate_car}")
            st.image(car_image_url, caption=f"{selected_corporate_car} 이미지", use_container_width=True)
            st.markdown("✅ **선택한 법인 유형:**")
            st.markdown(f"- {corporate_type}")
            st.markdown("✅ **운용 방식:**")
            st.markdown(f"- {operation_type}")
            st.markdown("✅ **차량 구매 목적:**")
            st.markdown(f"- {purchase_purpose}")
            st.markdown("✅ **적용 가능한 법인 혜택:**")
            if vat_deduction:
                st.markdown("- 부가세 환급 및 감가상각 적용 가능")
            if group_insurance:
                st.markdown("- 법인 차량 단체 보험료 할인 제공")
            if maintenance_package:
                st.markdown("- 차량 유지보수 패키지 포함 가능")
            if lease_discount:
                st.markdown("- 운용 리스 / 장기 렌트 특가 프로모션 적용 가능")
            if bulk_discount:
                st.markdown("- 3대 이상 구매 시 추가 할인 제공")
            st.subheader("🏢 추가 법인 프로모션")
            st.markdown("- 대량 구매 시 맞춤형 혜택 제공")
            st.markdown("- 법인 전용 금융 프로그램 적용 가능")
            st.markdown("- 친환경 차량 구매 시 추가 세제 혜택 가능")

# ✅ 탭 2: 할부 계산 및 리스 혜택 비교
with tab2:
    subtab1, subtab2 = st.tabs(["할부 계산", "리스 혜택 비교"])
    
    # 할부 계산 탭
    with subtab1:
        st.write("#### 할부 계산기")
        col1, col2 = st.columns([1, 1.5])
        with col1:
            # 전체 차량 목록
            all_cars = df["최근 구매 제품"].unique().tolist()
            # Tab1에서 선택한 차량을 세션에서 가져와 기본 인덱스로 사용
            if "selected_model_tab1" in st.session_state and st.session_state["selected_model_tab1"] in all_cars:
                default_index = all_cars.index(st.session_state["selected_model_tab1"])
            else:
                default_index = 0
            selected_model_installment = st.selectbox(
                "차량 모델 선택 (할부 적용 가능)",
                all_cars,
                index=default_index,
                key="selected_model_tab2"
            )
            purchase_price = df[df["최근 구매 제품"] == selected_model_installment]["최근 거래 금액"].values[0]
            loan_term = st.selectbox("할부 기간 선택", [12, 24, 36, 48, 60])
            interest_rate = st.slider("연이자율 (%)", min_value=1.0, max_value=7.0, value=3.5, step=0.1)
            initial_payment = st.number_input(
                "초기 선수금 입력 (원) : 차량가의 10%",
                min_value=0,
                max_value=int(purchase_price),
                value=int(purchase_price * 0.2),
                step=500000
            )
            monthly_payment = (purchase_price - initial_payment) * (1 + (interest_rate / 100) * (loan_term / 12)) / loan_term
        with col2:
            st.write("#### 할부 상세 내역")
            st.markdown(f"**차량 모델:** {selected_model_installment}")
            st.markdown(f"**차량 가격:** {purchase_price:,.0f} 원")
            st.markdown(f"**할부 기간:** {loan_term}개월")
            st.markdown(f"**이자율:** {interest_rate:.1f}%")
            st.markdown(f"**초기 선수금:** {initial_payment:,.0f} 원")
            st.markdown(f"**월 납입 금액:** {monthly_payment:,.0f} 원")
            st.write("#### 할부 시 카드 혜택")
            st.markdown("- 특정 카드 이용 시 최대 **1.5% 캐시백 제공**")
            st.markdown("- 월 30만 원 이상 사용 시 **주유비 / 충전비 할인 (5~10만 원)**")
            st.markdown("- 할부 고객 대상 자동차 보험료 **최대 10% 할인 가능**")
    
    # 리스 혜택 비교 탭
    with subtab2:
        st.write("#### 리스 혜택 비교")
        col3, col4 = st.columns([1, 1.5])
        with col3:
            lease_type = st.radio("리스 유형 선택", ["운용 리스", "금융 리스", "장기 렌트"])
            lease_term = st.selectbox("리스 기간 선택 (개월)", [12, 24, 36, 48, 60])
            selected_lease_model = st.selectbox("차량 모델 선택 (리스 가능)", df["최근 구매 제품"].unique())
            lease_price = df[df["최근 구매 제품"] == selected_lease_model]["최근 거래 금액"].values[0]
            if lease_type == "운용 리스":
                residual_value = int(lease_price * 0.5)
            elif lease_type == "금융 리스":
                residual_value = int(lease_price * 0.3)
            else:
                residual_value = 0
            lease_monthly_payment = (lease_price - residual_value) / lease_term if residual_value else lease_price / lease_term
            st.markdown(f"**선택한 차량:** {selected_lease_model}")
            st.markdown(f"**리스 유형:** {lease_type}")
            st.markdown(f"**리스 기간:** {lease_term}개월")
            st.markdown(f"**차량 가격:** {lease_price:,.0f} 원")
            st.markdown(f"**잔존 가치:** {residual_value:,.0f} 원")
            st.markdown(f"**월 납입 금액:** {lease_monthly_payment:,.0f} 원")
        with col4:
            st.write("#### 리스 고객 혜택")
            if lease_type == "운용 리스":
                st.text("- 차량 유지보수 비용 포함 가능 ✅")
                st.text("- 리스 종료 후 차량 반납 or 교체 가능 ✅")
                st.text("- 부가세 환급 가능 (사업자) ✅")
            elif lease_type == "금융 리스":
                st.text("- 계약 종료 후 차량 완전 소유 가능 ✅")
                st.text("- 차량 감가상각 처리 가능 (법인/사업자) ✅")
                st.text("- 부가세 환급 가능 (일부 조건) ✅")
            else:
                st.text("- 보험료 및 정비비 포함 (렌터카 개념) ✅")
                st.text("- 사고 시 면책금 낮음 (보험 혜택) ✅")
                st.text("- 법인 차량 비용 처리 용이 ✅")
            fuel_type = df[df["최근 구매 제품"] == selected_lease_model]["연료 구분"].values[0]
            if fuel_type in ["전기", "플러그인 하이브리드", "수소"]:
                st.write("#### 전기차 리스 혜택")
                st.markdown("- **월 리스료 5% 할인** 적용 가능 ✅")
                st.markdown("- **충전기 무료 설치 지원** 또는 충전 크레딧 제공 ✅")
                st.markdown("- **전기차 보험료 10% 추가 할인** 가능 ✅")

# ✅ 추가 프로모션 및 최종 할인/가격 정리 (공통 정보)
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("👨‍👩‍👧‍👦 다자녀 혜택")
    if has_children and selected_model in multi_child_cars:
        st.markdown("✅ **다자녀 혜택 적용 가능**")
        st.markdown("- 무이자 할부 제공")
        st.markdown("- 뒷좌석 모니터 30% 할인")
        st.subheader("📌 추가 혜택 선택 (최대 2개)")
        options = [
            "프리미엄 카시트 1개 무료 증정",
            "차량용 공기청정기 제공",
            "뒷좌석 모니터 50% 할인",
            "가족 차량 정기 점검 1년 무료"
        ]
        selected_benefits = st.multiselect("추가 혜택 선택", options, max_selections=2)
        if selected_benefits:
            st.markdown("**선택한 추가 혜택:**")
            for benefit in selected_benefits:
                st.markdown(f"- {benefit}")
    else:
        st.markdown("❌ 다자녀 혜택 적용 대상이 아닙니다.")
with col2:
    st.subheader("⚡ 전기차 혜택")
    ev_subsidy = 0
    if fuel_type in ["전기", "플러그인 하이브리드", "수소"]:
        ev_subsidy = ev_subsidies.get(region, 0)
        st.markdown("✅ **전기차 보조금 적용 가능**")
        st.markdown(f"- 거주 지역 ({region}) 기준 최대 **{ev_subsidy:,.0f} 원** 지원")
        st.markdown("- 충전기 설치 지원 가능")
    else:
        st.markdown("❌ 전기차 혜택 대상이 아닙니다.")
with col3:
    st.subheader("🏢 법인 차량 혜택")
    st.markdown("✅ **법인 고객을 위한 특별 혜택**")
    st.markdown("- 부가세 환급 및 감가상각 적용 가능")
    st.markdown("- 법인 차량 단체 보험료 할인 제공")
    st.markdown("- 운용 리스를 통한 유지비 절감 및 관리 편의성 제공")


# ✅ 탭 3: PDF 다운로드
with tab3:
    st.subheader("📄 구매 보고서 PDF 다운로드")
    # PDF 생성 버튼 클릭 시, Tab1과 Tab2에서 선택한 정보를 정리하여 PDF에 반영
    if st.button("PDF 생성"):
        # Tab1(프로모션) 관련 정보 정리
        promotion_info = (
            f"재구매 여부: {'예' if is_rebuy else '아니오'}\n"
            f"다자녀 혜택: {'적용' if has_children and selected_model in multi_child_cars else '미적용'}\n"
            f"전기차 보조금: {ev_subsidy:,.0f} 원"
        )
        # Tab2(할부 계산) 관련 정보 정리
        installment_info = (
            f"할부 기간: {loan_term}개월\n"
            f"연이자율: {interest_rate:.1f}%\n"
            f"초기 선수금: {initial_payment:,.0f} 원\n"
            f"월 납입 금액: {monthly_payment:,.0f} 원"
        )
        pdf_file = generate_pdf(selected_model, final_price, ["전기차 보조금", "다자녀 혜택"], car_image_url, promotion_info, installment_info)
        if pdf_file:
            with open(pdf_file, "rb") as pdf:
                st.download_button(label="PDF 다운로드", data=pdf, file_name="car_report.pdf", mime="application/pdf")