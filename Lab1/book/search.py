##根据给定关键词检索倒排表进行搜索

import file_readwrite
from book_word_segmentation import get_string
import csv

index_list_file = "index_list_file"     #存储单词位置表
inverted_table_file = "inverted_table_file"         #存储倒排表
#index_list = []
list_num = 10                           #每次搜索显示最匹配的前10项
book_num = 1200                        #电影总数量

#with open (index_list_file, 'r', encoding='utf-8') as input_file_1:
    #str_read = input_file_1.readline()          #单词——倒排表项索引表
    #get_string(index_list, str_read)
    #input_file_1.close()
index_list = file_readwrite.Read_list_str(index_list_file)

inverted_table = file_readwrite.Read_list(inverted_table_file)


def getSym(aimWord, wordSet):
    result = []
    for words in wordSet:
        for word in words:
            if aimWord == word:
                return words
    return [aimWord]

f = open('dict_synonym.txt', 'r', encoding='utf-8')
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
'''
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
'''

##读入搜索，采用主析取范式的方式来记录搜索
keyword = []        #记录关键词
final_score = [0.0]*book_num        #记录每一项得分
cnt_temp = [0]*book_num             #记录当前命中数
cnt_temp_NOT = [0]*book_num         #记录not项命中数
#得分计算方式为: 多个or式中最高者，每个分式分数计算为:记录命中项数N和总项数M，最终得分为100*N/M

while True:
    print("请输入关键词的and连接的bool式,非式前加一个NOT:")
    print("例如: A B NOT C")
    print("输入 -1 结束输入")
    get_str = input()
    if(get_str == "-1"):
        break
    get_str = get_str.split(" ")
    keyword.append(get_str)
    print("多次输入的关键词bool式采用or连接")

#print(keyword)
for and_word in keyword :    #开始解析
    cnt = len(and_word)
    i = 0
    cnt_NOT = 0
    cnt_temp = [0]*book_num     #记录and关键词命中数
    cnt_temp_NOT = [0]*book_num     #记录and关键词命中数
    while i < cnt:
        word = and_word[i]
        reverse = False
        index_of_table = -1
        if word == 'NOT':
            reverse = True
            word = and_word[i+1]
            cnt_NOT += 1
        for word_set in index_list:
            if word in word_set:
                index_of_table = index_list.index(word_set)
                break
        if index_of_table != -1:          #关键词存在
            for index_of_book in inverted_table[index_of_table]:       #给每一项加分
                if reverse:
                    cnt_temp_NOT[index_of_book] += 1
                else:
                    cnt_temp[index_of_book] += 1
                #print(index_of_book)
        if reverse:
            i += 2
        else:
            i += 1
    for i in range(0, book_num):     #更新每部电影分数
        temp_score = 100*(cnt_temp[i]+cnt_NOT-cnt_temp_NOT[i])/(cnt-cnt_NOT)
        if temp_score>final_score[i]:
            final_score[i] = temp_score

judge = False           #没有书籍匹配
for j in range(0, book_num):            #检测是否有书籍匹配
    if (final_score[j] > 0.0):
        judge = True

if judge == False:
    print("未能检索到符合条件的书籍")


else:
    movie_information = []
    movie_file = "Book_details.csv"            #书籍文件
    with open(movie_file, 'r', encoding='utf-8') as input_file:
        csv_reader = csv.reader(input_file)
        for row in csv_reader:
            movie_information.append(row)
    print("以下为最符合检索条件的"+str(list_num)+"部书籍:")
    for i in range(0,list_num):
        max_score = max(final_score)
        if(max_score == 0.0):                 #没有匹配的书籍
            print("已无匹配的书籍")
            exit(0)
        max_idx = final_score.index(max_score)       #定位最高匹配书籍下标
        print(movie_information[max_idx][1],end='， ')
        print("匹配度为:"+str(max_score))
        final_score[max_idx] = 0
