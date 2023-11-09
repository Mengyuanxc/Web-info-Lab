import os
import random
import pandas as pd
import numpy as np
from sklearn.metrics import ndcg_score


def load_data_from_path(data_path, embedding, cache_dir):
    cache_path = os.path.join(cache_dir, "ratings_matrix_cache")

    # 加载数据集
    if os.path.exists(cache_path):
        ratings_matrix = pd.read_pickle(cache_path)
    else:
        ratings = pd.read_csv(data_path, dtype={
            "User": np.int32, "Book": np.int32, "Rate": np.float32
        }, usecols=range(3))
        length = len(ratings)
        for row in range(0, length):
            if embedding[row] == 1:
                ratings.at[row, "Rate"] = None
        ratings_matrix = pd.pivot_table(
            data=ratings, index=["User"], columns=["Book"], values="Rate")
        ratings_matrix.to_pickle(cache_path)

    return ratings_matrix

def pearson_coefficient(rating_matrix, cache_dir, based="user"):
    user_cache_path = os.path.join(cache_dir, "user_cache")
    item_cache_path = os.path.join(cache_dir, "item_cache")
    if based == "user":
        if os.path.exists(user_cache_path):
            similarity = pd.read_pickle(user_cache_path)
        else:
            similarity = rating_matrix.T.corr()
            similarity.to_pickle(user_cache_path)
    elif based == "item":
        if(os.path.exists(item_cache_path)):
            similarity = pd.read_pickle(item_cache_path)
        else:
            similarity = rating_matrix.corr()
            similarity.to_pickle(item_cache_path)
    else:
        print("base value error!")
        exit(0)
    return similarity

def predict_score(user_id, item_id, rating_matrix, user_similarity_matrix):
    # 寻找相关的用户
    relevant_users = user_similarity_matrix[user_id].drop([user_id]).dropna()
    relevant_users = relevant_users.where(relevant_users > 0).dropna()
    if relevant_users.empty is True: # 没有相关的用户，直接返回平均值
        return 2.5
    # 寻找跟item_id相关的用户
    ids = set(rating_matrix[item_id].dropna().index) & set(relevant_users.index)
    relevant_users = relevant_users.loc[list(ids)]
    # 预测评分
    numerator = 0
    denominator = 0
    for uid in relevant_users.index:
        similarity = relevant_users[uid]
        item_rating = rating_matrix.loc[uid].dropna()[item_id]
        numerator += similarity * item_rating
        denominator += similarity

    if denominator != 0:
        final_rating = numerator / denominator
    else:
        final_rating = 2.5
    return round(final_rating, 2)


def compute_ndcg(group):
    true_ratings = group['true'].tolist()
    pred_ratings = group['pred'].tolist()
    return ndcg_score([true_ratings], [pred_ratings], k=50)


