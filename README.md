# 맞춤형 차량 추천 및 프로모션 플랫폼

## 🧭 개요
본 프로젝트는 고객 데이터를 기반으로 **AI 차량 추천 시스템** 및 **프로모션 관리 플랫폼**을 구축하는 것을 목표로 하였습니다.  
고객의 구매 성향, 지역, 예산 등 다양한 특성을 분석하고, 이를 기반으로 최적의 차량을 추천하며, 실시간 프로모션 정보를 제공하는 대시보드를 Streamlit 기반으로 구현하였습니다.

---

## 🚀 주요 기능

### 🔍 AI 기반 차량 추천 시스템
- 사용자의 입력 정보(예산, 지역, 차량 유형 등)를 기반으로 머신러닝 모델을 통해 차량 추천
- 연료 유형별로 세분화된 모델 구성 (가솔린, 디젤, 전기)

### 🧠 고객 세분화 및 클러스터링
- 고객 충성도, 구매 이력 등을 기반으로 6가지 클러스터 도출
- 각 클러스터에 맞는 마케팅 전략 도출

### 📊 시각화 대시보드
- 연령대, 지역별 고객 분포 및 차량 선호도 시각화
- 연료 유형별 판매 추세 및 고객 가치 기반 인사이트 제공

### 🎯 프로모션 매칭 및 혜택 추천
- 할부 계산기 등 추가 서비스 연동
- 카드사 제휴 혜택 분석 및 구매 유도 전략 제공

### 🔐 보안 및 자동 배포
- `.secrets.toml`을 활용한 API 키 안전 보관
- GitHub Actions를 이용한 CI/CD 및 Streamlit Cloud 자동 배포

---

## 🛠 사용 기술

| 분야 | 기술 스택 |
|------|------------|
| Frontend | Streamlit (PWA 지원) |
| Backend/ML | Python, Scikit-learn, LightGBM, Pandas, NumPy |
| 시각화 | Matplotlib, Seaborn |
| 배포 및 관리 | GitHub Actions, Streamlit Cloud |
| 기타 | Openpyxl, dotenv, matplotlib.font_manager (운영체제별 한글 폰트 설정) |

---

## 💻 설치 및 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📈 프로젝트 결과

- **차량 추천 정확도**: 85% ~ 95%
- **최적 모델 선정**: `Decision Tree`, `Random Forest`, `Gradient Boosting`, `LightGBM`
- **연령대별 맞춤 전략 제안**: 20대 / 30대 / 40대 / 50대 / 60대 이상
- **주요 지역별 맞춤 전략 제안**: 서울 / 울산 / 수원 / 성남 / 천안
- **고객 등급별 맞춤 전략 제안**: 신규 / 일반 / VIP

---

## 🏁 기대 효과

- 맞춤형 차량 추천 & 프로모션 제공
- 직관적인 UI/UX 설계로 누구나 쉽게 사용 가능
- 고객과 영업사원 모두의 편의성 향상 및 매출 증대 기여

---

## 📽️ 시연 영상 및 문서

- 🔗 [Streamlit 앱](https://hyundai-crm-analysis-codeworks.streamlit.app/)
- 🎥 [시연 영상 (Google Drive)](https://docs.google.com/file/d/1hor22304b4WGEhOolFn4Hxg05QbQcAMw/preview)
