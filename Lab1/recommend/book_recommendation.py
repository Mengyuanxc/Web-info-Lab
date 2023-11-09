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
user_ids = []
pred_ratings = []
real_ratings = []
random_guess_ratings = []
for row in range(0, len(rating)):
    if embedding[row] == 1:
        user_id = rating.at[row, "User"]
        book_id = rating.at[row, "Book"]
        real_rating = rating.at[row, "Rate"]
        predict_rating = functions.predict_score(user_id, book_id, rating_matrix, user_similarity)
        random_guess_rating = random.randint(0, 6)
        cnt += 1
        user_ids.append(user_id)
        pred_ratings.append(predict_rating)
        real_ratings.append(real_rating)
        random_guess_ratings.append(random_guess_rating)
        var_predict += (predict_rating - real_rating) ** 2
        var_random_guess += (random_guess_rating - real_rating) ** 2
        if cnt % 10 == 0:
            print(cnt, var_predict / cnt, var_random_guess / cnt)
        # if cnt == 10000:
        #     break
var_predict = var_predict / cnt
var_random_guess = var_random_guess / cnt
print(var_predict, var_random_guess)

results = []
user_ids_np = np.array(user_ids).reshape(-1, 1)
pred_ratings_np = np.array(pred_ratings).reshape(-1, 1)
real_ratings_np = np.array(real_ratings).reshape(-1, 1)
random_guess_ratings_np = np.array(random_guess_ratings).reshape(-1, 1)
predict_result = np.column_stack((user_ids_np, pred_ratings_np, real_ratings_np))
random_guess_result = np.column_stack((user_ids_np, random_guess_ratings_np, real_ratings_np))

results.append(predict_result)
results = np.vstack(results)
results_df = pd.DataFrame(results, columns=['user', 'pred', 'true'])
results_df['user'] = results_df['user'].astype(int)
ndcg_scores = results_df.groupby("user").apply(functions.compute_ndcg)
avg_ndcg = ndcg_scores.mean()
print(f"Predict average NDCG: {avg_ndcg}")

results = []
results.append(random_guess_result)
results = np.vstack(results)
results_df = pd.DataFrame(results, columns=['user', 'pred', 'true'])
results_df['user'] = results_df['user'].astype(int)
ndcg_scores = results_df.groupby("user").apply(functions.compute_ndcg)
avg_ndcg = ndcg_scores.mean()
print(f"Random guess average NDCG: {avg_ndcg}")

