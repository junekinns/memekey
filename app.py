import streamlit as st
import requests
import utils
import os
from PIL import Image

logo_path = "logo.png"
logo = Image.open(logo_path)
st.image(logo)

image_dir = "imgs"
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
image_files = image_files[:7]
selected_member = "JHOPE"

# 선택 상태를 저장할 세션 상태 초기화
if 'selected' not in st.session_state:
    st.session_state.selected = [False] * len(image_files)

st.markdown("""
<style>
    .rounded-image {
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 5px;
    }
    .stButton>button {
        width: 100%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .selected {
        border: 4px solid rgba(214, 93, 174, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# 선택 상태를 저장할 세션 상태 초기화
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

# 이미지 표시 및 버튼 생성
for idx, (col, image_file) in enumerate(zip(st.columns(len(image_files)), image_files)):
    with col:
        st.markdown('<div class="image-button-container">', unsafe_allow_html=True)

        # 이미지 표시
        image_path = os.path.join(image_dir, image_file)
        img_base64 = utils.get_image_base64(image_path)
        selected_class = "selected" if st.session_state.selected_index == idx else ""
        st.markdown(f"""
        <div class="rounded-image {selected_class}">
            <img src="data:image/png;base64,{img_base64}" style="width:100%;">
        </div>
        """, unsafe_allow_html=True)

        # 버튼 라벨 생성 (확장자 제거 및 대문자 변환)
        button_label = os.path.splitext(image_file)[0].upper()

        # 버튼 생성
        if st.button(button_label, key=f"btn_{idx}"):
            if st.session_state.selected_index == idx:
                st.session_state.selected_index = idx  # 같은 버튼을 다시 클릭하면 선택 해제
            else:
                st.session_state.selected_index = idx  # 다른 버튼을 클릭하면 해당 버튼만 선택
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.selected_index is not None:
    selected_item = os.path.splitext(image_files[st.session_state.selected_index])[0].upper()
    selected_member = selected_item

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chat with BTS!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    endpoint = "http://junekins.iptime.org:7860/translate"
    response = requests.post(endpoint, json={"text": prompt, "member": selected_member})

    if response.status_code == 200:
        result = response.json()
        full_response = result["completion"][0]['text']
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        with st.chat_message("assistant"):
            st.markdown(utils.format_response(full_response), unsafe_allow_html=True)
    else:
        error_message = "오류가 발생했습니다. 다시 시도해주세요."
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        with st.chat_message("assistant"):
            st.markdown(error_message)