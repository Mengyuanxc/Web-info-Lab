#Movie_word_segmentation_jieba      用结巴对电影进行分词处理
#预期效果:读取信息检索所得到的csv文件，对其中的剧情简介进行分词拆成一堆关键词，再加上演员以及类型生成关键词表，
#最终在原csv表加上最后一项——关键词生成新的csv表，不打乱电影原有的顺序

import csv

if __name__ == '__main__':
    input = "Movie_details.csv"
    output = "Movie_word_segmentation.csv"
    with open(input, 'r', encoding='utf-8') as input_file:
        with open(output, 'w', encoding='utf-8') as output_file:
            csv_reader = csv.reader(input_file)
            csv_writer = csv.writer(output_file,lineterminator='\n')
            for row in csv_reader:
                #print(row[4])
                ####这里进行分词处理附加到row的末尾
                keyword = []        ##关键词
                state = 0
                string = ""
                #先加入导演
                for i in row[4]:        #自己提取字符串内容
                    if i == '\'' and state == 0:        #开始提取
                        state = 1
                    elif i == '\'' and state == 1:      #提取完毕
                        state = 0
                        keyword.append(string)
                        string = ""
                    elif state == 1:                    #提取中
                        string += i
                        
                #将演员名都加入关键词
                for i in row[5]:        #自己提取字符串内容
                    if i == '\'' and state == 0:        #开始提取
                        state = 1
                    elif i == '\'' and state == 1:      #提取完毕
                        state = 0
                        keyword.append(string)
                        string = ""
                    elif state == 1:                    #提取中
                        string += i

                #再加入电影类型
                for i in row[6]:        #自己提取字符串内容
                    if i == '\'' and state == 0:        #开始提取
                        state = 1
                    elif i == '\'' and state == 1:      #提取完毕
                        state = 0
                        keyword.append(string)
                        string = ""
                    elif state == 1:                    #提取中
                        string += i


                #再对剧情简介进行分词处理 To be done
                #print(keyword)

                keyword = list(set(keyword))            #去重
                row.append(keyword)
                csv_writer.writerow(row)
                

            input_file.close()
            output_file.close()
