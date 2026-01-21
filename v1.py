import streamlit as st

# ---------------------------------------------------------
# [디자인 설정 영역] - 각 항목이 제어하는 부분을 주석으로 달았습니다.
# ---------------------------------------------------------
STYLE_CONFIG = {
 "corner_radius": "25px",   # 카드의 모서리 곡률 (값이 클수록 더 둥글게 보임)
 "border_width": "2px",     # 카드 테두리 선의 두께
 "border_color": "#10b981", # 카드 테두리 및 상단 포인트 바 색상
 "fg_color": "#FFFFFF",      # 카드 내부의 배경색 (정보가 적히는 흰색 부분)
 "text_color": "#1f2937",    # 제목, 라벨, 본문 등 모든 글자의 색상
 "primary_color": "#10b981", # 버튼 배경색 등 시스템의 주요 강조 색상
 "bg_color": "#f0fdf4"       # 카드 바깥쪽, 전체 페이지의 배경색
}

st.set_page_config(page_title="건강 정보 분석 서비스", layout="centered")

# 세션 상태 관리
if 'step' not in st.session_state: st.session_state.step = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'user_data' not in st.session_state:
 st.session_state.user_data = {"name": "", "gender": "남성", "age": 70, "height": 160, "weight": 60, "diseases": []}
if 'phq9_answers' not in st.session_state: st.session_state.phq9_answers = {}

# CSS: 1543 버전의 안정적인 레이아웃 스타일
st.markdown(f"""
 <style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
  
  .stApp {{
   background-color: {STYLE_CONFIG['bg_color']};
   font-family: 'Noto Sans KR', sans-serif;
  }}

  /* 메인 카드 레이아웃 */
  .block-container {{
   background-color: {STYLE_CONFIG['fg_color']} !important;
   border-radius: {STYLE_CONFIG['corner_radius']} !important;
   border: {STYLE_CONFIG['border_width']} solid {STYLE_CONFIG['border_color']} !important;
   padding: 3.5rem 2.5rem !important;
   box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
   margin-top: 80px !important;
   max-width: 700px !important;
  }}

  /* 라디오 버튼 공통 카드 스타일 */
  div[data-testid="stRadio"] label[data-baseweb="radio"] {{
   background-color: #ffffff !important;
   border: 1px solid #e5e7eb !important;
   border-radius: 15px !important;
   padding: 18px 25px !important;
   display: flex !important;
   align-items: center !important;
  }}

  div[data-testid="stRadio"] label[data-selected="true"] {{
   border: 2px solid {STYLE_CONFIG['primary_color']} !important;
   background-color: #f0fdf4 !important;
  }}

  /* 라디오 원형 버튼 제거 */
  div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"]::before {{
   display: none !important;
  }}

  /* 성별 가로 정렬을 위한 설정 */
  div[data-testid="stRadio"] > div {{
   gap: 12px;
  }}

  .summary-box {{
   background-color: #f8fafc;
   border: 1px dashed {STYLE_CONFIG['border_color']};
   border-radius: 15px;
   padding: 1.5rem;
   margin: 2rem 0;
  }}

  .stButton > button {{
   border-radius: 15px !important;
   height: 3.8rem !important;
   font-weight: 700 !important;
  }}
 </style>
""", unsafe_allow_html=True)

PHQ9_QUESTIONS = ["1. 일을 하는 것에 대한 흥미나 재미가 거의 없음", "2. 가라앉은 느낌, 우울감 혹은 절망감", "3. 잠들기 어렵거나 자꾸 깨어남, 혹은 너무 많이 잠", "4. 피곤감, 기력이 저하됨", "5. 식욕 저하 혹은 과식", "6. 내 자신이 나쁜 사람이라는 느낌 혹은 실패자라는 느낌", "7. 신문을 읽거나 TV를 볼 때 집중하기 어려움", "8. 남들이 알아챌 정도로 거동이나 말이 느리거나 혹은 너무 초조함", "9. 차라리 죽는 것이 낫겠다는 생각 혹은 자해 생각"]
OPTIONS = ["전혀 아니다", "여러 날 동안", "일주일 이상", "거의 매일", "모름, 무응답"]

