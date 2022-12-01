from . import View_constant as STRING

'''
Input_View : 사용자에게 어떤 입력을 받을때 사용하는 함수들을 모아둔 파일

모두 직접 작성했다.
'''

# 사용자에게 유명 영화 목록중에 마음에 드는 영화들의 번호를 입력받고 그 값을 반환하는 함수
def input_movies():
	user_movie_numbers = list(map(int, input(STRING.MOVIE_INPUT_GUIDE).split()))
	return user_movie_numbers

# 사용자에게 장르의 유사도를 중요하게 생각하는지 아닌지 입력받고 그 값을 반환하는 함수
def input_genre_importance():
    genre_importance = input(STRING.GENRE_INPUT_GUIDE)
    if genre_importance == STRING.YES_CHAR:
        return STRING.GENRE_WEIGHT["HEAVY"]
    if genre_importance == STRING.NO_CHAR:
        return STRING.GENRE_WEIGHT["LIGHT"]
    else:
        return STRING.GENRE_WEIGHT["NORMAL"]