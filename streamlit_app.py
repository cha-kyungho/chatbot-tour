import openai
import streamlit as st
from openai import OpenAI
import os


# 개선 1 : 대화 흐름 개선
# 개선 2 : 시스템 메시지 넣기(여행용 챗봇)
# 개선 3 : 대화 초기화 버튼 추가해 보기.
# 개선 4 : 대화가 여러 언어가 동시에 대답을 하도록 하기.

# Streamlit app
st.title("여행용 챗봇과 대화하기")

# client = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
openai_api_key = st.secrets['REPLICATE_KEY']['API_KEY']
client = OpenAI(api_key  = openai_api_key)


# 언어 선택 체크박스  
st.sidebar.subheader("언어 선택")  
languages = {  
    "한국어": "ko",  
    "영어": "en",  
    "일본어": "ja",  
    "중국어": "zh"  
}  

selected_languages = st.sidebar.multiselect("지원할 언어를 선택하세요:", 
                                    list(languages.keys()), default=["한국어"])

# 초기 대화 상태 설정
# 개선 2
if "messages" not in st.session_state:
    # 시스템 메시지에 선택된 언어 반영  
    language_list = ", ".join(selected_languages) 
    st.session_state.messages = [  
        {"role": "system", 
         "content": "당신은 여행에 관한 질문에 답하는 챗봇입니다. "
                    "여행지 추천, 준비물, 문화, 음식 등 다양한 주제에 대해 친절하게 안내해 주세요."
                    "답변은 기본적으로 한국어로 그리고 동시에 일본어로 번역해서 답변해 주렴."}  
    ] 

# 사용자 입력
user_input = st.text_input("당신:", key="user_input")

# 개선 3 : 대화 초기화 버튼 추가
if st.button("대화 초기화") and st.session_state.messages:
    st.session_state.messages = []

if st.button("전송") and user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", 
                                      "content": user_input})

    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # gpt-4로 변경
        messages=st.session_state.messages
    )

    # OpenAI 응답 추가
    response_message = response.choices[0].message.content
    # st.session_state.messages.append(response_message)
    st.session_state.messages.append({"role": "assistant", 
                                      "content": response_message})

    # 사용자 입력 초기화
    user_input = ""

# 대화 내용 표시
for message in st.session_state.messages:
    # st.markdown(message)
    role = "👤"  if message["role"] == "user" else "🤖"
    # st.markdown(f"👤: {response_message}")
    st.markdown(f"{role}: {message['content']}")

# 선택된 언어에 따라 응답 표시  
for lang in selected_languages:  
    if lang != "한국어":  # 한국어는 기본 언어로 사용  
        translated_message = f"{message['content']} ({lang})"  # 번역된 메시지 표시 (실제 번역 로직은 필요)  
        st.markdown(f"🤖 ({lang}): {translated_message}")
