FAMOUS_MOVIE_NAMES = [
    "Fight Club",
    "Iron Man",
    "The Dark Knight",
    "Forrest Gump",
    "The Matrix",
    "Pirates of the Caribbean: The Curse of the Black Pearl",
    "Star Wars",
    "Twilight",
    "Spider-Man 3",
    "Titanic"
]
DIVIDE_LINE = '#' * 101
MOVIE_NUM_INPUT_GUIDE = "#  다음 영화들중에 재미있게 봤거나, 볼 생각이 있는 영화들의 번호를 공백으로 구분하여 입력해주세요.  #"
LOADING_TEXT = '\n계산 중입니다...'
RESULT_GUIDE_TEXT = "\n추천 하는 5개의 영화 목록 입니다."
FIRST_ROW_OF_RESULT = "\n   {:<38} {:<7} {:<18} {:<60}".format('제목', '연관성', '장르', '줄거리')

def print_guide():
    print(DIVIDE_LINE)
    print(MOVIE_NUM_INPUT_GUIDE)
    print(DIVIDE_LINE + '\n')


def print_famous_movies():
	for index in range(len(FAMOUS_MOVIE_NAMES)):
		print(f"{index + 1}. {FAMOUS_MOVIE_NAMES[index]}")


def printLoading():
    print(LOADING_TEXT)


def printResult(result):
    print(RESULT_GUIDE_TEXT)
    print(FIRST_ROW_OF_RESULT)
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
