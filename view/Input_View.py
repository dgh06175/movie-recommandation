# Input_View : 사용자에게 어떤 입력을 받을때 사용하는 함수들을 모아둔 파일

# 상수 저장한 변수들
MOVIE_INPUT_GUIDE = "\n입력 : "
GENRE_INPUT_GUIDE = "\n비슷한 장르로 추천할까요? (Y/N) : "
YES_CHAR = 'Y'
NO_CHAR = 'N'
EMPTY = ''
GENRE_WEIGHT = {
	"HEAVY" : 0.3,
	"NORMAL" : 0.15,
	"LIGHT" : 0.1
} # 장르 중요성 가산 점수들


# 사용자에게 유명 영화 목록중에 마음에 드는 영화들의 번호를 입력받고 그 값을 반환하는 함수
def input_movies():
	user_movie_numbers = list(map(int, input(MOVIE_INPUT_GUIDE).split()))
	return user_movie_numbers

# 사용자에게 장르의 유사도를 중요하게 생각하는지 아닌지 입력받고 그 값을 반환하는 함수
def input_genre_importance():
    genre_importance = input(GENRE_INPUT_GUIDE)
    if genre_importance == YES_CHAR:
        return GENRE_WEIGHT["HEAVY"]
    if genre_importance == NO_CHAR:
        return GENRE_WEIGHT["LIGHT"]
    else:
        return GENRE_WEIGHT["NORMAL"]