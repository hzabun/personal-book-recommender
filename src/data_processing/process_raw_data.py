import isbnlib
import pandas as pd

ratings_df = pd.read_csv("data/raw/BX-Book-Ratings.csv", delimiter=";")
books_df = pd.read_csv("data/raw/BX-Books.csv", delimiter=";", escapechar="\\")

books_df.drop(["Image-URL-S", "Image-URL-M", "Image-URL-L"], axis=1, inplace=True)
ratings_df.columns = ["user_id", "isbn", "book_rating"]
books_df.columns = [
    "isbn",
    "book_title",
    "book_author",
    "publication_year",
    "publisher",
]

ratings_df["isbn"] = ratings_df["isbn"].apply(isbnlib.canonical)
books_df["isbn"] = books_df["isbn"].apply(isbnlib.canonical)

ratings_df = ratings_df[ratings_df["isbn"] != ""]
books_df = books_df[books_df["isbn"] != ""]

ratings_df = ratings_df.drop_duplicates(subset=["user_id", "isbn"], keep=False)
books_df = books_df.drop_duplicates(subset=["isbn"])

user_book_ratings = ratings_df.merge(right=books_df, how="left")

ratings_df.to_csv("data/processed/ratings.csv", index=False)
books_df.to_csv("data/processed/books.csv", index=False)
user_book_ratings.to_csv("data/processed/user_book_ratings.csv", index=False)
