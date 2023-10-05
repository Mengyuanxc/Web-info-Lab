##根据给定关键词检索倒排表进行搜索

import file_readwrite
from movie_word_segmentation import get_string

index_list_file = "index_list_file.txt"     #存储单词位置表
inverted_table_file = "inverted_table_file.txt"         #存储倒排表
index_list = []

with open (index_list_file, 'r', encoding='utf-8') as input_file_1:
    str_read = input_file_1.readline()          #单词——倒排表项索引表
    get_string(index_list, str_read)
    input_file_1.close()

inverted_table = file_readwrite.Read_list(inverted_table_file)

print(index_list)
print(inverted_table)
print(len(inverted_table))
print(len(index_list))

max = 0

#print(inverted_table[index_list.index('剧情')])


for list in inverted_table:
    if(len(list)>max):
        max = len(list)
print(max)
