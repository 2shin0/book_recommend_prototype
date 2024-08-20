import pandas as pd
import numpy as np
import random

# 엑셀 파일 경로
file_paths = {
    '과학': 'data/과학.xlsx',
    '사회': 'data/사회.xlsx',
    '인문': 'data/인문.xlsx',
    '문학': 'data/문학.xlsx'
}

# 독서능력 요소 랜덤 지정 함수
def assign_random_ability(df):
    ability_elements = ['이해력', '추론력', '비판력', '종합']
    df['독서능력 요소'] = np.random.choice(ability_elements, len(df))
    return df

# 각 시트에서 데이터 읽어오기
def read_excel_sheets(file_paths):
    data_frames = {}
    for category, path in file_paths.items():
        # 엑셀 파일 읽기
        df = pd.read_excel(path, engine='openpyxl')
        
        # 필요한 컬럼 선택 및 이름 변경
        df = df[['Grade', 'BookTitle', 'Writer', 'Content']]
        df.rename(columns={'Grade': '추천 학년', 'BookTitle': '책 제목', 'Writer': '작가', 'Content': '줄거리'}, inplace=True)
        
        # 독서능력 영역 추가
        df['독서능력 영역'] = category
        
        # 독서능력 요소 랜덤 지정
        df = assign_random_ability(df)
        
        data_frames[category] = df
    return data_frames

# 데이터 읽어오기
books_data = read_excel_sheets(file_paths)

# 데이터 통합
def combine_dataframes(data_frames):
    combined_df = pd.DataFrame()
    
    for _, df in data_frames.items():
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    return combined_df

# 데이터 통합
book_list = combine_dataframes(books_data)




# 학생 이름 리스트
names_list = [
    '김민준', '이서연', '박준호', '최지우', '정서원', '강현우', '조수빈', '오민석',
    '임하늘', '서동현', '한지민', '류호준', '안지우', '전진우', '서민정', '류준호',
    '최유리', '배현수', '원지훈', '남지연'
]

# 학년 리스트
grades = ['M1', 'M2', 'M3']

# 진단평가 결과 랜덤 생성 함수
def generate_diagnosis_element():
    return {
        '이해력': random.randint(1, 4),
        '추론력': random.randint(1, 4),
        '비판력': random.randint(1, 4),
        '종합': random.randint(1, 4)
    }

def generate_diagnosis_category():
    return {
        '과학': random.randint(1, 4),
        '사회': random.randint(1, 4),
        '인문': random.randint(1, 4),
        '문학': random.randint(1, 4)
    }

# 데이터 생성 함수
def create_students(num_students):
    students = []
    names_count = len(names_list)
    for i in range(num_students):
        student = {
            '이름': names_list[i % names_count],  # 순서대로 이름을 선택
            '학년': random.choice(grades),
            '진단평가 결과(요소)': generate_diagnosis_element(),
            '진단평가 결과(영역)': generate_diagnosis_category(),
            '서비스 신규 사용자 여부': random.choice([True, False])
        }
        students.append(student)
    return students

# 학생 데이터 생성
num_students = 20
students_data = create_students(num_students)

# 데이터프레임으로 변환
student_list = pd.DataFrame(students_data)





# 추천 도서 목록 생성 함수
def generate_recommendations(num_books):
    return book_list.sample(num_books)

# 만족도 데이터 생성 함수
def generate_satisfaction():
    return random.choice([0, 1]) 

# 진단평가 회차 
def get_random_assessment_round():
    return random.randint(2, 5)

# 추천받은 도서 목록과 만족도 생성
def create_recommendation_data(df):
    recommendation_data = []
    
    for index, row in df.iterrows():
        # 추천 도서 목록 (랜덤으로 3권 추천)
        recommended_books = generate_recommendations(3)

        # 진단평가 회차 설정
        if row['서비스 신규 사용자 여부']:
            assessment_round = 1
        else:
            assessment_round = get_random_assessment_round()
            
        for _, book_row in recommended_books.iterrows():
            book_title = book_row['책 제목']
            book_author = book_row['작가']
            book_content = book_row['줄거리']

            # 만족도 (각 도서마다 랜덤 생성)
            if row['서비스 신규 사용자 여부']:
                satisfaction = 'None'
            else:
                satisfaction = generate_satisfaction()

            recommendation_data.append({
                '이름': row['이름'],
                '학년': row['학년'],
                '진단평가 회차': assessment_round,
                '책 제목': book_title,
                '작가': book_author,
                '줄거리' : book_content,
                '만족 여부': satisfaction
            })
    
    return pd.DataFrame(recommendation_data)

# 추천 데이터 생성
recommendation_list = create_recommendation_data(student_list)