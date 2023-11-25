#!/usr/bin/env python
# coding: utf-8

# # Movie Recommendation

# ## Call Data

# In[25]:


import pandas as pd
import numpy as np
import json


# In[26]:


movies = pd.read_csv('C:/Users/user/Desktop/기계학습 데이터분석/tmdb_5000_movies.csv')
credits = pd.read_csv('C:/Users/user/Desktop/기계학습 데이터분석/tmdb_5000_credits.csv')


# In[27]:


movies.head()


# In[28]:


movies.describe()


# In[29]:


credits.head()


# In[30]:


credits.describe()


# ## Data Cleaning

# In[31]:


movies['genres'] = movies['genres'].apply(json.loads)
for index, row in movies.iterrows():
    genre_list = [genre['name'] for genre in row['genres']]
    movies.at[index, 'genres'] = str(genre_list)


# In[32]:


movies['keywords'] = movies['keywords'].apply(json.loads)
for index, row in movies.iterrows():
    keywords_list = [keywords['name'] for keywords in row['keywords']]
    movies.at[index, 'keywords'] = str(keywords_list)


# In[33]:


credits['cast'] = credits['cast'].apply(json.loads)
for index, row in credits.iterrows():
    cast_list = [cast['character'] for cast in row['cast']]
    credits.at[index, 'cast'] = str(cast_list)


# In[34]:


credits['crew'] = credits['crew'].apply(json.loads)
def get_directors(x):
    directors = [crew['name'] for crew in x if crew['job'] == 'Director']
    return directors
credits['crew'] = credits['crew'].apply(get_directors)
credits.rename(columns={'crew':'director'},inplace=True)


# In[35]:


movies = movies.merge(credits,left_on='id',right_on='movie_id',how='left')
movies = movies[['id','original_title','genres','cast','vote_average','director','keywords']]
movies.head()


# In[36]:


new_id = list(range(0,movies.shape[0]))
movies['new_id'] = new_id
movies = movies[['new_id','original_title','genres','cast','vote_average','director','keywords']]
movies.head()


# ## Working with the Genres column

# In[37]:


movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['genres'] = movies['genres'].str.split(',')
movies.head()


# In[38]:


for i,j in zip(movies['genres'],movies.index):
    list2=[]
    list2=i
    list2.sort()
    movies.loc[j,'genres']=str(list2)
movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['genres'] = movies['genres'].str.split(',')


# In[39]:


genreList = []
for index, row in movies.iterrows():
    genres = row["genres"]
    
    for genre in genres:
        if genre not in genreList:
            genreList.append(genre)
genreList[:10]


# ### One Hot Encoding for multiple labels

# In[40]:


def binary(genre_list):
    binaryList = []
    
    for genre in genreList:
        if genre in genre_list:
            binaryList.append(1)
        else:
            binaryList.append(0)
    
    return binaryList


# In[41]:


movies['genres_bin'] = movies['genres'].apply(lambda x: binary(x))
movies['genres_bin'].head()


# ## Working with Director column

# In[42]:


def xstr(s):
    if s is None:
        return ''
    return str(s)
movies['director'] = movies['director'].apply(xstr)


# In[44]:


directorList=[]
for i in movies['director']:
    if i not in directorList:
        directorList.append(i)


# In[45]:


def binary(director_list):
    binaryList = []  
    for direct in directorList:
        if direct in director_list:
            binaryList.append(1)
        else:
            binaryList.append(0)
    return binaryList


# In[46]:


movies['director_bin'] = movies['director'].apply(lambda x: binary(x))
movies.head()


# In[ ]:




