#Movie_word_segmentation_jieba      对电影进行分词处理
#预期效果:读取信息检索所得到的csv文件，对其中的剧情简介进行分词拆成一堆关键词，再加上演员以及类型生成关键词表，
#最终在原csv表加上最后一项——关键词生成新的csv表，不打乱电影原有的顺序

import csv
import jieba        #结巴分词
from snownlp import SnowNLP
import time

def remove_stopword(target_string, stopword_string):        #去除停用词(包括标点符号)
    for word in stopword_string:
        try:
            target_string.remove(word)
        except:
            pass


def get_string(result, source):         #从source中提取单引号中字符串加到result后面
    state = 0
    string = ""
    for i in source:        #自己提取字符串内容
        if i == '\'' and state == 0:        #开始提取
            state = 1
        elif i == '\'' and state == 1:      #提取完毕
            state = 0
            result.append(string)
            string = ""
        elif state == 1:                    #提取中
            string += i
    
if __name__ == '__main__':

    time_jieba = 0          #计时
    time_snownlp = 0    
    #从stopword.txt导入停用词表
    stopword_file = "stopword.txt"
    stopword_list = []
    with open(stopword_file,'r',encoding='utf-8') as file:
        line = file.readline()
        while(line):
            stopword_list.append(line[:-1])
            line = file.readline()
    stopword_list.append("\u3000")
    #停用词表构建完成


    input = "Movie_details.csv"
    output_jieba = "Movie_word_segmentation_jieba.csv"
    output_snownlp = "Movie_word_segmentation_snownlp.csv"
    #构建关键词表加入到每一部电影的列表末尾，结果存入"Movie_word_segmentation.csv"
    with open(input, 'r', encoding='utf-8') as input_file:
        with open(output_jieba, 'w', encoding='utf-8') as output_jieba_file:
            with open(output_snownlp, 'w', encoding='utf-8') as output_snownlp_file:
                csv_reader = csv.reader(input_file)
                csv_writer_jieba = csv.writer(output_jieba_file,lineterminator='\n')
                csv_writer_snownlp = csv.writer(output_snownlp_file,lineterminator='\n')
                i = 0
                for row in csv_reader:
                    #print(row[4])
                    ####这里进行分词处理附加到row的末尾
                    keyword = []        ##关键词
                    state = 0
                    string = ""
                    #先加入导演
                    get_string(keyword, row[4])
                            
                    #将演员名都加入关键词
                    get_string(keyword, row[5])

                    #再加入电影类型
                    get_string(keyword, row[6])

                    keyword_snownlp = keyword.copy()            ##复制一个，一会用snownlp分词
                    #再对剧情简介进行分词处理 To be done
                    #print(keyword)
                    time_start = time.time()
                    seg_list_jieba = list(jieba.cut(row[8], cut_all=False))
                    keyword += seg_list_jieba
                    time_end = time.time()
                    time_jieba += (time_end-time_start)

                    time_start = time.time()
                    if(row[8]):             #snownlp不能处理空字符串
                        seg_list_snownlp = SnowNLP(row[8])
                        keyword_snownlp += seg_list_snownlp.words
                    time_end = time.time()
                    time_snownlp += (time_end-time_start)

                    keyword = list(set(keyword))            #去重
                    keyword_snownlp = list(set(keyword_snownlp))
                    remove_stopword(keyword, stopword_list)     #删除停用词
                    remove_stopword(keyword_snownlp, stopword_list)

                    #print(keyword)
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