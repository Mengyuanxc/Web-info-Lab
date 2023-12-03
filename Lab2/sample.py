import json


original_dict = None

entity_core = 20
relationship_threshold = 50

with open("movie_triplet_dict.json", "r") as f:
    original_dict = json.load(f)

relationship_count_map = {}
child_count_map = {}

available_relationship = set({})
available_child_entity = set({})

for movie in original_dict:
    all_triplet = original_dict[movie]
    for triplet in all_triplet:
        relationship = triplet[1]
        child_entity = triplet[2]
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

with open("sampled_movie_triplet_dict.json", "w") as file:
    json_str = json.dumps(sampled_entity_map)
    file.write(json_str)

