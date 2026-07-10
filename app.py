# 강원생활도우미앱 — 추천 이유 문장 출력 기능 확장 (SDD 레거시 확장)
# 기존 함수는 전부 보존, 새 기능은 make_reasons 새 함수로만 추가

import streamlit as st
import pandas as pd

# ── 기존 함수 (그대로 보존) ─────────────────────────────
def load_data(path):
    place_df = pd.read_excel(path, sheet_name='장소정보')
    recommend_df = pd.read_excel(path, sheet_name='추천정보')
    return place_df, recommend_df

def join_data(place_df, recommend_df):
    return pd.merge(recommend_df, place_df, on='place_id', how='left')

def filter_recommendations(df, 지역, 추천목적, 추천상황, 추천대상, 예산):
    return df[
        (df['지역'] == 지역) & (df['추천목적'] == 추천목적) &
        (df['추천상황'] == 추천상황) & (df['추천대상'] == 추천대상) &
        (df['예산'] <= 예산)
    ]

# ── 새 함수 (이번 확장, 기존 코드는 안 건드림) ──────────
def make_reasons(df):
    """검색 결과 DataFrame을 복사해 '추천이유' 열을 붙여 반환 (원본 불변)"""
    result = df.copy()
    reasons = []
    for _, row in result.iterrows():
        parts = [f"{row['이름']}은(는) 평점 {row['평점']}점"]
        parts.append(f"예산 {int(row['예산'])}원")
        if row['예약필요'] == '아니오':
            parts.append('예약 없이 바로 방문 가능')
        sentence = ', '.join(parts) + f"이라서 {row['추천목적']}하기 좋은 곳입니다."
        reasons.append(sentence)
    result['추천이유'] = reasons
    return result

# ── 화면 ────────────────────────────────────────────────
st.title('강원생활도우미')

place_df, recommend_df = load_data('gangwon_data.xlsx')
merged_df = join_data(place_df, recommend_df)

지역 = st.selectbox('지역', sorted(merged_df['지역'].unique()))
추천목적 = st.selectbox('목적', sorted(merged_df['추천목적'].unique()))
추천상황 = st.selectbox('상황', sorted(merged_df['추천상황'].unique()))
추천대상 = st.selectbox('대상', sorted(merged_df['추천대상'].unique()))
예산 = st.number_input('예산(원)', min_value=0, value=10000, step=1000)

if st.button('검색'):
    st.session_state['result'] = filter_recommendations(
        merged_df, 지역, 추천목적, 추천상황, 추천대상, 예산)

if 'result' in st.session_state:
    result = st.session_state['result']
    if len(result) > 0:
        st.dataframe(result)                      # 기존 출력 그대로
        st.bar_chart(result.set_index('이름')['평점'])  # 기존 차트 그대로
        # ↓ 새 기능: 체크박스 켰을 때만 새 함수 호출
        if st.checkbox('추천 이유 보기'):
            for s in make_reasons(result)['추천이유']:
                st.info(s)
    else:
        st.warning('조건에 맞는 추천 장소가 없습니다.')
