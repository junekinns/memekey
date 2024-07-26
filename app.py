import streamlit as st
import pandas as pd

st.title('간단한 Streamlit 앱')

# 데이터 생성
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수', '정지은'],
    '나이': [25, 28, 22, 30],
    '점수': [85, 92, 78, 95]
})

# 데이터프레임 표시
st.write("## 학생 데이터")
st.dataframe(df)

# 차트 그리기
st.write("## 점수 분포")
st.bar_chart(df['점수'])

# 사용자 입력 받기
name = st.text_input("이름을 입력하세요")
if name:
    st.write(f"안녕하세요, {name}님!")

# 슬라이더로 값 선택하기
age = st.slider("나이를 선택하세요", 0, 100, 25)
st.write(f"선택한 나이: {age}")