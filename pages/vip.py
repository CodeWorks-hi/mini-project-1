import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta

# VIP 고객 맞춤 프로모션 타이틀
st.title(" VIP 고객 맞춤 프로모션 & 프라이빗 스케줄")
st.write("VIP 고객을 대상으로 맞춤형 할인 혜택과 프라이빗 이벤트를 제공합니다.")

#  VIP 고객의 누적 구매 금액 입력
purchase_amount = st.number_input("🔢 누적 구매 금액 입력 (단위: 만 원)", min_value=0, step=100, value=5000)

#  VIP 등급 결정 및 맞춤 혜택 제공
if purchase_amount >= 30000:
    grade = "💎 Prestige VIP"
    discount = 12
    extra_benefits = "✨ 최고급 리무진 서비스 + 프라이빗 럭셔리 요트 디너 + 최고급 골프장 초청"
elif purchase_amount >= 20000:
    grade = "🏆 Royal VIP"
    discount = 10
    extra_benefits = "💎 VIP 전용 라운지 + 프리미엄 가죽 시트 업그레이드 + 개인 맞춤 컨시어지 서비스"
elif purchase_amount >= 10000:
    grade = "🌟 Exclusive VIP"
    discount = 7
    extra_benefits = "🎖️ VIP 전용 이벤트 초대 + 맞춤형 차량 시승 + 우선 예약 혜택"
elif purchase_amount >= 5000:
    grade = "🔹 Premium Member"
    discount = 5
    extra_benefits = " VIP 전용 차량 보관 서비스 + 무료 정기 차량 점검"
else:
    grade = "💼 일반 고객"
    discount = 0
    extra_benefits = "❌ 추가 혜택 없음"

if purchase_amount >= 10000:
    format_purchase = format(purchase_amount, ",")
    purchase_1 = format_purchase[:-5] + "억 "
    purchase_2 = format_purchase[-5:] + "만 "
    if purchase_2.startswith("0"):
        if purchase_2 == "0,000만 ":
            format_purchase = purchase_1
        else:
            format_purchase = purchase_1 + purchase_2.lstrip("0,").lstrip("0")
    else:
        format_purchase = purchase_1 + purchase_2

else:
    format_purchase = format(purchase_amount, ",")

# 프로모션 적용 결과 출력
st.markdown("---")
st.subheader(" VIP 고객 맞춤 프로모션 적용 결과")
st.write(f"**누적 구매 금액:** {format_purchase}원")
st.write(f"**고객 등급:** {grade}")
st.write(f"**적용 할인율:** {discount}%")
st.write(f"**추가 제공 혜택:** {extra_benefits}")

#  할인 적용 후 예상 결제 금액 계산
if discount > 0:
    final_price = purchase_amount * (1 - discount / 100)
    if final_price >= 10000:
        format_final = format(final_price, ",")
        final_1 = format_final[:-7] + "억 "
        final_2 = format_final[-7:-2] + "만 "
        if final_2.startswith("0"):
            if final_2 == "0,000만 ":
                format_final = final_1
            else:
                format_final = final_1 + final_2.lstrip("0,").lstrip("0")
        else:
            format_final = final_1 + final_2
        
    st.write(f"**💰 할인 적용 후 예상 결제 금액:** {format_final}원")
else:
    st.write("❌ 할인이 적용되지 않습니다.")

st.markdown("---")
st.markdown("### 🎉 **VIP 이상 고객만을 위한 맞춤형 컨시어지 서비스!** 😊")

# VIP 프로모션 옵션 선택
promotion = st.radio(" 원하는 VIP 프로모션을 선택하세요.", 
                     [" 프라이빗 차량 체험 패키지 ", 
                      " 차고지 예약 & 맞춤형 차량 보관 서비스 ",
                      " 익스클루시브 이벤트 & 개인 맞춤형 혜택 ",
                      " 커넥티드 라이프스타일 멤버십 "])

