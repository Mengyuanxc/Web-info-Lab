import random

import pandas as pd
import numpy as np
import functions

data_path = "./data/book_score.csv"
cache_dir = "./data/book_cache/"

embedding = [0]
file = pd.read_csv(data_path)
for i in range(1, len(file)):
    embedding.append(1 - embedding[i - 1])
random.seed(0)
random.shuffle(embedding)

rating_matrix = functions.load_data_from_path(data_path, cache_dir=cache_dir, embedding=embedding)
user_similarity = functions.pearson_coefficient(rating_matrix, cache_dir, based="user")
item_similarity = functions.pearson_coefficient(rating_matrix, cache_dir, based="item")

rating = pd.read_csv(data_path, dtype={
    "User": np.int32, "Book": np.int32, "Rate": np.float32}, usecols=range(3))
rating_matrix_2 = pd.pivot_table(data=rating, index=["User"], columns=["Book"], values="Rate")


var_predict = 0
var_random_guess = 0
cnt = 0
for row in range(0, len(rating)):
    if embedding[row] == 1:
        predict_rating = functions.predict_score(rating.at[row, "User"], rating.at[row, "Book"], rating_matrix, user_similarity)
        random_guess_rating = random.randint(0, 6)
        real_rating = rating.at[row, "Rate"]
        cnt += 1
        var_predict += (predict_rating - real_rating) ** 2
        var_random_guess += (random_guess_rating - real_rating) ** 2
        if (cnt % 10 == 0):
            print(cnt, var_predict / cnt, var_random_guess / cnt)
var_predict = var_predict / cnt
var_random_guess = var_random_guess / cnt
print(var_predict, var_random_guess)