# ---------------------------------------------------------
# STEP 1: 건강 정보 입력
# ---------------------------------------------------------
if st.session_state.step == 1:
 st.markdown('<h1 style="text-align:center;">건강 정보 입력</h1>', unsafe_allow_html=True)
 st.write("---")

 st.markdown('### 👤 기본 인적 사항', unsafe_allow_html=True)
 c1, c2 = st.columns([1, 1])
 with c1:
  name = st.text_input("성함", value=st.session_state.user_data["name"], placeholder="성함을 입력하세요")
 with c2:
  # 성별: horizontal=True로 가로 배치 보존
  gender = st.radio("성별", ["남성", "여성"], index=0 if st.session_state.user_data["gender"] == "남성" else 1, horizontal=True)
 
 st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
 st.markdown('### ⚖️ 신체 정보', unsafe_allow_html=True)
 col_a, col_b, col_c = st.columns(3)
 with col_a: age = st.number_input("나이 (세)", value=st.session_state.user_data["age"])
 with col_b: height = st.number_input("키 (cm)", value=st.session_state.user_data["height"])
 with col_c: weight = st.number_input("몸무게 (kg)", value=st.session_state.user_data["weight"])

 diseases = st.multiselect("🏥 보유 질환 (중복 선택 가능)", ["고혈압", "당뇨병", "고지혈증", "골다공증", "심장질환", "뇌졸중", "해당 없음"], default=st.session_state.user_data["diseases"])

 st.session_state.user_data = {"name": name, "gender": gender, "age": age, "height": height, "weight": weight, "diseases": diseases}

 st.markdown(f"""
  <div class="summary-box">
   <p style="margin:0; font-weight:700; color:{STYLE_CONFIG['primary_color']}; font-size:1.1rem;">📋 입력 정보 요약 확인</p>
   <p style="margin:8px 0 0 0; font-size:1rem; line-height:1.6;">
    성함: <b>{name if name else "___"}</b> 님 ({gender})<br>
    나이: <b>{age}세</b> | 신체: <b>{height}cm / {weight}kg</b>
   </p>
  </div>
 """, unsafe_allow_html=True)
 
 if st.button("분석 시작하기 ➡", type="primary", use_container_width=True):
  if not name: st.error("성함을 입력해 주세요.")
  else: st.session_state.step = 2; st.rerun()

# ---------------------------------------------------------
# STEP 2: 정신건강 설문
# ---------------------------------------------------------
elif st.session_state.step == 2:
 q_idx = st.session_state.q_idx
 st.markdown(f"<h3 style='color:{STYLE_CONFIG['primary_color']}; margin:0;'>Mental Health Survey</h3>", unsafe_allow_html=True)
 st.progress((q_idx + 1) / len(PHQ9_QUESTIONS))
 st.markdown(f"**문항 {q_idx + 1}** / {len(PHQ9_QUESTIONS)}")
 
 st.markdown(f'<p style="font-size:1.5rem; font-weight:800; margin: 2.5rem 0 1.5rem 0; line-height:1.5;">{PHQ9_QUESTIONS[q_idx]}</p>', unsafe_allow_html=True)

 # 설문: horizontal=False로 수직 정렬 유지
 answer = st.radio("답변 선택", OPTIONS, key=f"survey_{q_idx}", label_visibility="collapsed", horizontal=False)
 st.session_state.phq9_answers[f"q{q_idx}"] = answer

 st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)
 b1, b2 = st.columns(2)
 with b1:
  if st.button("⬅ 이전 질문", use_container_width=True):
   if q_idx > 0: st.session_state.q_idx -= 1; st.rerun()
   else: st.session_state.step = 1; st.rerun()
 with b2:
  is_last = (q_idx == len(PHQ9_QUESTIONS) - 1)
  if st.button("다음 질문 ➡" if not is_last else "설문 완료 ➡", type="primary", use_container_width=True):
   if not is_last: st.session_state.q_idx += 1; st.rerun()
   else: st.balloons(); st.session_state.step = 3; st.rerun()