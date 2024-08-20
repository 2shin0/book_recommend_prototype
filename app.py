import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from book_rec import recommend_books
from random_data import student_list, book_list, recommendation_list

st.set_page_config(
    page_title="맞춤 도서 추천",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit 애플리케이션 제목
st.title("📚 맞춤 도서 추천 💯")

with st.sidebar:
    choice = option_menu("", ["시험 응시", "맞춤 도서 추천", "추천 도서 만족도 평가"],
    icons=['house', 'bi bi-robot', 'bi bi-check2-all'],
    menu_icon="app-indicator", default_index=0,
    styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )

student_name = st.text_input("학생 이름")

if choice == '시험 응시':
    # 지문 1
    st.subheader("과학")
    st.write("""
    봄이 되면 많은 식물들이 새싹을 틔우고, 꽃을 피우며 자생력을 발휘합니다. 새싹이 자라서 나무가 되고, 꽃이 피면 열매가 열립니다. 이런 자연의 순환 과정은 생태계의 중요한 부분을 차지합니다.
    """)

    # 문제 1과 문제 2
    st.write("문제 1: 지문 1의 주제는 무엇인가요?")
    q1 = st.radio("문제 1", ["a) 봄의 날씨", "b) 자연의 순환 과정", "c) 식물의 성장"])

    st.write("문제 2: 지문 1에서 언급된 식물의 발전 과정은 어떤 것인가요?")
    q2 = st.radio("문제 2", ["a) 씨앗 → 나무 → 열매", "b) 새싹 → 꽃 → 나무", "c) 새싹 → 나무 → 꽃"])

    # 지문 2
    st.subheader("사회")
    st.write("""
    한국의 전통 음식 중 하나인 김치는 여러 가지 채소와 양념을 사용하여 만들며, 발효 과정을 거쳐 독특한 맛과 영양을 갖추게 됩니다. 김치는 한국의 식탁에서 빠질 수 없는 음식입니다.
    """)

    # 문제 3과 문제 4
    st.write("문제 3: 지문 2에서 김치의 주요 특징은 무엇인가요?")
    q3 = st.radio("문제 3", ["a) 발효 과정이 있다", "b) 고기가 포함된다", "c) 단맛이 있다"])

    st.write("문제 4: 지문 2의 김치가 한국의 식탁에서 어떤 역할을 하나요?")
    q4 = st.radio("문제 4", ["a) 자주 먹지 않는다", "b) 특별한 날에만 먹는다", "c) 자주 먹는 음식이다"])

if st.button("제출"):
        st.write(f"{student_name}님의 진단평가 결과입니다.")

        # 선택된 학생의 데이터 필터링
        student_data = student_list[student_list['이름'] == student_name].iloc[0]
        
        # 진단평가 결과(요소) 데이터프레임 생성
        element_results = pd.DataFrame(student_data['진단평가 결과(요소)'], index=['점수']).T.reset_index()
        element_results.rename(columns={'index': '요소', '점수': '점수'}, inplace=True)
        
        st.write("### 진단평가 결과(요소)")
        st.dataframe(element_results)

        # 진단평가 결과(영역) 데이터프레임 생성
        area_results = pd.DataFrame(student_data['진단평가 결과(영역)'], index=['점수']).T.reset_index()
        area_results.rename(columns={'index': '영역', '점수': '점수'}, inplace=True)
        
        st.write("### 진단평가 결과(영역)")
        st.dataframe(area_results)

        # 서비스 신규 사용자 여부
        new_tf = pd.DataFrame({'여부': [student_data['서비스 신규 사용자 여부']]}, index=['신규 사용자 여부']).reset_index()
        new_tf.rename(columns={'index': '여부', '여부': '신규 사용자 여부'}, inplace=True)

        st.write("### 서비스 신규 사용자 여부")
        st.dataframe(new_tf)

elif choice == '맞춤 도서 추천':

        if student_name:
            st.write(f"{student_name}님께 꼭 맞는 추천 도서입니다.")
            recommendation_data = []

            for idx, user in student_list.iterrows():
                content_recommendations, collaborative_recommendations = recommend_books(user, book_list, recommendation_list)
                recommendation_data.append({
                    '이름': user['이름'],
                    '콘텐츠 기반 추천 도서': content_recommendations,
                    '협업 필터링 추천 도서': collaborative_recommendations
                })

            st.session_state.recommendation_data = recommendation_data
            st.session_state.selected_student_name = student_name

            filtered_data = next((data for data in recommendation_data if data['이름'] == student_name), None)

            if filtered_data:
                st.markdown("### 📕 콘텐츠 기반 추천 도서")
                if filtered_data['콘텐츠 기반 추천 도서']:
                    for book in filtered_data['콘텐츠 기반 추천 도서']:
                        st.markdown(f"**책 제목:** {book[0]}")
                        st.markdown(f"**작가:** {book[1]}")
                        st.markdown(f"**줄거리:** {book[2]}")
                        st.markdown("---")
                else:
                    st.markdown("추천할 도서가 없습니다.")

                st.markdown("### 📗 협업 필터링 추천 도서")
                if filtered_data['협업 필터링 추천 도서']:
                    for book in filtered_data['협업 필터링 추천 도서']:
                        st.markdown(f"**책 제목:** {book[0]}")
                        st.markdown(f"**작가:** {book[1]}")
                        st.markdown(f"**줄거리:** {book[2]}")
                        st.markdown("---")
                else:
                    st.markdown("추천 도서에 대한 만족도 평가를 하시면 다음 평가 결과부터 협업 필터링 추천 결과를 받으실 수 있습니다.")
            else:
                st.markdown("해당 학생의 추천 도서를 찾을 수 없습니다.")

elif choice == '추천 도서 만족도 평가':
    st.write("추천 도서가 마음에 드시면 만족 버튼을 눌러 주세요. 다음 도서 추천에서 사용자의 취향을 바탕으로 더욱 정확한 추천이 가능해집니다.")

    if 'recommendation_data' in st.session_state and 'selected_student_name' in st.session_state:
        recommendation_data = st.session_state.recommendation_data
        student_name = st.session_state.selected_student_name
        
        # 선택된 학생의 데이터 필터링
        filtered_data = next((data for data in recommendation_data if data['이름'] == student_name), None)

        if filtered_data:
            recommendation_sections = ['콘텐츠 기반 추천 도서', '협업 필터링 추천 도서']

            for section in recommendation_sections:
                st.subheader(section)
                books = filtered_data[section]
                
                if not books:
                    st.markdown("추천 도서에 대한 만족도 평가를 하시면 다음 평가 결과부터 협업 필터링 추천 결과를 받으실 수 있습니다.")
                else:
                    for idx, book in enumerate(books):
                        book_title, book_author, book_summary = book[0], book[1], book[2]
                        
                        st.markdown(f"**책 제목:** {book_title}")
                        st.markdown(f"**작가:** {book_author}")
                        st.markdown(f"**줄거리:** {book_summary}")
                        
                        # 만족도 버튼에 고유 키 추가
                        if st.button(f"만족 - {book_title}", key=f"button_{idx}_{book_title}"):
                            # 만족도 평가 결과를 처리하는 로직
                            st.write(f"{book_title}에 대한 만족도가 기록되었습니다.")
        else:
            st.markdown("해당 학생의 추천 도서를 찾을 수 없습니다.")
    else:
        st.markdown("추천 도서 데이터를 로드할 수 없습니다.")