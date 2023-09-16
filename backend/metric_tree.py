import json
import os

import keywordExtract.storytree as storytree
from datetime import datetime
# Define Node class
# from BackEnd.keywordExtract import storytree


class Node:
    def __init__(self, data,name):
        self.data = data  # value of node
        self.children = []  # list of children
        self.parent = None
        self.keyset= set()
        self.name=name
        self.docNum=0
        self.genSet()

    def genSet(self):
        docNum=0
        for sep_keylist in self.data:

            for keylist in sep_keylist:
                docNum = docNum + 1
                # print("keylist: "+",".join(keylist))
                for key in keylist:
                    self.keyset.add(key)
        self.docNum=docNum
        # print(self.keyset)

# Define Tree class
class Tree:
    def __init__(self):
        self.root = None  # pointer to root node
        self.nodenum = 0
        self.leaveList=[]
        self.docNum=0
    # Insert method
    def insert(self, data, parent,name):
        # Create new node with data
        new_node = Node(data,name)
        parent.children.append(new_node)
        new_node.parent=parent
        self.nodenum=1+self.nodenum
        self.docNum=new_node.docNum+self.docNum

        return new_node
    def initTree(self,jsonDict):
        self.root=Node([],'ROOT')

        self.buildTree(jsonDict["children"],self.root)

    def buildTree(self, jsonList,parent):

        for jsonTemp in jsonList:
            new_node=self.insert(jsonTemp["tree_allkeyword"],parent,jsonTemp["name"])
            if(len(jsonTemp["children"])!=0):
                self.buildTree(jsonTemp["children"],new_node)
            else:
                self.leaveList.append(new_node)


    # Traverse method (pre-order)
    def traverse(self, node=None):
        # If node is None,
        # start from root
        if not node:
            node = self.root
        print(node.name)
        print(node.keyset)  # Print value of current node

        for child in node.children:  # Recursively traverse each child
            self.traverse(child)


    def genMetricA(self):
        metricA=0

        metricA=self.metricA_recur(self.root.children)
        return metricA

    def metricA_recur(self,temp_node_list):
        sumMetric = 0
        while len(temp_node_list)!=0:
            for temp_node in temp_node_list:
                for childNode in temp_node.children:
                    # print('----')
                    # print(temp_node.name)
                    # print(childNode.name)
                    # print('----')
                    # print(temp_node.keyset)
                    # print(childNode.keyset)
                    temp_metric = len(temp_node.keyset.intersection(childNode.keyset))
                    # print(temp_metric)
                    sumMetric = sumMetric + temp_metric
                sumMetric = sumMetric + self.metricA_recur(temp_node.children)
            return sumMetric
        return 0

        # sumMetric=0
        # while len(temp_node.children)!=0:
        #     for childNode in temp_node.children:
        #         print('----')
        #         print(temp_node.name)
        #         print(childNode.name)
        #         print('----')
        #         # print(temp_node.keyset)
        #         # print(childNode.keyset)
        #         temp_metric=len(temp_node.keyset.intersection(childNode.keyset))
        #         # print(temp_metric)
        #         sumMetric=sumMetric+temp_metric
        #         sumMetric=sumMetric+self.metricA_recur(childNode)
        #     return sumMetric
        # return 0




    def genMetricB(self):
        metricB=0
        for leafnode in self.leaveList:
            print("leafnode start!!!")
            while leafnode.name!="ROOT":
                print("begin temp0 : nodename : "+leafnode.name)
                metricB=metricB+self.metricB_recur(leafnode.parent,leafnode.keyset)
                leafnode=leafnode.parent


        return metricB
        # for childNode in self.root.children:
        #     for childchildNode in childNode.children:
        #         metricB=metricB+self.metricB_recur(childchildNode,childNode.keyset)
        #
        #
        # return metricB
        #从根节点开始，往子节点走，维护一个大的set list
        #每到分叉则list需要复制
        #到根节点 来


    def metricB_recur(self,temp_node,tempSet):
        print("===========================")
        print(temp_node.name)

        if temp_node.name=="ROOT":
            print("in ROOT!!!!!!!")
            return 0
        else:
            tempSet2 = tempSet.intersection(temp_node.keyset)
            print("len: " + str(len(tempSet2)))
            print("begin temp1: node name: "+temp_node.name)
            temp1=self.metricB_recur(temp_node.parent,tempSet)
            # print("temp1: " + str(temp1))
            # print("begin temp2 : "+temp_node.name)
            # temp2=self.metricB_recur(temp_node.parent,temp_node.keyset)


            # print("temp2: "+str(temp2))
            return len(tempSet2)+temp1

        #
        # if len(temp_node.children)==0: #leaf node
        #     print('leafNode!!!: '+str(len(tempSet)))
        #     return len(tempSet)
        # else: # not leaf node
        #     sumMetric=0
        #     for childNode in temp_node.children:
        #         sumMetric=sumMetric+self.metricB_recur(childNode,tempSet)
        #
        #     return sumMetric


