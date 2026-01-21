import streamlit as st

# ---------------------------------------------------------
# [디자인 설정 영역]
# ---------------------------------------------------------
STYLE_CONFIG = {
 "corner_radius": "25px",
 "border_width": "2px",
 "border_color": "#10b981",
 "fg_color": "#FFFFFF",
 "text_color": "#1f2937",
 "primary_color": "#10b981",
 "bg_color": "#f0fdf4"
}

# 페이지 설정
st.set_page_config(page_title="건강 정보 분석 서비스", layout="centered")

# 세션 상태 초기화 (오류 방지를 위해 필수 데이터를 미리 선언)
if 'step' not in st.session_state:
 st.session_state.step = 1
if 'user_data' not in st.session_state:
 st.session_state.user_data = {
  "name": "",
  "gender": "남성",
  "age": 70,
  "height": 160,
  "weight": 60,
  "diseases": []
 }

# CSS 주입
st.markdown(f"""
 <style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
  .stApp {{ background-color: {STYLE_CONFIG['bg_color']}; font-family: 'Noto Sans KR', sans-serif; }}
  div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"]) {{
   background-color: {STYLE_CONFIG['fg_color']};
   border-radius: {STYLE_CONFIG['corner_radius']};
   border: {STYLE_CONFIG['border_width']} solid {STYLE_CONFIG['border_color']};
   padding: 4rem 3rem;
   box-shadow: 0 20px 40px rgba(0,0,0,0.08);
   margin-top: 2rem;
   position: relative;
  }}
  div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"])::before {{
   content: ""; position: absolute; top: 0; left: 0; right: 0; height: 12px;
   background-color: {STYLE_CONFIG['border_color']};
   border-radius: {STYLE_CONFIG['corner_radius']} {STYLE_CONFIG['corner_radius']} 0 0;
  }}
  div.stButton > button {{
   background-color: {STYLE_CONFIG['primary_color']} !important;
   color: white !important;
   border-radius: 15px !important;
   padding: 0.8rem !important;
   font-weight: 700 !important;
   width: 100% !important;
   border: none !important;
  }}
  /* 요약 박스 스타일 */
  .summary-box {{
   background-color: #f9fafb;
   border-radius: 15px;
   padding: 1.5rem;
   border: 1px dashed #10b981;
   margin: 1.5rem 0;
  }}
 </style>
""", unsafe_allow_html=True)

main_container = st.container()

with main_container:
 # ---------------------------------------------------------
 # STEP 1: 개인정보 수집 및 확인
 # ---------------------------------------------------------
 if st.session_state.step == 1:
  st.markdown('<h1>건강 정보 입력</h1>', unsafe_allow_html=True)

  st.markdown('### 👤 기본 인적 사항', unsafe_allow_html=True)
  col_name, col_gender = st.columns([1.5, 1])
  with col_name:
   name = st.text_input("성함", value=st.session_state.user_data["name"], placeholder="성함을 입력하세요")
  with col_gender:
   gender = st.radio("성별", ["남성", "여성"], index=0 if st.session_state.user_data["gender"] == "남성" else 1, horizontal=True)

  st.markdown('### ⚖️ 신체 정보', unsafe_allow_html=True)
  c1, c2, c3 = st.columns(3)
  with c1:
   age = st.number_input("나이 (세)", value=st.session_state.user_data["age"])
  with c2:
   height = st.number_input("키 (cm)", value=st.session_state.user_data["height"])
  with c3:
   weight = st.number_input("몸무게 (kg)", value=st.session_state.user_data["weight"])

  st.markdown('### 🏥 보유 질환', unsafe_allow_html=True)
  diseases = st.multiselect("보유 질환을 선택하세요", ["고혈압", "당뇨병", "고지혈증", "관절염", "심장질환", "해당 없음"], default=st.session_state.user_data["diseases"])

  # 데이터 저장
  st.session_state.user_data = {"name": name, "gender": gender, "age": age, "height": height, "weight": weight, "diseases": diseases}

  # 확인 섹션 (요약 보기)
  st.write("---")
  st.markdown(f"""
   <div class="summary-box">
    <p style="margin-bottom:0.5rem;"><b>📋 입력 정보 요약</b></p>
    <span style="font-size: 0.95rem;">
     <b>성함:</b> {name} ({gender}) | <b>나이:</b> {age}세<br>
     <b>신체:</b> {height}cm / {weight}kg<br>
     <b>보유 질환:</b> {', '.join(diseases) if diseases else '없음'}
    </span>
   </div>
  """, unsafe_allow_html=True)
  
  st.markdown('<p style="text-align: center; font-weight: 600;">입력하신 정보가 모두 맞습니까?</p>', unsafe_allow_html=True)
  
  confirm_col1, confirm_col2 = st.columns(2)
  with confirm_col1:
   if st.button("예, 맞습니다"):
    if not name: st.warning("성함을 입력해 주세요.")
    else:
     st.session_state.step = 2
     st.rerun()
  with confirm_col2:
   if st.button("아니오, 수정할게요"):
    st.info("내용을 다시 확인 후 수정해 주세요.")

 # ---------------------------------------------------------
 # STEP 2: 정신건강 설문 조사
 # ---------------------------------------------------------
 elif st.session_state.step == 2:
  # 안전하게 데이터 가져오기
  user_name = st.session_state.user_data["name"]
  
  st.markdown(f"""
   <h1>정신건강 설문 조사</h1>
   <p style="opacity: 0.7;">{user_name} 어르신의 마음 건강 상태를 확인하는 단계입니다.</p>
  """, unsafe_allow_html=True)
  
  st.info("진행 중인 설문: 노인 우울 척도(GDS-K) 단축형")
  
  # 설문 예시 문항
  q1 = st.radio("1. 현재의 생활에 대체로 만족하십니까?", ["예", "아니오"], horizontal=True)
  
  col_prev, col_next = st.columns(2)
  with col_prev:
   if st.button("이전 단계로"):
    st.session_state.step = 1
    st.rerun()
  with col_next:
   if st.button("설문 완료"):
    st.session_state.step = 3
    st.rerun()