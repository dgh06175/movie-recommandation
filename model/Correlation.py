import numpy as np
import pandas as pd
import json

class Correlation:
    # 5.0 : 어느정도 성공한 영화 10.0 : 꽤 성공한 영화 20.0 : 글로벌 히트작
    PUPULARITY_CUTLINE = 13.5
    # 0.0 ~ 10.0 전체 유저 평점의 평균
    VOTE_AVERAGE_CUTLINE = 6.0

    def __init__(self):
        self.meta = pd.read_csv('the-movies-dataset/movies_metadata.csv', low_memory=False)
        self.meta = self.meta[['id', 'original_title', 'original_language', 'genres', 'overview', 'popularity', 'vote_average']] # csv 파일에서 가져올 정보들.
        self.meta = self.meta.rename(columns={'id':'movieId'}) # id를 헷갈리지 않게 하기 위해 이름을 movieId로 변경
        self.meta = self.meta[self.meta['original_language'] == 'en'] # 영어로 된 영어들만 하기
        self.ratings = pd.read_csv('the-movies-dataset/ratings_small.csv')
        self.ratings = self.ratings[['userId', 'movieId', 'rating']]
        self.ratings.describe()
        self.meta.movieId = pd.to_numeric(self.meta.movieId, errors='coerce') # 숫자 문자열을을 숫자형식으로 변경
        self.ratings.movieId = pd.to_numeric(self.ratings.movieId, errors='coerce')  # 동일
        self.meta['genres'] = self.meta['genres'].apply(self.parse_genres)
        

    def getData(self):
        return pd.merge(self.ratings, self.meta, on='movieId', how='inner') # 메타 데이터와 별점 데이터를 합침


    def parse_genres(self, genres_str): # 장르 데이터 분석
        genres = json.loads(genres_str.replace('\'', '"'))
        genres_list = []
        for g in genres:
            genres_list.append(g['name'])
        return genres_list

    def pearsonR(self, s1, s2): # 피어슨 상관관계 계산식
        s1_c = s1 - s1.mean()
        s2_c = s2 - s2.mean()
        a = np.sum(s1_c * s2_c)
        b = np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))
        if b:
            return a / b
        else:
            return a / (b + 0.0000001)

    def recommend(self, input_movie, matrix, genre_weight): # 영화이름, 데이터, 장르를 연관성 점수에 반영할것인지 여부를 입력받는다.
        input_genres = self.meta[self.meta['original_title'] == input_movie]['genres'].iloc(0)[0] # 입력받은 영화의 장르 데이터 변수에 저장
        result = []
        for title in matrix.columns: # 모든 영화 데이터 검사
            if title == input_movie: # 입력받은 영화랑 같은 영화면 넘기기
                continue
            popularity = float(self.meta[self.meta['original_title'] == title]['popularity'].iloc(0)[0])
            vote_average = float(self.meta[self.meta['original_title'] == title]['vote_average'].iloc(0)[0])
            if popularity < self.PUPULARITY_CUTLINE:
                continue
            if vote_average < self.VOTE_AVERAGE_CUTLINE:
                continue

            # 별점 비교
            cor = self.pearsonR(matrix[input_movie], matrix[title]) # 피어슨 상관관계로 연관성 계산한 값을 cor에 저장
            if len(input_genres) > 0: # 장르 데이터가 존재하면
                temp_genres = self.meta[self.meta['original_title'] == title]['genres'].iloc(0)[0] # temp_genres에 장르데이터 저장

            # 장르 비교
            if len(input_genres) > 0: # 장르가 같으면 연관성 점수에 추가 점수 부여
                same_count = np.sum(np.isin(input_genres, temp_genres))
                cor += (genre_weight * same_count)

            # 줄거리 받아오기
            overview = self.meta[self.meta['original_title'] == title]['overview'].iloc(0)[0] # ovew에 줄거리 데이터 저장

            if np.isnan(cor):
                continue
            else:
                result_dict = {"title":title, "score" : cor, "genres" : temp_genres, "overview" : overview}
                result.append(result_dict)

        return result