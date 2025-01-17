# -*- coding: utf-8 -*-
"""Copy of fcc_book_recommendation_knn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qX2oFk6EovAdpNO2F34nw1alaULqAvBN
"""

# import libraries (you may add additional imports but you may not have to)
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# get data files


books_filename = 'BX-Books.csv'
ratings_filename = 'BX-Book-Ratings.csv'

# import csv data into dataframes
df_books = pd.read_csv(
    books_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['isbn', 'title', 'author'],
    usecols=['isbn', 'title', 'author'],
    dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})

df_ratings = pd.read_csv(
    ratings_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['user', 'isbn', 'rating'],
    usecols=['user', 'isbn', 'rating'],
    dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})

# add your code here - consider creating a new cell for each section of code
print(df_ratings.head())
print(df_books.head())
df_books['title'] = df_books['title'].str.lower()
df_books['author'] = df_books['author'].str.lower()

df = df_ratings.merge(df_books, on='isbn', how = 'left')
print(df.loc[1])

c = df.groupby(['user']).size()>=20
d = df.groupby(['isbn']).size()>=10
df_ratings = df_ratings[df.user.isin(c[c].index)]
df = df[df.isbn.isin(d[d].index)]
df = df.drop_duplicates(['user', 'isbn'])
df = df.dropna()
print(df.head())



book_df = df.pivot_table(index = 'title', columns = 'user', values = 'rating', fill_value=0)
print(book_df.head())
print(book_df.shape)

nn = NearestNeighbors(metric='cosine')

nn.fit(csr_matrix(book_df.values))

# function to return recommended books - this will be tested
def get_recommends(book = ""):
  recommended_books = []
  distance, book_names = nn.kneighbors([book_df.loc[book]], n_neighbors=6, return_distance = True)
  recommended_books.append(book)
  #print(book_names)
  e=[]

  for i in range(1,6):
    e.append([book_df.iloc[book_names[0][i]].name, distance[0][i]])
  recommended_books.append(e)

  return recommended_books

def search_author(authors = ""):
    auth = df_books[df_books["author"] == authors]
    print(auth["title"])

while True:
    book = input("Enter a book title: ")
    try:
        books = get_recommends(book.lower())
        print(books)
    except:
        print("Book not found in the dataset.")
        opt = input("Search author?").lower()
        if opt == 'yes':
            author = input("Enter an author's name: ")
            search_author(author)








