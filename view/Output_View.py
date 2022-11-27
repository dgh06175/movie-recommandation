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

def print_famous_movies():
	for index in range(len(FAMOUS_MOVIE_NAMES)):
		print(f"{index + 1}. {FAMOUS_MOVIE_NAMES[index]}")