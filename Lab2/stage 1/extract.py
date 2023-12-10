import gzip
import csv
import json
from tqdm import tqdm


# 读取豆瓣id与电影mid，进行第一次jump，得到以电影mid为head entity的triplet集合，存入json中
def get_gzip_file_line_count(file_path):
    line_count = 0
    with gzip.open(file_path, "rb") as file:
        for _ in file:
            line_count += 1
    return line_count


# 构建movie豆瓣id到freebase mid的映射
# 例: 1291544 --> m.03177r
convert_dict = {}
with open("data/douban2fb.txt", "r") as convert_txt:
    for line in convert_txt:
        line = line.strip()
        # print(line)
        convert_list = line.split("\t")
        convert_dict[convert_list[0]] = convert_list[1]

# 读取全部的movie豆瓣id，筛选出在freebase中的电影对应的映射
# 字典大小应为578
# movie_dict 为电影id到mid的映射
# movie_dict_reverse 为mid到电影id的映射
movie_dict = {}
movie_dict_reverse = {}
with open("data/Movie_id.csv", "r") as movie_id_csv:
    csv_reader = csv.reader(movie_id_csv)
    for row in csv_reader:
        # print(row)
        if row[0] in convert_dict:
            movie_dict[row[0]] = convert_dict[row[0]]
            movie_dict_reverse[convert_dict[row[0]]] = row[0]

# 单步jump，搜索gz文件中以电影mid为head entity的三元组集合，存入movie_triplet_dict中
movie_triplet_dict = {}
# line_count: gz文件的行数
line_count = 395577070
# line_count = get_gzip_file_line_count('data/freebase_douban.gz')
# print(line_count)

with gzip.open('data/freebase_douban.gz', 'rb') as f:
    for line_num, line in tqdm(enumerate(f, start=1), total=line_count):
        line = line.strip()
        triplet = line.decode().split('\t')[:3]
        mid = triplet[0].split('/')[-1][:-1]
        if mid in movie_dict_reverse:
            if triplet[1].startswith("<http://rdf.freebase.com/ns"):
                movie_triplet_dict.setdefault(mid, [])
                movie_triplet_dict[mid].append(triplet)

# 将dict写入json文件中
with open("output/movie_triplet_dict.json", "w") as file:
    json_str = json.dumps(movie_triplet_dict)
    file.write(json_str)
