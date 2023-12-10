import gzip
from tqdm import tqdm
import json
# 第二次筛选，原理同sample.py
# entity最多出现20000次
entity_count_upper_limit = 20000
relationship_threshold = 50
entity_core = 15

relationship_count_map = {}
entity_count_map = {}

available_relationship = set({})
available_entity = set({})


# def get_gzip_file_line_count(file_path):
#     line_count = 0
#     with gzip.open(file_path, "rb") as file:
#         for _ in file:
#             line_count += 1
#     return line_count
#
# line_count = get_gzip_file_line_count("2step.gz")
# print(line_count)
line_count = 213662478

with gzip.open("data/2step.gz", "rb") as f:
    for line_num, line in tqdm(enumerate(f, start=1), total=line_count):
        line = line.strip()
        triplet = line.decode().split('\t')
        relationship = triplet[1]
        head_entity = triplet[0]
        tail_entity = triplet[2]
        relationship_count_map.setdefault(relationship, 0)
        relationship_count_map[relationship] += 1
        if relationship_count_map[relationship] > relationship_threshold:
            available_relationship.add(relationship)
        entity_count_map.setdefault(head_entity, 0)
        entity_count_map.setdefault(tail_entity, 0)
        entity_count_map[head_entity] += 1
        entity_count_map[tail_entity] += 1
        if entity_count_map[head_entity] >= entity_core:
            available_entity.add(head_entity)
        if entity_count_map[tail_entity] >= entity_core:
            available_entity.add(tail_entity)

sampled_triplets = []

with gzip.open("data/2step.gz", "rb") as f:
    for line_num, line in tqdm(enumerate(f, start=1), total=line_count):
        line = line.strip()
        triplet = line.decode().split('\t')
        relationship = triplet[1]
        head_entity = triplet[0]
        tail_entity = triplet[2]
        if entity_count_map[head_entity] < entity_count_upper_limit and entity_count_map[tail_entity] < entity_count_upper_limit:
            if head_entity in available_entity and tail_entity in available_entity and relationship in available_relationship:
                sampled_triplets.append(triplet)

print(len(sampled_triplets))
with open("output/sampled_2step_triplets.json", "w") as f:
    json_str = json.dumps(sampled_triplets)
    f.write(json_str)

