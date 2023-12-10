"""
第一步,将知识图谱映射到从0到n的范围内
"""

import gzip
from tqdm import tqdm
import json
import pandas as pd

movie_triplet_dict = None

with open("../stage 1/output/sampled_3step_triplets.json", "r") as f:
    movie_triplet_dict = json.load(f)

midToIdmap = {}
"""
将Mid映射到0——movie_num
"""
# 获取midToIdmap
# 总共有两层映射：mid->id->0——movie_num
with open("data/douban2fb.txt", "r") as f:
    for line in f:
        line = line.strip()
        # print(line)
        convert_list = line.split("\t")
        midToIdmap[convert_list[1]] = convert_list[0]
Idmap = {}  # Id->0——movie_num
with open("data/movie_id_map.txt", "r") as f:
    for line in f:
        line = line.strip()
        # print(line)
        convert_list = line.split("\t")
        Idmap[convert_list[0]] = convert_list[1]
for key in midToIdmap:
    midToIdmap[key] = Idmap[midToIdmap[key]]

# print(midToIdmap)

# 找出所有涉及到的entity
non_movie_cnt = 578  # 其他实体从578开始映射起
non_movie_map = {}  # 非电影实体到数字的映射表

relationship_cnt = 0  # 关系的种类数
relationship_map = {}  # 关系到数字的映射表

movie_cnt = 0
cnt = 0

triplets_columns = []
"""
映射后的三元组
"""
for movie in movie_triplet_dict:
    # 头的映射
    cnt += 1
    triplet = []
    movie_str = movie[0][28:-1]
    if movie_str in midToIdmap:  # 构造映射
        movie_id = midToIdmap[movie_str]
        triplet.append(int(movie_id))
        movie_cnt += 1
    else:
        if movie[0] in non_movie_map:  # 在表中了
            triplet.append(non_movie_map[movie[0]])
        else:  # 不在映射表里
            non_movie_map[movie[0]] = non_movie_cnt
            triplet.append(non_movie_cnt)
            non_movie_cnt += 1

    # 关系的映射
    if movie[1] in relationship_map:  # 在表中了
        triplet.append(relationship_map[movie[1]])
    else:  # 不在映射表里
        relationship_map[movie[1]] = relationship_cnt
        triplet.append(relationship_cnt)
        relationship_cnt += 1

    # 尾的映射
    movie_str = movie[2][28:-1]
    if movie_str in midToIdmap:  # 构造映射
        movie_id = midToIdmap[movie_str]
        triplet.append(int(movie_id))
        movie_cnt += 1
    else:
        if movie[2] in non_movie_map:  # 在表中了
            triplet.append(non_movie_map[movie[2]])
        else:  # 不在映射表里
            non_movie_map[movie[2]] = non_movie_cnt
            triplet.append(non_movie_cnt)
            non_movie_cnt += 1
    triplets_columns.append(triplet)

print(movie_cnt)
print(relationship_cnt)
print(non_movie_cnt)
# 结果写入文件中
triplet_csv = pd.DataFrame(triplets_columns)
triplet_csv.to_csv("given_code\data\Douban\kg_final.csv", header=None)
