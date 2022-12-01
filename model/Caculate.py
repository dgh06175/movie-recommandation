from view import Output_View as Output
from model import Correlation as co
from . import Model_constant as STRING

'''
Calculate : 유저가 선택한 영화들을 Correlation 클래스로 계산하여 도출한 결과값들로 상관관계가 가장 높게 나온 5개의 영화를 반환하는 함수를 저장한 파일

18줄 matrix 변수에 평점 데이터를 가져오는 줄을 제외하고 모두 직접 작성했다.
'''

# Correlation 파일안의 Correlation 클래스를 이용하여 상관관계를 계산하여 상관관계가 높은 5개의 영화를 반환하는 함수
def calculate_correlation (user_movie_numbers, genre_weight):
    recommand_results = []
    result = []
    Output.printLoading()
    pearson = co.Correlation()
    data = pearson.getData()
    matrix = data.pivot_table(index=STRING.USERID, columns=STRING.ORIGINAL_TITLE, values=STRING.RATING) # 매트릭스 데이타를 만듦
    for movie_number in user_movie_numbers:
        movie_name = STRING.FAMOUS_MOVIE_NAMES[movie_number - 1]
        recommand_results.append(pearson.recommend(movie_name, matrix, genre_weight))

    for recommand_result in recommand_results: # recommand_result = 고른 영화 하나에 대한 matrix안의 모든 영화의 연관성 정보
        for recommand_result_data in recommand_result: # recommand_result_data = 고른 영화와 연관성 정보를 도출한 하나의 영화 데이터
            is_data_in_result = False

            for index in range(len(result)):
                if recommand_result_data[STRING.TITLE] == result[index][STRING.TITLE]:
                    is_data_in_result = True


            if not is_data_in_result:
                result.append(recommand_result_data)

            if is_data_in_result:
                for i in range(len(result)):
                    if result[i][STRING.TITLE] == recommand_result_data[STRING.TITLE]:
                        result[i][STRING.SCORE] += recommand_result_data[STRING.SCORE]
            
    result.sort(key = lambda x : x[STRING.SCORE], reverse=True)

    return result[:5]