'''
Book_word_segmentation_jieba: 对书籍进行分词处理
'''

import csv
import jieba
from snownlp import SnowNLP
import time
import re


def remove_square_brackets(s:str):
    pattern = r'\[.*\]'
    return re.sub(pattern, '', s)
def remove_stopword(target_string, stopword_string):
    for word in stopword_string:
        try:
            target_string.remove(word)
        except:
            pass


def get_string(result, source):
    state = 0
    string = ""
    for i in source:
        if i == '\'' and state == 0:
            state = 1
        elif i == '\'' and state == 1:
            state = 0
            result.append(string)
            string = ""
        elif state == 1:
            string += i


if __name__ == '__main__':
    time_jieba = 0  # 计时
    time_snownlp = 0
    stopword_file = "stopword.txt"
    stopword_list = []
    with open(stopword_file,'r',encoding='utf-8') as file:
        line = file.readline()
        while(line):
            stopword_list.append(line[:-1])
            line = file.readline()
    stopword_list.append("\u3000")

    input = "Book_details.csv"
    output_jieba = "Book_word_segmentation_jieba.csv"
    output_snownlp = "Book_word_segmentation_snownlp.csv"
    with open(input, 'r', encoding='utf-8') as input_file:
        with open(output_jieba, 'w', encoding='utf-8') as output_jieba_file:
            with open(output_snownlp, 'w', encoding='utf-8') as output_snownlp_file:
                csv_reader = csv.reader(input_file)
                csv_writer_jieba = csv.writer(output_jieba_file, lineterminator='\n')
                csv_writer_snownlp = csv.writer(output_snownlp_file, lineterminator='\n')
                i = 0
                for row in csv_reader:
                    keyword = []
                    state = 0
                    string = ""

                    # 获取作者名称
                    author = remove_square_brackets(str(row[4]))
                    # print(author)

                    keyword.append(author)

                    keyword_snownlp = keyword.copy()

                    time_start = time.time()
                    seg_list_jieba = list(jieba.cut(row[-1], cut_all=False))
                    keyword += seg_list_jieba
                    time_end = time.time()
                    time_jieba += time_end - time_start

                    time_start = time.time()
                    if(row[-1]):
                        seg_list_snownlp = SnowNLP(row[-1])
                        keyword_snownlp += seg_list_snownlp.words
                    time_end = time.time()
                    time_snownlp += (time_end - time_start)

                    keyword = list(set(keyword))
                    keyword_snownlp = list(set(keyword))
                    remove_stopword(keyword, stopword_list)
                    remove_stopword(keyword, stopword_list)

                    row.append(keyword)
                    csv_writer_jieba.writerow(row)
                    row.pop()
                    row.append(keyword_snownlp)
                    csv_writer_snownlp.writerow(row)
    input_file.close()
    output_jieba_file.close()
    output_snownlp_file.close()


    print("结巴分词用时为:" + str(time_jieba))
    print("snownlp分词用时为:" + str(time_snownlp))

