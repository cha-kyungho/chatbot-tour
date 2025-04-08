import requests

import openai
import streamlit as st
from openai import OpenAI
import os
import datetime


#streamlit secrets 로드확인
#st.write(st.secrets)

# Streamlit app
st.title("사주분석 챗봇과 대화")

# client = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
openai_api_key = st.secrets['openai']['API_KEY']
client = OpenAI(api_key  = openai_api_key)


# 언어 선택 체크박스  
st.sidebar.subheader("사주풀이")  
st.sidebar.write("생년월일과 시간을 입력하면 사주풀이 결과를 제공합니다.")

# 사용자 입력 받기
name = st.sidebar.text_input("이름을 입력하세요:")
birth_date = st.sidebar.date_input("생년월일을 선택하세요:", "2000-01-01")
birth_time = st.sidebar.time_input("출생 시간을 선택하세요:", "09:00")
# 시스템 메시지에 오늘 날짜 추가
today = datetime.date.today()

#초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 사용자 입력
user_input = st.sidebar.text_input("질문:", key="user_input")

if st.sidebar.button("전송") :
    if not name or not birth_date or not birth_time or not user_input:
        # 사용자 입력이 없을 경우 경고 메시지 표시
        st.warning("이름, 생년월일, 출생시간, 질문을 모두 입력해주세요.")
        st.stop() # 중단
    
    if len(st.session_state.messages) < 2:  # 수정: count -> len
        # 초기 대화 상태 설정
        # 시스템 메시지에 선택된 언어 반영  
        st.session_state.messages = [  
            {"role": "system", 
             "content": "당신은 사주풀이 전문가 챗봇입니다."
                        "기본 사주 내용과 자세한 사주 내용과 풀이 근거를 알려주고 요약 내용을 제공해줘."
                        "답변 내용이 자세하고 길게 설명해 줬으면 좋겠어." }
        ] 
        # 시스템 메시지에 사용자 정보를 추가
        user_info = "사용자정보 이름: {}, 생년월일: {}, 출생시간: {}, 오늘: {}".format(name, birth_date, birth_time, today)
        st.session_state.messages.append({"role": "user", 
                                          "content": user_info})

    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", 
                                      "content": user_input})

    st.markdown("---")
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

# 개선 3 : 대화 초기화 버튼 추가
if st.button("대화 초기화") and st.session_state.messages:
    st.session_state.messages = []


# 대화 내용 표시
for message in st.session_state.messages:
    if message["role"] == "user" and message["content"].find("사용자정보") == -1:
        # 사용자 메시지를 우측 정렬
        st.markdown(
            f"""
            <div style="text-align: right; color: blue;">
                질문: {message['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

    if message["role"] == "assistant":
        st.markdown(f"{message['content']}")
        st.markdown("---")  # 구분선 추가
