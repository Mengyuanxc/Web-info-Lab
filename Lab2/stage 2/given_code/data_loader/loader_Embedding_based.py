import os
import random
import collections

import torch
import numpy as np
import pandas as pd

from loader_base import DataLoaderBase


class DataLoader(DataLoaderBase):

    def __init__(self, args, logging):
        super().__init__(args, logging)

        self.cf_batch_size = args.cf_batch_size
        self.kg_batch_size = args.kg_batch_size
        self.test_batch_size = args.test_batch_size

        kg_data = self.load_kg(self.kg_file)
        self.construct_data(kg_data)
        self.print_info(logging)


    def construct_data(self, kg_data):
        '''
            kg_data 为 DataFrame 类型
        '''
        # 1. 为KG添加逆向三元组，即对于KG中任意三元组(h, r, t)，添加逆向三元组 (t, r+n_relations, h)，
        #    并将原三元组和逆向三元组拼接为新的DataFrame，保存在 self.kg_data 中。

        #self.kg_data = 

        # 2. 计算关系数，实体数和三元组的数量
        #self.n_relations = 
        #self.n_entities = 
        #self.n_kg_data = 

        # 3. 根据 self.kg_data 构建字典 self.kg_dict ，其中key为h, value为tuple(t, r)，
        #    和字典 self.relation_dict，其中key为r, value为tuple(h, t)。
        self.n_relations = 0         #计算关系数
        self.n_entitys = 0           #计算实体数
        data = {}
        data['h'] = []
        data['r'] = []
        data['t'] = []
        for i in range(0,kg_data.shape[0]):
            """
            循环计算关系数和实体数
            """
            if(kg_data.loc[i]["r"]>self.n_relations):
                self.n_relations = kg_data.loc[i]["r"]
            if(kg_data.loc[i]["h"]>self.n_entitys):
                self.n_entitys = kg_data.loc[i]["h"]
            if(kg_data.loc[i]["t"]>self.n_entitys):
                self.n_entitys = kg_data.loc[i]["t"]
        self.n_relations += 1
        self.n_entitys += 1

        ori_len = kg_data.shape[0]  #记录原来的长度
        #获取反转并生成字典
        self.kg_dict = collections.defaultdict(list)
        self.relation_dict = collections.defaultdict(list)
        for i in range(0,ori_len):
            rows = kg_data.loc[i]
            data['h'].append(rows['t'])
            data['t'].append(rows['h'])
            data['r'].append(rows['r']+self.n_relations)
            self.kg_dict[rows['h']].append((rows['t'],rows['r']))
            self.kg_dict[rows['t']].append((rows['h'],rows['r']+self.n_relations))
            self.relation_dict[rows['r']].append((rows['h'],rows['t']))
            self.relation_dict[rows['r']+self.n_relations].append((rows['t'],rows['h']))
        self.kg_data = pd.concat([kg_data,pd.DataFrame(data)],ignore_index=True)
        self.n_relations *= 2   #翻倍了
        self.n_kg_data = self.kg_data.shape[0]
        print("数据处理完毕,关系数为:"+str(self.n_relations)+"实体数为:"+str(self.n_entitys)+"三元组数为:"+str(self.n_kg_data))
        



    def print_info(self, logging):
        logging.info('n_users:      %d' % self.n_users)
        logging.info('n_items:      %d' % self.n_items)
        logging.info('n_entities:   %d' % self.n_entities)
        logging.info('n_relations:  %d' % self.n_relations)

        logging.info('n_cf_train:   %d' % self.n_cf_train)
        logging.info('n_cf_test:    %d' % self.n_cf_test)

        logging.info('n_kg_data:    %d' % self.n_kg_data)


#以下为功能测试
def load_kg(filename):
    kg_data = pd.read_csv(filename, names=['h', 'r', 't'], engine='python')
    kg_data = kg_data.drop_duplicates()
    return kg_data

if __name__ == '__main__':
    """
    测试补全的功能是否正确
    """
    kg_data = load_kg("../data/Douban/kg_final.txt")
    n_relations = 0         #计算关系数
    n_entitys = 0           #计算实体数
    data = {}
    data['h'] = []
    data['r'] = []
    data['t'] = []
    print(kg_data)
    print(kg_data.shape[0])
    print(kg_data.loc[kg_data.shape[0]-1])
    for i in range(0,kg_data.shape[0]):
        """
        循环计算关系数和实体数
        """
        if(kg_data.loc[i]["r"]>n_relations):
            n_relations = kg_data.loc[i]["r"]
        if(kg_data.loc[i]["h"]>n_entitys):
            n_entitys = kg_data.loc[i]["h"]
        if(kg_data.loc[i]["t"]>n_entitys):
            n_entitys = kg_data.loc[i]["t"]
    n_relations += 1
    n_entitys += 1

    print(n_relations)
    print(n_entitys)
    ori_len = kg_data.shape[0]  #保留原来的长度
    #获取反转并生成字典
    kg_dict = collections.defaultdict(list)
    relation_dict = collections.defaultdict(list)
    for i in range(0,ori_len):
        if i%10000 == 0:
            print(i)
        rows = kg_data.loc[i]
        data['h'].append(rows['t'])
        data['t'].append(rows['h'])
        data['r'].append(rows['r']+n_relations)
        kg_dict[rows['h']].append((rows['t'],rows['r']))
        kg_dict[rows['t']].append((rows['h'],rows['r']+n_relations))
        relation_dict[rows['r']].append((rows['h'],rows['t']))
        relation_dict[rows['r']+n_relations].append((rows['t'],rows['h']))
    print(kg_dict)
    input("Pause")
    print(relation_dict)
    input("Pause")
    print(pd.DataFrame(data))
    print(kg_data)
    kg_data = pd.concat([kg_data,pd.DataFrame(data)],ignore_index=True)
    print(kg_data)
    print(kg_data.shape[0])

    ##构造对应的字典
    
    # predict(args)
