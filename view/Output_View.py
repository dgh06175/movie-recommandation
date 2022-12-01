from . import View_constant as STRING

'''
Output_View : 화면에 어떤 것들을 출력하는 함수들을 모아둔 파일

모두 직접 작성했다.
'''

# 프로그램 실행하자마자 처음 가이드 출력
def print_guide():
    print(STRING.DIVIDE_LINE)
    print(STRING.MOVIE_NUM_INPUT_GUIDE)
    print(STRING.DIVIDE_LINE + '\n')

# 유명한 영화 목록 출력
def print_famous_movies():
	for index in range(len(STRING.FAMOUS_MOVIE_NAMES)):
		print(f"{index + 1}. {STRING.FAMOUS_MOVIE_NAMES[index]}")

# 계산할때 로딩문구 출력
def printLoading():
    print(STRING.LOADING_TEXT)

# 결과값을 인자로 받고 최종 결과창 출력
def printResult(result):
    print(STRING.RESULT_GUIDE_TEXT)
    print("\n   {:<38} {:<7} {:<18} {:<60}".format('제목', '연관성', '장르', '줄거리'))
    for i in range(len(result)):
        title = result[i][STRING.TITLE][:38]
        correlation = "{:.2f}".format(result[i][STRING.SCORE])
        genre = result[i][STRING.GENRES_STR][0]
        if len(result[i][STRING.GENRES_STR])>=2:
            genre += f", {result[i][STRING.GENRES_STR][1]}"
        genre = genre[:20]
        overview = result[i][STRING.OVERVIEW_STR][:60]
        print("{:<1}. {:<40} {:<10} {:<20} {:<60}..".format(i + 1, title, correlation, genre, overview))
    print()
