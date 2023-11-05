#利用结巴分词得到的关键词项生成倒排表

from book_word_segmentation import get_string
import csv
import file_readwrite

def getSym(aimWord, wordSet):
    result = []
    for words in wordSet:
        for word in words:
            if aimWord == word:
                return words
    return [aimWord]


index_list = []         #记录单词的位置
inverted_table = []     #倒排表
keyword_file = "Book_word_segmentation_jieba.csv"
index_list_file = "index_list_file.txt"     #存储单词位置表
inverted_table_file = "inverted_table_file"         #存储倒排表

f = open('dict_synonym.txt', 'r',encoding='utf-8')
lines = f.readlines()
sym_words = []
# sym_class_words = []
# 从txt中获取词条，构建同义词词集sym_words和相关词词集sym_class_words
for line in lines:
    line = line.replace('\n','')
    items = line.split(' ')
    index = items[0]
    if index[-1] == '=':
        sym_words.append(items[1:])
    # if index[-1] == '#':
    #    sym_class_words.append(items[1:])
f.close()

with open (index_list_file, 'w', encoding='utf-8') as output_file_1:
    with open(keyword_file, 'r', encoding='utf-8') as input_file:
        csv_reader = csv.reader(input_file)
        index = 0               #记录对应第几条电影
        for row in csv_reader:
            keyword = []        ##关键词
            get_string(keyword, row[-1])
            for word in keyword:
                word_index = -1
                i = 0
                for word_set in index_list:
                    if word in word_set:
                        word_index = i
                        break
                    i += 1
                if word_index != -1:          #关键词已在倒排表中
                    if inverted_table[word_index][-1] != index:
                        inverted_table[word_index].append(index)
                else:
                    index_list.append(getSym(word, sym_words))         #添加关键词(按照近义词类存储)
                    inverted_table.append([index])       #添加倒排表
            index += 1
        #output_file_1.writelines(str(index_list))
        file_readwrite.Save_list(inverted_table, inverted_table_file)
        file_readwrite.Save_list(index_list, index_list_file)
        input_file.close()
        output_file_1.close()
