# Movie Recommendation

    OTT 사이트를 처음 들어갔을 때 유명한 영화 목록들을 보여주고 사용자가 재미있게 봤거나 보고싶은 영화들을 고르면
    고른 영화들과 관련성이 높은 영화들을 보여주는 것을 프로그램으로 구현했다.

- 기능 목록

  - 입력

    - [x] 유명한 영화 10개를 출력하고, 볼 생각이 있거나 재미있게 본 영화들을 골라달라고 출력한다.
    - [x] 장르의 유사정도를 얼마나 중요하게 생각하는지 입력받는다. (1~5점).

  - 계산

    - [x] 피어슨 알고리즘을 이용하여 관련성을 계산한다.
    - [x] 각 영화별로 (관련성 X 사용자의 평점)을 총합해서 계산한다.

  - 출력

    - [x] 계산한 값이 가장 높은 5개의 영화 목록을 출력한다.

  - 예외 처리
    - [ ] 입력받을때, 쉼표를 넣었거나 같은 번호를 여러개 넣어도 정상작동 하도록 처리하기
  - 적용할 유명한 영화 목록
    Fight Club
    Iron Man
    The Dark Knight
    Forrest Gump
    The Matrix
    Pirates of the Caribbean: The Curse of the Black Pearl
    Star Wars
    Twilight
    Spider-Man 3
    Titanic
