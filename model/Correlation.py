import numpy as np
import pandas as pd
import json
from . import Model_constant as STRING

'''
Correlation : 영화 데이터셋과 별점 데이터셋을 이용하여 피어슨 상관관계를 계산하는 함수를 모아둔 클래스를 저장한 파일

전제적인 틀은 오픈소스를 가져왔고, 추가하고 싶은 것 추가하고 수정할 부분을 수정했다.

추가한 부분 : 영화의 PUPULARITY, VOTE_AVERAGE 데이터를 추가로 가져와서, PUPULARITY_CUTLINE와 VOTE_AVERAGE_CUTLINE 변수를 사용하여 영화의 유명한 정도와 평점으로 출력 커트라인을 만들었다. 이것을 추가하기 전에는 들어보지도 못한 유명하지 않은 영화들이 결과값으로 출력됐다.
추가한 부분 : overview 데이터를 추가로 가져와서 줄거리를 결과값에 포함하도록 바꿨다.

수정한 부분 : 사용하기 편하게 결과값을 list 형식이 아니라 dict 형식으로 바꿨다.
수정한 부분 : 함수 형식으로 나누어져 있던 오픈소스 코드를 클래스로 묶어서 생성자와 메서드로 분리해줬다.
수정한 부분 : recommand 메서드를 목적에 맞게 일부 수정했다.
'''

# 영화 데이터셋과 별점 데이터셋을 이용하여 피어슨 상관관계를 계산하는 함수를 모아둔 클래스
class Correlation:
    # 5.0 : 어느정도 성공한 영화 10.0 : 꽤 성공한 영화 20.0 : 글로벌 히트작
    # 해당 값 아래인 영화는 결과값에서 제외했다.
    PUPULARITY_CUTLINE = 13.5
    # 0.0 ~ 10.0 전체 유저 평점의 평균
    # 해당 값 아래인 영화는 결과값에서 제외했다.
    VOTE_AVERAGE_CUTLINE = 6.0

    # 인자에 self는 클래스 자신의 주소이다. 클래스의 메서드(함수)면 무조건 써줘야함
    # 데이터셋에서 필요한 데이터를 가공하여 가져오는 생성자 메서드(클래스를 불러올때 자동으로 실행되는 함수)
    def __init__(self):
        self.meta = pd.read_csv(STRING.MOVIE_DATASET_LOCATION, low_memory=False)
        self.meta = self.meta[[STRING.ID_STR, STRING.ORIGINAL_TITLE_STR, STRING.ORIGINAL_LANGUAGE_STR, STRING.GENRES_STR, STRING.OVERVIEW_STR, STRING.POLULARITY_STR, 'vote_average']] # csv 파일에서 가져올 정보들.
        self.meta = self.meta.rename(columns={STRING.ID_STR:STRING.MOVIE_ID_STR}) # id를 헷갈리지 않게 하기 위해 이름을 movieId로 변경
        self.meta = self.meta[self.meta[STRING.ORIGINAL_LANGUAGE_STR] == 'en'] # 영어로 된 영어들만 하기
        self.ratings = pd.read_csv(STRING.RATING_DATASET_LOCATION)
        self.ratings = self.ratings[[STRING.USER_ID_STR, STRING.MOVIE_ID_STR, STRING.RATING_STR]]
        self.ratings.describe()
        self.meta.movieId = pd.to_numeric(self.meta.movieId, errors=STRING.COERCE_STR) # 숫자 문자열을을 숫자형식으로 변경
        self.ratings.movieId = pd.to_numeric(self.ratings.movieId, errors=STRING.COERCE_STR)  # 동일
        self.meta[STRING.GENRES_STR] = self.meta[STRING.GENRES_STR].apply(self.parse_genres)
        
    # 가져온 데이터들과 별점 데이터들을 합쳐서 반환하는 함수
    def getData(self):
        return pd.merge(self.ratings, self.meta, on=STRING.MOVIE_ID_STR, how='inner') # 메타 데이터와 별점 데이터를 합침

    # 장르 데이터를 분석하여 반환하는 함수
    def parse_genres(self, genres_str):
        genres = json.loads(genres_str.replace(STRING.QUOTE_STR, STRING.DOUBLE_QUOTE_STR))
        genres_list = []
        for g in genres:
            genres_list.append(g[STRING.NAME_STR])
        return genres_list

     # 피어슨 상관관계를 계산하는 함수
    def pearsonR(self, s1, s2):
        s1_c = s1 - s1.mean()
        s2_c = s2 - s2.mean()
        a = np.sum(s1_c * s2_c)
        b = np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))
        if b:
            return a / b
        else:
            return a / (b + 0.0000001)

    # 위에 작성한 메서드(함수)들을 사용하여 input_movie 영화와 matrix 안의 모든 영화들의 상관관계를 반환하는 함수
    def recommend(self, input_movie, matrix, genre_weight): # 영화이름, 데이터, 장르를 연관성 점수에 반영할것인지 여부를 입력받는다.
        input_genres = self.meta[self.meta[STRING.ORIGINAL_TITLE_STR] == input_movie][STRING.GENRES_STR].iloc(0)[0] # 입력받은 영화의 장르 데이터 변수에 저장
        result = []
        for title in matrix.columns: # 모든 영화 데이터 검사
            if title == input_movie: # 입력받은 영화랑 같은 영화면 넘기기
                continue
            popularity = float(self.meta[self.meta[STRING.ORIGINAL_TITLE_STR] == title][STRING.POLULARITY_STR].iloc(0)[0])
            vote_average = float(self.meta[self.meta[STRING.ORIGINAL_TITLE_STR] == title][STRING.VOTE_AVERAGE_STR].iloc(0)[0])
            if popularity < self.PUPULARITY_CUTLINE:
                continue
            if vote_average < self.VOTE_AVERAGE_CUTLINE:
                continue

            # 별점 비교
            cor = self.pearsonR(matrix[input_movie], matrix[title]) # 피어슨 상관관계로 연관성 계산한 값을 cor에 저장
            if len(input_genres) > 0: # 장르 데이터가 존재하면
                temp_genres = self.meta[self.meta[STRING.ORIGINAL_TITLE_STR] == title][STRING.GENRES_STR].iloc(0)[0] # temp_genres에 장르데이터 저장

            # 장르 비교
            if len(input_genres) > 0: # 장르가 같으면 연관성 점수에 추가 점수 부여
                same_count = np.sum(np.isin(input_genres, temp_genres))
                cor += (genre_weight * same_count)

            # 줄거리 받아오기
            overview = self.get_overview(self.meta, title) # ovew에 줄거리 데이터 저장

            if np.isnan(cor):
                continue
            else:
                result_dict = {STRING.TITLE_STR:title, STRING.SCORE_STR : cor, STRING.GENRES_STR : temp_genres, STRING.OVERVIEW_STR : overview}
                result.append(result_dict)

        return result

    def get_overview(self, meta, title):
        return meta[meta[STRING.ORIGINAL_TITLE_STR] == title][STRING.OVERVIEW_STR].iloc(0)[0]