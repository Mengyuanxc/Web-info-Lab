"""
第一步,将知识图谱映射到从0到n的范围内
"""

import gzip
from tqdm import tqdm
import json
import pandas as pd

Core = 15
relation = 50

movie_triplet_dict = None

with open("output/sampled_2step_triplets.json", "r") as f:
    movie_triplet_dict = json.load(f)

#统计每一个实体、关系出现次数
entity_map = {}
relationship_map = {}
triplets_columns = []
"""
映射后的三元组
"""
for movie in movie_triplet_dict:
    #头的映射
    if movie[0] in entity_map:       #在表中了
        entity_map[movie[0]] += 1
    else:       #不在映射表里
        entity_map[movie[0]] = 1

    #关系的映射
    if movie[1] in relationship_map:       #在表中了
        relationship_map[movie[1]] += 1
    else:       #不在映射表里
        relationship_map[movie[1]] = 1

    if movie[2] in entity_map:       #在表中了
        entity_map[movie[2]] += 1
    else:       #不在映射表里
        entity_map[movie[2]] = 1

modify_triplets = []
for movie in movie_triplet_dict:
    if(entity_map[movie[0]]<Core or entity_map[movie[2]]<Core or relationship_map[movie[1]]<relation):
        pass
    else:
        modify_triplets.append(movie)

print(len(modify_triplets))
with open("output/sampled_3step_triplets.json", "w") as f:
    json_str = json.dumps(modify_triplets)
    f.write(json_str)

