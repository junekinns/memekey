import streamlit as st
import requests


st.title("Memekey")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("번역할 가사를 입력하세요:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    endpoint = "http://junekins.iptime.org:7860/translate"
    response = requests.post(endpoint, json={"text": prompt})

    if response.status_code == 200:
        result = response.json()
        title = result["title"]
        en_word = result["en_word"]
        en_meaning = result["en_meaning"]
        en_pronun = result["en_pronun"]
        lyric = result["lyric"]
        result = f"제목: {title}\n영어단어: {en_word}\n영어뜻: {en_meaning}\n영어발음: {en_pronun}\nlyric: {lyric}"
        st.session_state.messages.append({"role": "assistant", "content": result})
        with st.chat_message("assistant"):
            st.markdown(result)
    else:
        error_message = "오류가 발생했습니다. 다시 시도해주세요."
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        with st.chat_message("assistant"):
            st.markdown(error_message)