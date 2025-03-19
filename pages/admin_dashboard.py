import streamlit as st

st.set_page_config(page_title="현대자동차 관리자 페이지", layout="wide")

# ✅ 1️⃣ "현대자동차 관리자 페이지" 헤더
st.title("현대자동차 관리자 페이지")
st.markdown("---")

# ✅ 2️⃣ 상단 탭 구성 (프로모션 조회, 할부 계산, PDF, 고객 화면 전송)
tab1, tab2, tab3, tab4 = st.tabs(["프로모션 조회", "할부 계산 및 혜택 비교", "PDF 다운로드", "고객 화면 전송"])

# ✅ 3️⃣ 프로모션 조회 (탭 1)
with tab1:
    # 🔹 서브탭 구성 (개인 고객 vs 법인 고객)
    subtab1, subtab2 = st.tabs(["개인 고객", "법인 고객"])

    with subtab1:
        col1, col2 = st.columns([1, 1.5])

        with col1:
            customer_name = st.text_input("고객 이름")
            selected_model = st.selectbox("차량 모델 선택", [
                "Avante (CN7 N)", "Avante (CN7 HEV)", "Grandeur (GN7 HEV)",
                "G80 (RG3)", "Santa-Fe ™", "Santa-Fe (MX5 PHEV)", "Tucson (NX4 PHEV)",
                "Palisade (LX2)", "IONIQ (AE EV)", "IONIQ 6 (CE)", "NEXO (FE)",
                "G90 (HI)", "G70 (IK)", "i30 (PD)", "GV80 (RS4)", "G90 (RS4)"
            ])
            region = st.selectbox("거주 지역 선택", [
                "서울특별시", "부산광역시", "대구광역시", "인천광역시",
                "광주광역시", "대전광역시", "울산광역시", "경기도 수원시",
                "경기도 성남시", "충청북도 청주시", "충청남도 천안시",
                "전라북도 전주시", "전라남도 목포시", "경상북도 포항시", "경상남도 창원시"
            ])
            is_rebuy = st.checkbox("재구매 고객 여부")
            has_children = st.checkbox("다자녀 혜택 적용 (미성년자 3명 이상)")

        with col2:
            st.subheader("개인 고객 혜택 상세")
            final_price = 41430000  # 예시 기본 가격 (차량 선택 시 변경)

            if has_children:
                st.write("- **다자녀 가구 혜택 적용:** 무이자 할부 제공, 뒷좌석 모니터 30% 할인")
                final_price -= 1000000  # 다자녀 혜택 추가 감면

            if "IONIQ" in selected_model or "NEXO" in selected_model:
                ev_subsidy = {
                    "서울특별시": 9000000, "부산광역시": 10500000, "대구광역시": 11000000,
                    "인천광역시": 10600000, "광주광역시": 11000000, "대전광역시": 12000000,
                    "울산광역시": 10500000, "경기도 수원시": 10500000, "경기도 성남시": 11000000,
                    "충청북도 청주시": 14000000, "충청남도 천안시": 14000000, "전라북도 전주시": 15000000,
                    "전라남도 목포시": 15500000, "경상북도 포항시": 13000000, "경상남도 창원시": 13000000
                }.get(region, 0)
                st.write(f"- **전기차 보조금:** 최대 {ev_subsidy:,.0f} 원 적용")
                final_price -= ev_subsidy  # 전기차 보조금 적용

            if is_rebuy:
                discount = {
                    "G80 (RG3)": 2000000, "GV80 (RS4)": 3000000,
                    "Palisade (LX2)": 1500000, "스타리아": 1500000
                }.get(selected_model, 0)
                if discount > 0:
                    st.write(f"- **재구매 할인:** {discount:,.0f} 원 적용")
                    final_price -= discount
                else:
                    st.write("- **재구매 할인:** 해당 차종은 추가 할인이 없습니다.")

            st.write(f"**최종 적용 가격:** {final_price:,.0f} 원")

    with subtab2:
        col3, col4 = st.columns([1, 1.5])

        with col3:
            st.write("법인 고객 관련 입력란 (필요 시 추가 가능)")

        with col4:
            st.subheader("법인 고객 혜택")
            st.write("""
            ✅ 부가세 환급 및 감가상각 적용 가능  
            ✅ 법인 차량 단체 보험료 할인 제공  
            ✅ 운용 리스를 통한 유지비 절감 및 관리 편의성 제공  
            """)

    st.markdown("---")

    # ✅ 사용자가 선택한 항목 정리
    st.subheader("📌 선택한 항목 정리")
    st.markdown(f"**차량:** {selected_model}")
    st.markdown(f"**최종 적용 가격:** {final_price:,.0f} 원")
    if has_children:
        st.markdown(f"**다자녀 혜택 적용:** ✅")

    if "IONIQ" in selected_model or "NEXO" in selected_model:
        st.markdown(f"**전기차 보조금:** {ev_subsidy:,.0f} 원 적용")

    if is_rebuy:
        st.markdown(f"**재구매 할인:** {discount:,.0f} 원 적용")

    # ✅ 다자녀 혜택 추가 선택 (4가지 중 2가지 선택 가능)
    if has_children:
        st.subheader("📌 다자녀 추가 혜택 선택 (2가지 선택 가능)")
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