#  1️⃣ VIP 전용 ‘프라이빗 차량 체험 패키지’
if promotion == " 프라이빗 차량 체험 패키지 ":
    st.subheader(" 프라이빗 차량 체험 패키지 ")
    st.write("""
    **VIP 고객 전용 ‘프라이빗 테스트 드라이브’ 제공**
    - 특정 하이엔드 모델(제네시스, BMW, 벤츠, 포르쉐 등) 대상으로 진행  
    - VIP 고객이 관심 있는 차량을 **7일간 무료 체험 후 구매 결정 가능**  
    - 체험 후 구매할 경우 **최대 5% 추가 할인 혜택 제공**  
    """)

#  2️⃣ VIP 전용 ‘차고지 예약 & 맞춤형 차량 보관 서비스’
elif promotion == " 차고지 예약 & 맞춤형 차량 보관 서비스 ":
    st.subheader(" 차고지 예약 & 맞춤형 차량 보관 서비스 ")
    st.write("""
    **VIP 고객 전용 차량 보관 & 즉시 출고 서비스**
    - VIP 고객이 **자주 사용하는 차량을 사전 예약 후 차고지에 보관**  
    - 필요할 때 **즉시 차량을 출고할 수 있도록 대기 상태 유지**  
     **장기 보관 후 구매 시 추가 혜택**
    - VIP 고객이 장기 보관 후 차량을 구매할 경우 **보관료 20 ~ 40% 차감 혜택 제공**  
    - 차량 보관료 : 고급차 (Luxury/스포츠카) 80만 ~ 150만원, 슈퍼카 (Supercar) 150만 ~ 300만원  
    """)

#  3️⃣ ‘VIP 익스클루시브 이벤트 & 개인 맞춤형 혜택’
elif promotion == " 익스클루시브 이벤트 & 개인 맞춤형 혜택 ":
    st.subheader(" 익스클루시브 이벤트 & 개인 맞춤형 혜택 ")
    st.write("""
    **VIP 고객 초청 ‘프라이빗 브랜드 이벤트’**
    - 고급 레스토랑에서 진행하는 **VIP 초청 시승회 & 네트워킹 디너**  
    - 유명 레이서와 함께하는 **서킷 체험 이벤트** 진행  
    """)

#  4️⃣ VIP ‘커넥티드 라이프스타일 멤버십’
elif promotion == " 커넥티드 라이프스타일 멤버십 ":
    st.subheader(" 커넥티드 라이프스타일 멤버십 ")
    st.write("""
    **VIP 전용 컨시어지 서비스 운영**
    - 차량 정비, 세차, 보험, 유지보수를 전담하는 **프리미엄 컨시어지 서비스** 제공  
    **VIP 고객 전용 글로벌 렌터카 & 모빌리티 서비스 연계**
    - 해외 출장 시, VIP 고객에게 **프리미엄 렌터카 서비스 무료 제공**  
    """)

st.markdown("---")
st.markdown("### 🎉 **VVIP 이상 고객만을 위한 맞춤형 컨시어지 서비스!** 😊")

