import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from random_data import student_list, book_list, recommendation_list

# 도서 추천 시스템
def recommend_books(user, book_list, recommendation_list):
    if user['서비스 신규 사용자 여부']:
        # 신규 사용자: 콘텐츠 기반 추천
        content_recommendations = content_based_recommendation(user, book_list)
        return content_recommendations, []
    else:
        # 기존 사용자: 콘텐츠 기반 + 협업 필터링 추천
        content_recommendations = content_based_recommendation(user, book_list)
        collaborative_recommendations = collaborative_filtering(user, recommendation_list, content_recommendations)
        return content_recommendations, collaborative_recommendations

def content_based_recommendation(user, book_list):
    # 학생의 취약 영역을 찾음 (최소 점수)
    element_weakest_skills = get_weakest_skills(user['진단평가 결과(요소)'])
    area_weakest_skills = get_weakest_skills(user['진단평가 결과(영역)'])
    
    # 각 취약 영역에서 도서 추천
    recommended_books = []
    
    # '진단평가 결과(요소)'에서 취약 영역 도서 추천
    for skill in element_weakest_skills:
        books_for_skill = book_list[book_list['독서능력 요소'] == skill]
        if len(books_for_skill) >= 2:
            recommended_books.extend(books_for_skill[['책 제목', '작가', '줄거리']].sample(2).values.tolist())
        else:
            recommended_books.extend(books_for_skill[['책 제목', '작가', '줄거리']].values.tolist())
    
    # '진단평가 결과(영역)'에서 취약 영역 도서 추천
    for area in area_weakest_skills:
        books_for_area = book_list[book_list['독서능력 영역'] == area]
        if len(books_for_area) >= 2:
            recommended_books.extend(books_for_area[['책 제목', '작가', '줄거리']].sample(2).values.tolist())
        else:
            recommended_books.extend(books_for_area[['책 제목', '작가', '줄거리']].values.tolist())
    
    # 추천 도서가 4개 미만일 경우 추가 추천
    if len(recommended_books) < 4:
        remaining_books = book_list[~book_list['책 제목'].isin([book[0] for book in recommended_books])]
        additional_books = remaining_books[['책 제목', '작가', '줄거리']].sample(4 - len(recommended_books)).values.tolist()
        recommended_books.extend(additional_books)
    
    return recommended_books

def collaborative_filtering(user, recommendation_list, recommended_books):

    # 비정상적인 값을 처리하고, 만족 여부 열의 데이터 타입을 정수형으로 변환
    recommendation_list['만족 여부'] = pd.to_numeric(recommendation_list['만족 여부'], errors='coerce')
    recommendation_list = recommendation_list.dropna(subset=['만족 여부'])
    recommendation_list['만족 여부'] = recommendation_list['만족 여부'].astype(int)
    
    # 유사한 사용자 찾기: 과거 만족도를 기준으로 사용자 간 유사도를 계산
    user_ratings = recommendation_list.pivot_table(index='이름', columns='책 제목', values='만족 여부', fill_value=0)
    
    if user['이름'] not in user_ratings.index:
        return []

    # 유사도 계산
    similarity_matrix = cosine_similarity(user_ratings)
    similarity_df = pd.DataFrame(similarity_matrix, index=user_ratings.index, columns=user_ratings.index)

    similar_users = similarity_df[user['이름']].sort_values(ascending=False).index[1:4]

    # 유사한 사용자들이 좋아했던 도서 추천
    recommended_books_set = set(tuple(book) for book in recommended_books)
    similar_users_recommendations = []

    for similar_user in similar_users:
        similar_user_books = recommendation_list[recommendation_list['이름'] == similar_user]
        liked_books = similar_user_books[similar_user_books['만족 여부'] == 1][['책 제목', '작가', '줄거리']].values.tolist()
        for book in liked_books:
            if tuple(book) not in recommended_books_set:
                similar_users_recommendations.append(book)

    return similar_users_recommendations[:2]  # 추천할 도서 수 제한

def hybrid_recommendation(user, books_df, recommendation_list, recommended_books):
    # 콘텐츠 기반 추천
    content_recommendations = content_based_recommendation(user, books_df)

    # 협업 필터링 추천 (신규 사용자는 협업 필터링 제외)
    collaborative_recommendations = collaborative_filtering(user, recommendation_list, recommended_books)
    hybrid_recommendations = content_recommendations + collaborative_recommendations

    return hybrid_recommendations

def get_weakest_skills(diagnosis_results):
    # 최소 점수를 가진 영역을 추출
    min_score = min(diagnosis_results.values())
    weakest_skills = [skill for skill, score in diagnosis_results.items() if score == min_score]
    return weakest_skills

recommendation_data = []

for idx, user in student_list.iterrows():
    content_recommendations, collaborative_recommendations = recommend_books(user, book_list, recommendation_list)
    recommendation_data.append({
        '이름': user['이름'],
        '콘텐츠 기반 추천 도서': content_recommendations,
        '협업 필터링 추천 도서': collaborative_recommendations
    })

# 데이터프레임 생성
recommendation_df = pd.DataFrame(recommendation_data)