### ✅ 소개
>기존 서비스 고도화를 위하여 추천 알고리즘에 초점을 맞추어 제작해 본 서비스 프로토타입입니다.

'추천 알고리즘 기반 맞춤 도서 추천 서비스'입니다. 사용자는 중학생으로 가정하였으며, 진단평가 응시 후 평가 결과를 바탕으로 맞춤 도서를 추천 받을 수 있습니다.
현재 사용자별 평가 결과와 신규 사용자 여부는 랜덤 지정되도록 해두었으며, 추천 도서 만족도 평가 결과는 저장되지 않습니다.
맞춤 도서 추천 방식은 이미지를 참고하여 주세요.
![제안](https://github.com/user-attachments/assets/82112f34-24ce-4725-ae98-79d77069a4c0)
![제안 (1)](https://github.com/user-attachments/assets/5310431e-aafd-4833-91a3-cee68cea254b)
![제안 (2)](https://github.com/user-attachments/assets/68d6a328-5bae-401f-a7f0-d338052ff207)
![제안 (3)](https://github.com/user-attachments/assets/b04675f2-f6f2-43e1-81a5-24830ec8c159)

### ✅ 실행 순서
1. data 폴더에 도서 목록 파일을 생성하여 주세요. 본 서비스의 경우 아래와 같이 구성되어 있습니다.
>인문.xlsx
사회.xlsx
과학.xlsx
문학.xlsx<br>
파일별 컬럼 : Category(인문 1, 사회 2, 과학 3, 문학 4), Grade(추천 학년), Writer(작가), Content(줄거리)
2. pip install -r requirements.txt
3. streamlit run app.py

감사합니다 🙌
