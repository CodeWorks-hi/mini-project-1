import streamlit as st

st.title("📌 고객 정보 입력 & 제품 추천")

# 고객 정보 입력
name = st.text_input("이름을 입력하세요:")
age = st.number_input("나이 입력", min_value=18, max_value=100)
category = st.selectbox("관심 카테고리", ["가전", "의류", "식품", "화장품"])

# 추천 버튼 (나중에 머신러닝 모델 연동 예정)
if st.button("추천 받기"):
    st.success(f"{name}님에게 추천하는 제품을 곧 제공할 예정입니다!")
