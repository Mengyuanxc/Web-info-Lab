#利用结巴分词得到的关键词项生成倒排表

from movie_word_segmentation import get_string
import csv
import file_readwrite

index_list = []         #记录单词的位置
inverted_table = []     #倒排表
keyword_file = "Movie_word_segmentation_jieba.csv"
index_list_file = "index_list_file.txt"     #存储单词位置表
inverted_table_file = "inverted_table_file.txt"         #存储倒排表

with open (index_list_file, 'w', encoding='utf-8') as output_file_1:
    with open(keyword_file, 'r', encoding='utf-8') as input_file:
        csv_reader = csv.reader(input_file)
        index = 0               #记录对应第几条电影
        for row in csv_reader:
            keyword = []        ##关键词
            get_string(keyword, row[-1])
            for word in keyword:
                if word in index_list:          #关键词已在倒排表中
                    word_index = index_list.index(word)     #定位单词对应倒排表中哪一项
                    inverted_table[word_index].append(index)
                else:
                    index_list.append(word)         #添加关键词
                    inverted_table.append([index])       #添加倒排表
            index+=1
        output_file_1.writelines(str(index_list))
        file_readwrite.Save_list(inverted_table, inverted_table_file)
        input_file.close()
        output_file_1.close()