def genMetricTotal(fname):
    f = open(fname, 'r')
    tree_pro_json = json.load(f)
    f.close()

    #找到所有分支，读取keyword信息
    tree_pro=Tree()
    tree_pro.initTree(tree_pro_json)
    metricA=tree_pro.genMetricA()
    metricB=tree_pro.genMetricB()
    return [tree_pro.nodenum,tree_pro.docNum,metricA,metricB]
    # print(tree_pro.genMetricA())
    # tree_pro.traverse()
    # print(tree_pro.genMetricB())
    # print(tree_pro)



def genMetricEach(time_scope,mSrc_list,classnum,country_list,testId,test_conf,test_value):


    conf_dir="./conf/EnglishNewsParameters_cluster.txt"
    # conf_dir = "./EnglishNewsParameters_cluster - 副本.txt"
    f = open(conf_dir, "r+")
    content = f.readlines()

    print(content)
    for i in range(len(content)):
        if test_conf in content[i]:
            test_str = content[i]
            temp_index = content[i].find('=')
            temp_index = temp_index + 2
            test_str = test_str[0:temp_index] + str(test_value) + test_str[temp_index + 1:]
            content[i] = test_str
    print(content)
    f.seek(0)
    f.truncate()
    f.writelines(content)
    f.close()

    f=open(conf_dir,"a")
    dir_name="metric_test"
    goalpath=dir_name+"/test"+str(testId)
    os.mkdir(goalpath)
    time_cost=storytree.genMetricTreedata(time_scope, mSrc_list, classnum, country_list,goalpath)
    f = open("metric_test.csv", 'a+')
    lines = []

    # metricList = genMetricTotal(goalpath+"/tree_ori.json")
    # print(metricList)
    # temp_line = "tree_ori," + str(metricList[0]) + "," + str(metricList[1]) + "," + str(metricList[2])+","+str(metricList[3])
    metricList = genMetricTotal(goalpath+"/tree_pro.json")
    print(metricList)
    temp_line =  "tree_pro," + str(metricList[0]) + "," + str(metricList[1]) + "," + str(metricList[2]) +","+str(metricList[3])+","+str(time_cost)+test_conf+","+str(test_value)+"\n"
    lines.append(temp_line)
    f.writelines(lines)
    f.close()


if __name__ == "__main__":
    # mSrc_list = '["irishexaminer.com", "sputniknews.com", "wandsworthguardian.co.uk", "romseyadvertiser.co.uk"]'
    #
    # time_scope = '["2019-10-01","2020-01-31"]'
    # country_list = '["ALL"]'
    # classnum = '3'

    mSrc_list = '["tass.com", "bbc.co.uk", "dw.com", "reuters.com"]'
    time_scope='["2021-06-01","2022-08-31"]'
    country_list = '["ALL"]'
    classnum ='3'
    # storytree.genMetricTreedata(time_scope,mSrc_list,classnum,country_list)

    # if os.path.isfile("metric_test.csv"):
    #     os.remove("metric_test.csv")
    f = open("metric_test.csv", 'a+')
    lines = []
    lines.append("name,nodenum,docnum,tree_pro_metricA,tree_pro_metricB,time_cost,conf_name,conf_value\n")
    f.writelines(lines)
    f.close()
    index=0
    for i in range(15):
        for j in range(5):
            index=index+1
            genMetricEach(time_scope,mSrc_list,i+5,country_list,index,'cut_mul',j+1)

    for i in range(15):
        for j in range(8):
            index=index+1
            conf_value='.'+str(j+1)
            genMetricEach(time_scope,mSrc_list,i+5,country_list,index,'minSimDoc2KeyGraph ',conf_value)

    time_scope = '["2022-01-01","2022-05-31"]'
    mSrc_list = '["msn.com", "dw.com", "tass.com", "menafn.com"]'
    f = open("metric_test.csv", 'a+')
    lines = []
    lines.append("name,nodenum,docnum,tree_pro_metricA,tree_pro_metricB,time_cost,conf_name,conf_value\n")
    f.writelines(lines)
    f.close()
    for i in range(15):
        for j in range(5):
            index=index+1
            genMetricEach(time_scope,mSrc_list,i+5,country_list,index,'cut_mul',j+1)

    for i in range(15):
        for j in range(8):
            index=index+1
            conf_value='.'+str(j+1)
            genMetricEach(time_scope,mSrc_list,i+5,country_list,index,'minSimDoc2KeyGraph ',conf_value)
    # genMetricEach(time_scope,mSrc_list,9,country_list,9)_

    # list1=genMetricTotal("tree_ori.json")
    # list2=genMetricTotal("tree_pro.json")
    # print(list1)
    # print(list2)
    # print(genMetricTotal("tree_ori.json"))
    # print(genMetricTotal("tree_pro.json"))