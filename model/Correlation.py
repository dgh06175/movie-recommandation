import numpy as np
import pandas as pd
import json

MOVIE_DATASET_LOCATION = 'the-movies-dataset/movies_metadata.csv'
RATING_DATASET_LOCATION = 'the-movies-dataset/ratings_small.csv'

NAME_STR = 'name'
TITLE_STR = 'title'
GENRES_STR = 'genres'
OVERVIEW_STR = 'overview'
ID_STR = 'id'
USER_ID_STR = 'userId'
MOVIE_ID_STR = 'movieId'
ORIGINAL_TITLE_STR = 'original_title'
ORIGINAL_LANGUAGE_STR = 'original_language'
RATING_STR = 'rating'
SCORE_STR = 'score'
POLULARITY_STR = 'popularity'
COERCE_STR = 'coerce'
QUOTE_STR = '\''
DOUBLE_QUOTE_STR = '"'
VOTE_AVERAGE_STR = 'vote_average'

# 영화 데이터셋과 별점 데이터셋을 이용하여 피어슨 상관관계를 계산하는 함수를 모아둔 클래스
class Correlation:
    # 5.0 : 어느정도 성공한 영화 10.0 : 꽤 성공한 영화 20.0 : 글로벌 히트작
    PUPULARITY_CUTLINE = 13.5
    # 0.0 ~ 10.0 전체 유저 평점의 평균
    VOTE_AVERAGE_CUTLINE = 6.0

    # 데이터셋에서 필요한 데이터를 가공하여 가져오는 생성자 메서드(클래스를 불러올때 자동으로 실행되는 함수)
    # 인자에 self는 클래스 자신의 주소이다. 클래스의 메서드(함수)면 무조건 써줘야함
    def __init__(self):
        self.meta = pd.read_csv(MOVIE_DATASET_LOCATION, low_memory=False)
        self.meta = self.meta[[ID_STR, ORIGINAL_TITLE_STR, ORIGINAL_LANGUAGE_STR, GENRES_STR, OVERVIEW_STR, POLULARITY_STR, 'vote_average']] # csv 파일에서 가져올 정보들.
        self.meta = self.meta.rename(columns={ID_STR:MOVIE_ID_STR}) # id를 헷갈리지 않게 하기 위해 이름을 movieId로 변경
        self.meta = self.meta[self.meta[ORIGINAL_LANGUAGE_STR] == 'en'] # 영어로 된 영어들만 하기
        self.ratings = pd.read_csv(RATING_DATASET_LOCATION)
        self.ratings = self.ratings[[USER_ID_STR, MOVIE_ID_STR, RATING_STR]]
        self.ratings.describe()
        self.meta.movieId = pd.to_numeric(self.meta.movieId, errors=COERCE_STR) # 숫자 문자열을을 숫자형식으로 변경
        self.ratings.movieId = pd.to_numeric(self.ratings.movieId, errors=COERCE_STR)  # 동일
        self.meta[GENRES_STR] = self.meta[GENRES_STR].apply(self.parse_genres)
        
    # 가져온 데이터들과 별점 데이터들을 합쳐서 반환하는 함수
    def getData(self):
        return pd.merge(self.ratings, self.meta, on=MOVIE_ID_STR, how='inner') # 메타 데이터와 별점 데이터를 합침

    # 장르 데이터를 분석하여 반환하는 함수
    def parse_genres(self, genres_str):
        genres = json.loads(genres_str.replace(QUOTE_STR, DOUBLE_QUOTE_STR))
        genres_list = []
        for g in genres:
            genres_list.append(g[NAME_STR])
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
        input_genres = self.meta[self.meta[ORIGINAL_TITLE_STR] == input_movie][GENRES_STR].iloc(0)[0] # 입력받은 영화의 장르 데이터 변수에 저장
        result = []
        for title in matrix.columns: # 모든 영화 데이터 검사
            if title == input_movie: # 입력받은 영화랑 같은 영화면 넘기기
                continue
            popularity = float(self.meta[self.meta[ORIGINAL_TITLE_STR] == title][POLULARITY_STR].iloc(0)[0])
            vote_average = float(self.meta[self.meta[ORIGINAL_TITLE_STR] == title][VOTE_AVERAGE_STR].iloc(0)[0])
            if popularity < self.PUPULARITY_CUTLINE:
                continue
            if vote_average < self.VOTE_AVERAGE_CUTLINE:
                continue

            # 별점 비교
            cor = self.pearsonR(matrix[input_movie], matrix[title]) # 피어슨 상관관계로 연관성 계산한 값을 cor에 저장
            if len(input_genres) > 0: # 장르 데이터가 존재하면
                temp_genres = self.meta[self.meta[ORIGINAL_TITLE_STR] == title][GENRES_STR].iloc(0)[0] # temp_genres에 장르데이터 저장

            # 장르 비교
            if len(input_genres) > 0: # 장르가 같으면 연관성 점수에 추가 점수 부여
                same_count = np.sum(np.isin(input_genres, temp_genres))
                cor += (genre_weight * same_count)

            # 줄거리 받아오기
            overview = self.meta[self.meta[ORIGINAL_TITLE_STR] == title][OVERVIEW_STR].iloc(0)[0] # ovew에 줄거리 데이터 저장

            if np.isnan(cor):
                continue
            else:
                result_dict = {TITLE_STR:title, SCORE_STR : cor, GENRES_STR : temp_genres, OVERVIEW_STR : overview}
                result.append(result_dict)

        return result