#  고정된 6개월 VIP 이벤트 일정 생성
vip_event_data = pd.DataFrame({
    "이벤트 제목": [
        " 프라이빗 럭셔리 드라이브 체험", " VIP 초청 골프 라운딩", " Prestige VIP 요트 디너", 
        " Royal VIP 런치", " Exclusive VIP 시승 & 맞춤 상담", "Prestige VIP 리무진 픽업 서비스",
        " 하이엔드 스포츠카 드라이브", "프리미엄 골프 멤버십 체험", " VIP 요트 선상 파티",
        " 미슐랭 셰프의 다이닝 경험", "VIP 하이브리드 모델 시승", " 글로벌 공항 VIP 리무진 서비스",
        " 클래식카 드라이빙 투어", " 해외 골프 투어 패키지", " 초호화 크루즈 나이트"
    ],
    "일정": [
        "2025-04-05", "2025-04-18", "2025-05-10",
        "2025-05-25", "2025-06-08", "2025-06-22",
        "2025-07-06", "2025-07-20", "2025-08-05",
        "2025-08-22", "2025-09-10", "2025-09-28",
        "2025-10-12", "2025-10-27", "2025-11-15"
    ],
    "장소": [
        "한강 프라이빗 드라이브 코스", "제주 최고급 골프장", "부산 요트 클럽",
        "서울 프라이빗 레스토랑", "전국 주요 대리점", "VIP 고객 지정 장소",
        "서울 드라이빙 클럽", "제주 프리미엄 골프장", "부산 마리나 요트 선착장",
        "미슐랭 3스타 레스토랑", "전국 주요 대리점", "해외 공항 VIP 터미널",
        "서울 클래식카 박물관", "하와이 골프 투어", "지중해 크루즈 선착장"
    ],
    "참여 가능 등급": [
        "Exclusive VIP", "Royal VIP", "Prestige VIP",
        "Royal VIP, Prestige VIP", "Exclusive VIP", "Prestige VIP",
        "Exclusive VIP", "Royal VIP", "Prestige VIP",
        "Royal VIP, Prestige VIP", "Exclusive VIP", "Prestige VIP",
        "Exclusive VIP", "Royal VIP", "Prestige VIP"
    ],
    "예약 가능 여부": [
        "가능", "예약 마감", "가능", "가능", "가능", "예약 마감",
        "가능", "가능", "예약 마감", "가능", "가능", "예약 마감",
        "가능", "가능", "가능"
    ],
    "잔여석": [5, 0, 3, 8, 10, 0, 7, 5, 0, 9, 6, 0, 4, 8, 10]
})

# 월별 분류
vip_event_data["월"] = vip_event_data["일정"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").month)
monthly_events = vip_event_data.groupby("월")

#  월별 이벤트 캘린더 표시
st.markdown("####  VIP 월별 프라이빗 이벤트 스케줄")

#  월 선택 드롭다운
selected_month = st.selectbox(" 월을 선택하세요.", sorted(vip_event_data["월"].unique()))

# 선택한 월의 이벤트만 필터링
filtered_events = vip_event_data[vip_event_data["월"] == selected_month]

#  캘린더 형식으로 이벤트 정렬
st.markdown(f"###  {calendar.month_name[selected_month]} VIP 이벤트 일정")

#  보기 편한 이벤트 테이블 정리
styled_df = filtered_events[["이벤트 제목", "일정", "장소", "참여 가능 등급", "예약 가능 여부", "잔여석"]].copy()


styled_df = styled_df.style.set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#4F81BD'), ('color', 'white'), ('font-weight', 'bold')]},
    {'selector': 'tbody td', 'props': [('text-align', 'center')]},
    {'selector': 'th', 'props': [('text-align', 'center')]},
]).format({'잔여석': "{:,.0f}석"})  # 잔여석 숫자 서식 적용

# 📋 보기 편한 테이블 출력
st.table(styled_df)
#  선택한 이벤트 상세 정보 표시
st.markdown("---")
st.subheader(" 현재 진행 중인 이벤트 상세 정보")

#  이벤트 선택
event_selection = st.radio(
    " 자세히 보고 싶은 이벤트를 선택하세요.", 
    filtered_events["이벤트 제목"].tolist(), 
    key="event_selection"
)

# 선택한 이벤트 데이터 가져오기
selected_event = filtered_events[filtered_events["이벤트 제목"] == event_selection].iloc[0]

#  상세 설명 추가
st.markdown("---")
st.subheader(f"🎟️ {selected_event['이벤트 제목']} 상세 정보")

# 일정 및 기본 정보
st.write(f" **일정:** {selected_event['일정']}")
st.write(f" **장소:** {selected_event['장소']}")
st.write(f" **참여 가능 등급:** {selected_event['참여 가능 등급']}")
st.write(f" **예약 가능 여부:** {selected_event['예약 가능 여부']}")
st.write(f" **잔여석:** {selected_event['잔여석']}석")

