import os
import random
import pandas as pd
import numpy as np
from pprint import pprint

DATA_PATH="./data/movie_score.csv"
CACHE_DIR="./data/movie_cache/"

#分出测试集
Embedding = [0]
get_len = pd.read_csv(DATA_PATH)
for i in range(1,len(get_len)):
    Embedding.append(1 - Embedding[i-1])
random.seed(0)
random.shuffle(Embedding)

def load_data(data_path):
    '''
    加载数据
    :param  data_path:数据集路径
    :param  cache_path:数据集缓存路径
    :return  用户-物品评分矩阵
    '''
    #数据集缓存地址
    cache_path=os.path.join(CACHE_DIR, "ratings_matrix_cache")

    print("开始加载数据集...")
    if os.path.exists(cache_path):  #判断是否存在缓存文件
        print("加载缓存中...")
        ratings_matrix=pd.read_pickle(cache_path)
        print("从缓存加载数据集完毕")
    else:
        print("加载新数据中...")
        #设置要加载的数据字段的类型
        dtype={"User": np.int32, "Movie": np.int32, "Rate": np.float32}
        #加载数据，我们只用前三列数据，分别是用户ID、电影ID、以及用户对电影的对应评分
        ratings=pd.read_csv(DATA_PATH, dtype=dtype, usecols=range(3))
        #设置Embedding掩盖数组
        for row in range(0,len(ratings)):
            if Embedding[row] == 1:
                ratings.at[row, "Rate"] = None
        #透视表，将电影ID转换为列名称，转换成为一个User-Movie的评分矩阵
        ratings_matrix = pd.pivot_table(data=ratings, index=["User"], columns=["Movie"], values="Rate")
        #存入缓存文件
        ratings_matrix.to_pickle(cache_path)
        print("数据集加载完毕")
    return ratings_matrix

def compute_persion_similarity(ratings_matrix, based="user"):
    '''
    计算皮尔逊相关系数
    :param  ratings_matrix:用户物品评分矩阵
    :param  based: "user" or "item"
    :return: 相似度矩阵
    '''
    user_similarity_cache_path=os.path.join(CACHE_DIR, "user_similarity_cache")
    item_similarity_cache_path=os.path.join(CACHE_DIR, "item_similarity_cache")
    #基于皮尔逊相关系数计算相似度
    #用户相似度
    if based=="user":
        if os.path.exists(user_similarity_cache_path):
            print("正从缓存加载用户相似度矩阵")
            similarity=pd.read_pickle(user_similarity_cache_path)
        else:
            print("开始计算用户相似度矩阵")
            similarity=ratings_matrix.T.corr()
            similarity.to_pickle(user_similarity_cache_path)
    elif based=="item":
        if os.path.exists(item_similarity_cache_path):
            print("正从缓存加载物品相似度矩阵")
            similarity=pd.read_pickle(item_similarity_cache_path)
        else:
            print("开始计算物品相似度矩阵")
            similarity=ratings_matrix.corr()
            similarity.to_pickle(item_similarity_cache_path)
    else:
        raise Exception("Unhandled 'based' value: %s"%based)
    print("相似度矩阵计算/加载完毕")
    return similarity

def predict_userBasedCF(uid, iid, ratings_matrix, user_similar):
    '''
    预测给定用户对给定物品的评分值
    :param uid:用户id
    :param iid:物品id
    :param ratings_matrix:用户-物品评分矩阵
    :param user_similar:用户两两相似度矩阵
    :return:预测的评分值
    '''
    #1.找出uid用户的相似用户
    similar_users=user_similar[uid].drop([uid]).dropna()
    #相似用户筛选规则：正相关的用户
    similar_users=similar_users.where(similar_users>0).dropna()
    if similar_users.empty is True:
        return 2.5
        raise Exception("用户{}没有相似的用户".format(uid))

    #2.从uid用户的相邻用户中筛选出对iid物品有评分记录的近邻用户
    ids=set(ratings_matrix[iid].dropna().index)&set(similar_users.index)
    finally_similar_users=similar_users.loc[list(ids)]

    #3.结合uid用户与其近邻用户的相似度预测uid用户对iid用户的评分
    sum_up=0    #评分预测部分的分子部分的值
    sum_down=0   #评分预测部分的分母部分的值
    for sim_uid in finally_similar_users.index:
        similarity = finally_similar_users[sim_uid]
        #近邻用户的评分数据
        sim_user_rated_movies=ratings_matrix.loc[sim_uid].dropna()
        #近邻用户对iid物品的评分
        sim_user_rating_for_item=sim_user_rated_movies[iid]
        #计算分子的值
        sum_up+=similarity * sim_user_rating_for_item
        #计算分母的值
        sum_down+=similarity

    #计算预测的评分并返回
    predict_rating=sum_up/sum_down
    #print("预测出用户{0}对电影{1}的评分为：{2:.2f}".format(uid, iid, predict_rating))
    return round(predict_rating, 2)

#获取某一项评分
def get_predict(uid, item_id, ratings_matrix, user_similar):
    return predict_userBasedCF(uid, item_id ,ratings_matrix, user_similar)

ratings_matrix=load_data(DATA_PATH)
user_similar=compute_persion_similarity(ratings_matrix, based="user")
item_similar=compute_persion_similarity(ratings_matrix, based="item")
#print(ratings_matrix)
#print(user_similar)
#print(item_similar)



#开始计算准确率
print("开始计算预测准确率...")
#设置要加载的数据字段的类型
dtype={"User": np.int32, "Movie": np.int32, "Rate": np.float32}
#加载数据，我们只用前三列数据，分别是用户ID、电影ID、以及用户对电影的对应评分
ratings_2=pd.read_csv(DATA_PATH, dtype=dtype, usecols=range(3))
#透视表，将电影ID转换为列名称，转换成为一个User-Movie的评分矩阵
ratings_matrix_2 = pd.pivot_table(data=ratings_2, index=["User"], columns=["Movie"], values="Rate")

Var = 0 #方差
Var_2 = 0 #瞎猜的方差
cnt = 0 #计数
for row in range(0, len(ratings_2)):
    if Embedding[row] == 1:       #为测试数据
        #预测的分数
        predict_rating = get_predict(ratings_2.at[row, "User"], ratings_2.at[row, "Movie"], ratings_matrix, user_similar)
        #瞎猜的分数
        guess_rating = random.randint(0,6)
        #实际的分数
        real_rating = ratings_2.at[row, "Rate"]
        cnt += 1
        Var += (predict_rating-real_rating)**2
        Var_2 += (guess_rating-real_rating)**2
        if(cnt % 10 == 0):
            print(cnt, Var/cnt, Var_2/cnt)
Var = Var / cnt
Var_2 = Var_2 /cnt
print(Var, Var_2)

