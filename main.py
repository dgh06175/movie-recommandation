import numpy as np
import pandas as pd
import json
from view import Output_View as Output


meta = pd.read_csv('the-movies-dataset/movies_metadata.csv')

meta.head() # meta 5줄 미리보기

meta = meta[['id', 'original_title', 'original_language', 'genres', 'overview', 'popularity', 'vote_average']] # csv 파일에서 가져올 정보들.
meta = meta.rename(columns={'id':'movieId'}) # id를 헷갈리지 않게 하기 위해 이름을 movieId로 변경
meta = meta[meta['original_language'] == 'en'] # 영어로 된 영어들만 하기
meta.head()


ratings = pd.read_csv('the-movies-dataset/ratings_small.csv')
ratings = ratings[['userId', 'movieId', 'rating']]
ratings.head()


ratings.describe()
meta.movieId = pd.to_numeric(meta.movieId, errors='coerce') # 숫자 문자열을을 숫자형식으로 변경
ratings.movieId = pd.to_numeric(ratings.movieId, errors='coerce')  # 동일


def parse_genres(genres_str): # 장르 데이터 분석
    genres = json.loads(genres_str.replace('\'', '"'))
    
    genres_list = []
    for g in genres:
        genres_list.append(g['name'])

    return genres_list

meta['genres'] = meta['genres'].apply(parse_genres)

meta.head()


data = pd.merge(ratings, meta, on='movieId', how='inner') # 메타 데이터와 별점 데이터를 합침

data.head()


matrix = data.pivot_table(index='userId', columns='original_title', values='rating') # 매트릭스 데이타를 만듦

matrix.head(20)


# 5.0 : 어느정도 성공한 영화
# 10.0 : 꽤 성공한 영화
# 20.0 : 글로벌 히트작
PUPULARITY_CUTLINE = 13.5

# 0.0 ~ 10.0 전체 유저 평점의 평균
VOTE_AVERAGE_CUTLINE = 6.0


def pearsonR(s1, s2): # 피어슨 상관관계 계산식
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    a = np.sum(s1_c * s2_c)
    b = np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))
    if b:
        return a / b
    else:
        return a / (b + 0.0000001)

def recommend(input_movie, matrix, genre_weight): # 영화이름, 데이터, 장르를 연관성 점수에 반영할것인지 여부를 입력받는다.
    input_genres = meta[meta['original_title'] == input_movie]['genres'].iloc(0)[0] # 입력받은 영화의 장르 데이터 변수에 저장

    result = []
    for title in matrix.columns: # 모든 영화 데이터 검사
        if title == input_movie: # 입력받은 영화랑 같은 영화면 넘기기
            continue
        popularity = float(meta[meta['original_title'] == title]['popularity'].iloc(0)[0])
        vote_average = float(meta[meta['original_title'] == title]['vote_average'].iloc(0)[0])
        if popularity < PUPULARITY_CUTLINE:
            continue
        if vote_average < VOTE_AVERAGE_CUTLINE:
            continue

        # 별점 비교
        cor = pearsonR(matrix[input_movie], matrix[title]) # 피어슨 상관관계로 연관성 계산한 값을 cor에 저장
        if len(input_genres) > 0: # 장르 데이터가 존재하면
            temp_genres = meta[meta['original_title'] == title]['genres'].iloc(0)[0] # temp_genres에 장르데이터 저장

        # 장르 비교
        if len(input_genres) > 0: # 장르가 같으면 연관성 점수에 추가 점수 부여
            same_count = np.sum(np.isin(input_genres, temp_genres))
            cor += (genre_weight * same_count)

        # 줄거리 받아오기
        overview = meta[meta['original_title'] == title]['overview'].iloc(0)[0] # ovew에 줄거리 데이터 저장

        if np.isnan(cor):
            continue
        else:
            result_dict = {"title":title, "score" : cor, "genres" : temp_genres, "overview" : overview}
            result.append(result_dict)

    return result

def input_movies():
    print("#####################################################################################################")
    print("#  다음 영화들중에 재미있게 봤거나, 볼 생각이 있는 영화들의 번호를 공백으로 구분하여 입력해주세요.  #")
    print("#####################################################################################################\n")
    Output.print_famous_movies()
    print("\n입력 : ", end="")
    user_movie_numbers = list(map(int, input().split()))
    return user_movie_numbers

def input_genre_importance():
    print("\n비슷한 장르로 추천할까요? (Y/N) : ", end="")
    genre_importance = input()
    if genre_importance == 'Y':
        return 0.3
    if genre_importance == 'N':
        return 0.1
    else:
        return 0.11



def calculate_correlation (user_movie_numbers, genre_weight, matrix):
    recommand_results = []
    result = []
    printLoading()
    for movie_number in user_movie_numbers:
        movie_name = Output.FAMOUS_MOVIE_NAMES[movie_number - 1]
        recommand_results.append(recommend(movie_name, matrix, genre_weight))

    for recommand_result in recommand_results: # recommand_result = 고른 영화 하나에 대한 matrix안의 모든 영화의 연관성 정보
        for recommand_result_data in recommand_result: # recommand_result_data = 고른 영화와 연관성 정보를 도출한 하나의 영화 데이터
            is_data_in_result = False

            for index in range(len(result)):
                if recommand_result_data["title"] == result[index]["title"]:
                    is_data_in_result = True


            if not is_data_in_result:
                result.append(recommand_result_data)

            if is_data_in_result:
                for i in range(len(result)):
                    if result[i]["title"] == recommand_result_data["title"]:
                        result[i]["score"] += recommand_result_data["score"]
            
    result.sort(key = lambda x : x["score"], reverse=True)

    return result[:5]

def printLoading():
    print('\n계산 중입니다...')


def printResult(result):
    print(f"\n추천 하는 5개의 영화 목록 입니다.")
    print("\n   {:<38} {:<7} {:<18} {:<60}".format('제목', '연관성', '장르', '줄거리'))
    for i in range(len(result)):
        title = result[i]['title'][:38]
        correlation = "{:.2f}".format(result[i]['score'])
        genre = result[i]['genres'][0]
        if len(result[i]['genres'])>=2:
            genre += f", {result[i]['genres'][1]}"
        genre = genre[:20]
        overview = result[i]['overview'][:60]
        print("{:<1}. {:<40} {:<10} {:<20} {:<60}..".format(i + 1, title, correlation, genre, overview))
    print()


def run(matrix):
    user_movie_numbers = input_movies()
    genre_weight = input_genre_importance()
    result = calculate_correlation(user_movie_numbers, genre_weight, matrix)
    printResult(result)

run(matrix)