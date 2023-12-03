import gzip
import pickle
import json

movie_triplet_dict = None

with open("movie_triplet_dict.json", "r") as f:
    movie_triplet_dict = json.load(f)

with gzip.open("data/freebase_douban.gz", 'rb') as f:
    for line in f:
        line = line.strip()
        triplet = line.decode().split('\t')[:3]
