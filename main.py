from view import Output_View as Output
from view import Input_View as Input
from model import calculate as ca

# 전체 프로그램을 실행하는 메인 함수
def run():
    Output.print_guide()
    Output.print_famous_movies()
    user_movie_numbers = Input.input_movies()
    genre_weight = Input.input_genre_importance()
    result = ca.calculate_correlation(user_movie_numbers, genre_weight)
    Output.printResult(result)

run()