#  프라이빗 럭셔리 드라이브 체험
if event_selection == " 프라이빗 럭셔리 드라이브 체험":
    st.write("""
    ✨ **프라이빗 럭셔리 드라이브 체험**
    
    -  **페라리, 람보르기니, 벤틀리 등 최고급 스포츠카 시승**
    -  **서울 한강 및 한적한 교외 드라이브 코스 포함**
    -  **전문 포토그래퍼가 촬영하는 럭셔리 드라이빙 기념사진 제공**
    -  **시승 후 프라이빗 레스토랑에서 고급 다이닝**
    -  **VIP 한정 기념품 제공 (럭셔리 키체인 & 프리미엄 시승권)**
    """)

#  VIP 초청 골프 라운딩
elif event_selection == " VIP 초청 골프 라운딩":
    st.write("""
     **VIP 초청 골프 라운딩**
    
    -  **제주도 최고급 골프 리조트에서 진행**
    -  **프라이빗 라운지에서 샴페인 리셉션**
    -  **세계적인 프로 골퍼와 함께하는 원포인트 레슨**
    -  **VIP 골프 굿즈 제공 (맞춤형 골프볼 & 고급 캐디백)**
    -  **라운딩 후 고급 프렌치 다이닝에서 VIP 디너**
    """)

#  Prestige VIP 요트 디너
elif event_selection == " Prestige VIP 요트 디너":
    st.write("""
     **Prestige VIP 요트 디너**
    
    -  **부산 요트 클럽에서 3시간 프라이빗 요트 투어**
    -  **미슐랭 셰프가 준비하는 최고급 디너 제공**
    -  **재즈 라이브 공연 & 샴페인 파티**
    -  **프라이빗 바에서 프리미엄 칵테일 서비스**
    -  **전문 포토그래퍼의 스냅 촬영 & 인스타그램 기념사진**
    """)

#  Royal VIP 런치
elif event_selection == " Royal VIP 런치":
    st.write("""
     **Royal VIP 런치**
    
    -  **서울 최고의 미슐랭 3스타 레스토랑에서 진행**
    -  **최고급 와인 & 맞춤형 코스 요리 제공**
    -  **클래식 연주와 함께하는 럭셔리 점심**
    -  **참석 고객에게 프리미엄 기프트 박스 제공**
    """)

#  Exclusive VIP 시승 & 맞춤 상담
elif event_selection == " Exclusive VIP 시승 & 맞춤 상담":
    st.write("""
     **Exclusive VIP 시승 & 맞춤 상담**
    
    -  **벤츠, 포르쉐, 테슬라 최신 모델 시승 기회 제공**
    -  **전국 주요 대리점에서 맞춤형 차량 상담**
    -  **VIP 고객만을 위한 특별 금융 혜택 안내**
    -  **시승 고객 한정, 프리미엄 차량 케어 패키지 증정**
    """)

#  Prestige VIP 리무진 픽업 서비스
elif event_selection == " Prestige VIP 리무진 픽업 서비스":
    st.write("""
     **Prestige VIP 리무진 픽업 서비스**
    
    -  **롤스로이스, 벤츠 마이바흐 전용 리무진 서비스 제공**
    -  **VIP 고객이 원하는 장소에서 맞춤형 픽업**
    -  **차량 내 프리미엄 음료 & 고급 간식 제공**
    -  **예약 고객에게 고급 브랜드 기념품 제공**
    """)

# 예약 버튼 (예약 가능 시 활성화)
if selected_event["예약 가능 여부"] == "가능" and selected_event["잔여석"] > 0:
    if st.button("✅ 예약하기", key="reservation_button"):
        st.success(f"✅ {selected_event['이벤트 제목']} 예약이 완료되었습니다! 🎉")
else:
    st.warning("❌ 해당 이벤트는 예약이 마감되었습니다.")

st.markdown("---")
st.write(" **VIP 고객만을 위한 차별화된 프리미엄 혜택을 제공합니다!** 🎖️")
