import json

# 第一次筛选
# original_dict: extract.py得到的字典
original_dict = None
# 采样：20核
entity_core = 20
# 关系数阈值：50
relationship_threshold = 50

with open("movie_triplet_dict.json", "r") as f:
    original_dict = json.load(f)

# 记录entity和relationship出现次数
relationship_count_map = {}
child_count_map = {}

# 筛选出的可行relationship和entity
available_relationship = set({})
available_child_entity = set({})

# 遍历原字典，找到可行relationship和entity
for movie in original_dict:
    all_triplet = original_dict[movie]
    for triplet in all_triplet:
        relationship = triplet[1]
        child_entity = triplet[2]  # 尾entity
        relationship_count_map.setdefault(relationship, 0)
        relationship_count_map[relationship] += 1
        if relationship_count_map[relationship] > relationship_threshold:
            available_relationship.add(relationship)
        child_count_map.setdefault(child_entity, 0)
        child_count_map[child_entity] += 1
        if child_count_map[child_entity] >= entity_core:
            available_child_entity.add(child_entity)

# print(available_child_entity)
# print(available_relationship)

# 再遍历一遍原字典，找出符合可行条件的triplet集合
sampled_entity_map = {}
entity_count = 0
for movie in original_dict:
    all_triplet = original_dict[movie]
    for triplet in all_triplet:
        relationship = triplet[1]
        child_entity = triplet[2]
        sampled_entity_map.setdefault(movie, [])
        if relationship in available_relationship:
            if child_entity in available_child_entity:
                sampled_entity_map[movie].append(triplet)
                entity_count += 1

print(entity_count)

# 保存筛选过一次的字典为json文件
with open("sampled_movie_triplet_dict.json", "w") as file:
    json_str = json.dumps(sampled_entity_map)
    file.write(json_str)
