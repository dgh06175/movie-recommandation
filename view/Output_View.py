# Output_View : 화면에 어떤 것들을 출력하는 함수들을 모아둔 파일

# 상수 저장한 변수들
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
TITLE_STR = 'title'
SCORE_STR = 'score'
GENRES_STR = 'genres'
OVERVIEW_STR = 'overview'


# 프로그램 실행하자마자 처음 가이드 출력
def print_guide():
    print(DIVIDE_LINE)
    print(MOVIE_NUM_INPUT_GUIDE)
    print(DIVIDE_LINE + '\n')

# 유명한 영화 목록 출력
def print_famous_movies():
	for index in range(len(FAMOUS_MOVIE_NAMES)):
		print(f"{index + 1}. {FAMOUS_MOVIE_NAMES[index]}")

# 계산할때 로딩문구 출력
def printLoading():
    print(LOADING_TEXT)

# 결과값을 인자로 받고 최종 결과창 출력
def printResult(result):
    print(RESULT_GUIDE_TEXT)
    print("\n   {:<38} {:<7} {:<18} {:<60}".format('제목', '연관성', '장르', '줄거리'))
    for i in range(len(result)):
        title = result[i][TITLE_STR][:38]
        correlation = "{:.2f}".format(result[i][SCORE_STR])
        genre = result[i][GENRES_STR][0]
        if len(result[i][GENRES_STR])>=2:
            genre += f", {result[i][GENRES_STR][1]}"
        genre = genre[:20]
        overview = result[i][OVERVIEW_STR][:60]
        print("{:<1}. {:<40} {:<10} {:<20} {:<60}..".format(i + 1, title, correlation, genre, overview))
    print()
