from view import Output_View as Output
from model import Correlation as co

TITLE_STR = 'title'
USER_ID_STR = 'userId'
COLUMN_STR = 'original_title'
VALUES_STR = 'rating'
SCORE_STR = 'score'

def calculate_correlation (user_movie_numbers, genre_weight):
    recommand_results = []
    result = []
    Output.printLoading()
    pearson = co.Correlation()
    data = pearson.getData()
    matrix = data.pivot_table(index=USER_ID_STR, columns=COLUMN_STR, values=VALUES_STR) # 매트릭스 데이타를 만듦
    for movie_number in user_movie_numbers:
        movie_name = Output.FAMOUS_MOVIE_NAMES[movie_number - 1]
        recommand_results.append(pearson.recommend(movie_name, matrix, genre_weight))

    for recommand_result in recommand_results: # recommand_result = 고른 영화 하나에 대한 matrix안의 모든 영화의 연관성 정보
        for recommand_result_data in recommand_result: # recommand_result_data = 고른 영화와 연관성 정보를 도출한 하나의 영화 데이터
            is_data_in_result = False

            for index in range(len(result)):
                if recommand_result_data[TITLE_STR] == result[index][TITLE_STR]:
                    is_data_in_result = True


            if not is_data_in_result:
                result.append(recommand_result_data)

            if is_data_in_result:
                for i in range(len(result)):
                    if result[i][TITLE_STR] == recommand_result_data[TITLE_STR]:
                        result[i][SCORE_STR] += recommand_result_data[SCORE_STR]
            
    result.sort(key = lambda x : x[SCORE_STR], reverse=True)

    return result[:5]