MOVIE_INPUT_GUIDE = "\n입력 : "
GENRE_INPUT_GUIDE = "\n비슷한 장르로 추천할까요? (Y/N) : "
YES_CHAR = 'Y'
NO_CHAR = 'N'
EMPTY = ''
GENRE_WEIGHT = {
	"HEAVY" : 0.3,
	"NORMAL" : 0.15,
	"LIGHT" : 0.1
}

def input_movies():
	user_movie_numbers = list(map(int, input(MOVIE_INPUT_GUIDE).split()))
	return user_movie_numbers


def input_genre_importance():
    genre_importance = input(GENRE_INPUT_GUIDE)
    if genre_importance == YES_CHAR:
        return GENRE_WEIGHT["HEAVY"]
    if genre_importance == NO_CHAR:
        return GENRE_WEIGHT["LIGHT"]
    else:
        return GENRE_WEIGHT["NORMAL"]