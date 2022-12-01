from view import Output_View as Output
from view import Input_View as Input
from model import Calculate as ca

'''
main : 전체 프로그램을 실행하는 메인 함수를 저장한 파일

모두 직접 작성했다.
'''
# 전체 프로그램을 실행하는 메인 함수
def run():
    Output.print_guide() # 초기 화면 출력
    Output.print_famous_movies() # 유명 영화 10개 출력
    user_movie_numbers = Input.input_movies() # 사용자에게 유명 영화중에 몇개 입력받음
    genre_weight = Input.input_genre_importance() # 사용자에게 장르 유사성을 추천 알고리즘에 적용할것인지 입력받음
    result = ca.calculate_correlation(user_movie_numbers, genre_weight) # 상관관계 계산한 결과값 계산하여 상위 5개 result 변수에 저장
    Output.printResult(result) # 결과 출력

run()