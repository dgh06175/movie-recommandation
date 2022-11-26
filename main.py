#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd
import json


# # Load Dataset

# In[2]:


meta = pd.read_csv('the-movies-dataset/movies_metadata.csv')

meta.head() # meta 5줄 미리보기


# In[3]:


meta = meta[['id', 'original_title', 'original_language', 'genres', 'overview']] # csv 파일에서 가져올 정보들.
meta = meta.rename(columns={'id':'movieId'}) # id를 헷갈리지 않게 하기 위해 이름을 movieId로 변경
meta = meta[meta['original_language'] == 'en'] # 영어로 된 영어들만 하기
meta.head()


# In[4]:


ratings = pd.read_csv('the-movies-dataset/ratings_small.csv')
ratings = ratings[['userId', 'movieId', 'rating']]
ratings.head()


# In[5]:


ratings.describe()


# # Refine Dataset

# In[6]:


meta.movieId = pd.to_numeric(meta.movieId, errors='coerce') # 숫자 문자열을을 숫자형식으로 변경
ratings.movieId = pd.to_numeric(ratings.movieId, errors='coerce')  # 동일


# In[7]:


def parse_genres(genres_str): # 장르 데이터 분석
    genres = json.loads(genres_str.replace('\'', '"'))
    
    genres_list = []
    for g in genres:
        genres_list.append(g['name'])

    return genres_list

meta['genres'] = meta['genres'].apply(parse_genres)

meta.head()


# # Merge Meta and Ratings

# In[8]:


data = pd.merge(ratings, meta, on='movieId', how='inner') # 메타 데이터와 별점 데이터를 합침

data.head()


# # Pivot Table

# In[9]:


matrix = data.pivot_table(index='userId', columns='original_title', values='rating') # 매트릭스 데이타를 만듦

matrix.head(20)


# # Pearson Correlation
# 
# https://namu.wiki/w/%EC%83%81%EA%B4%80%20%EA%B3%84%EC%88%98?from=%ED%94%BC%EC%96%B4%EC%8A%A8%20%EC%83%81%EA%B4%80%20%EA%B3%84%EC%88%98#s-2

# In[10]:


GENRE_WEIGHT = 0.1

def pearsonR(s1, s2): # 피어슨 상관관계 계산식
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    a = np.sum(s1_c * s2_c)
    b = np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))
    if b:
        return a / b
    else:
        return a / (b + 0.0000001)

def recommend(input_movie, matrix, n, similar_genre=True): # 영화이름, 데이터, 장르를 연관성 점수에 반영할것인지 여부를 입력받는다.
    input_genres = meta[meta['original_title'] == input_movie]['genres'].iloc(0)[0] # 입력받은 영화의 장르 데이터 변수에 저장

    result = []
    for title in matrix.columns: # 모든 영화 데이터 검사
        if title == input_movie: # 입력받은 영화랑 같은 영화면 넘기기
            continue

        # 별점 비교
        cor = pearsonR(matrix[input_movie], matrix[title]) # 피어슨 상관관계로 연관성 계산한 값을 cor에 저장
        if len(input_genres) > 0: # 장르 데이터가 존재하면
            temp_genres = meta[meta['original_title'] == title]['genres'].iloc(0)[0] # temp_genres에 장르데이터 저장

        # 장르 비교
        if similar_genre and len(input_genres) > 0: # 장르가 같으면 연관성 점수에 추가 점수 부여
            #temp_genres = meta[meta['original_title'] == title]['genres'].iloc(0)[0]

            same_count = np.sum(np.isin(input_genres, temp_genres))
            cor += (GENRE_WEIGHT * same_count)

        ######################################
        # 줄거리 받아오기
        ovew = meta[meta['original_title'] == title]['overview'].iloc(0)[0] # ovew에 줄거리 데이터 저장

        ######################################


        if np.isnan(cor):
            continue
        else:
            result.append((title, '{:.2f}'.format(cor), temp_genres, ovew)) # result 배열에 결과들 저장
            
    result.sort(key=lambda r: r[1], reverse=True) # 연관성 순서대로 정렬 하겠다. (내림차순)

    return result[:n]


# Prediction

# In[35]:


movie_name = input("재밌게 본 영화의 제목을 입력 하세요 : ")
movie_count = int(input("표시할 영화의 개수를 입력 하세요 (1~10) : "))
recommend_result = (recommend(movie_name, matrix, movie_count, similar_genre=True))
print(f"\n\n추천 하는 {movie_count}개의 영화 목록 입니다.")
# pd.DataFrame(recommend_results[0], columns = ['Title', 'Correlation', 'Genre'])
# print(recommend_result)


print("{:<48} {:<7} {:<18} {:<100}".format('제목', '연관성', '장르', '줄거리'))
for i in range(len(recommend_result)):
    title = recommend_result[i][0][:50]
    correlation = recommend_result[i][1][:10]
    genre = recommend_result[i][2][0][:20]
    overview = recommend_result[i][3][:98] + '..'
    print("{:<50} {:<10} {:<20} {:<100}".format(title, correlation, genre, overview))

