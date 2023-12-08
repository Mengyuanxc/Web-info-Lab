import json


original_movie_triplet_dict = None

with open("movie_triplet_dict.json", "r") as f:
    original_movie_triplet_dict = json.load(f)

step2_list = None
step2_triplets = set({})
with open("sampled_2step_triplets.json", "r") as f:
    step2_list = json.load(f)

for triplet in step2_list:
    head_entity = triplet[0]
    tail_entity = triplet[2]
    step2_triplets.add(head_entity)
    step2_triplets.add(tail_entity)

for movie in original_movie_triplet_dict:
    if movie not in step2_triplets:
        print("false!!")
print("true!!")