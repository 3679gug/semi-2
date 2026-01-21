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
st.set_page_config(page_title="건강 정보 입력", layout="centered")

# [핵심] Streamlit의 기본 컨테이너 자체를 흰색 카드로 변신시키는 CSS
st.markdown(f"""
 <style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
  
  /* 1. 전체 배경 */
  .stApp {{
   background-color: {STYLE_CONFIG['bg_color']};
   font-family: 'Noto Sans KR', sans-serif;
  }}

  /* 2. [가장 중요] 위젯들이 담기는 메인 영역을 흰색 카드로 강제 설정 */
  div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"]) {{
   background-color: {STYLE_CONFIG['fg_color']};
   border-radius: {STYLE_CONFIG['corner_radius']};
   border: {STYLE_CONFIG['border_width']} solid {STYLE_CONFIG['border_color']};
   padding: 4rem 3rem;
   box-shadow: 0 20px 40px rgba(0,0,0,0.08);
   margin-top: 2rem;
  }}

  /* 3. 상단 초록색 바 구현 (가상 요소 활용) */
  div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"])::before {{
   content: "";
   position: absolute;
   top: 0; left: 0; right: 0;
   height: 12px;
   background-color: {STYLE_CONFIG['border_color']};
   border-radius: {STYLE_CONFIG['corner_radius']} {STYLE_CONFIG['corner_radius']} 0 0;
  }}

  /* 4. 버튼 디자인 */
  div.stButton > button {{
   background-color: {STYLE_CONFIG['primary_color']} !important;
   color: white !important;
   border-radius: 15px !important;
   padding: 0.8rem !important;
   font-size: 1.25rem !important;
   font-weight: 700 !important;
   width: 100% !important;
   border: none !important;
   margin-top: 1rem;
  }}

  /* 5. 텍스트 및 라벨 색상 */
  label, h1, h3, p {{
   color: {STYLE_CONFIG['text_color']} !important;
  }}
 </style>
""", unsafe_allow_html=True)

# 카드 내부 레이아웃 시작 (st.container를 사용하여 내부 요소를 묶어줍니다)
main_container = st.container()

with main_container:
 # 헤더
 st.markdown(f"""
  <div style="margin-bottom: 2rem;">
   <h1 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem;">건강 정보 입력</h1>
   <p style="opacity: 0.7; font-size: 1.1rem;">정확한 건강 분석을 위해 정보를 입력해 주세요.</p>
  </div>
 """, unsafe_allow_html=True)

 # 👤 기본 인적 사항
 st.markdown('### 👤 기본 인적 사항', unsafe_allow_html=True)
 col_name, col_gender = st.columns([1.5, 1])
 with col_name:
  name = st.text_input("성함", placeholder="성함을 입력하세요")
 with col_gender:
  gender = st.radio("성별", ["남성", "여성"], horizontal=True)

 st.markdown('<div style="margin: 2rem 0; border-top: 1px solid #eee;"></div>', unsafe_allow_html=True)

 # ⚖️ 신체 정보
 st.markdown('### ⚖️ 신체 정보', unsafe_allow_html=True)
 c1, c2, c3 = st.columns(3)
 with c1:
  age = st.number_input("나이 (세)", value=20, step=1)
 with c2:
  height = st.number_input("키 (cm)", value=160, step=1)
 with c3:
  weight = st.number_input("몸무게 (kg)", value=60, step=1)

 st.markdown('<div style="margin: 2rem 0; border-top: 1px solid #eee;"></div>', unsafe_allow_html=True)

 # 🏥 보유 질환
 st.markdown('### 🏥 보유 질환 (중복 선택 가능)', unsafe_allow_html=True)
 diseases = st.multiselect(
  "해당되는 항목을 선택하세요",
  ["고혈압", "당뇨병", "고지혈증", "관절염", "심장질환", "해당 없음"],
  label_visibility="collapsed"
 )

 # 분석 버튼
 if st.button("분석 결과 확인하기 →"):
  st.success(f"{name} 님의 분석 결과가 준비되었습니다.")

 # 하단 안내 문구
 st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 0.85rem; margin-top: 2rem;">입력하신 정보는 분석 목적으로만 사용되며 안전하게 보호됩니다.</p>', unsafe_allow_html=True)