#coding=utf-8
# 基于多叉树的elt调度任务
import settings
import cx_Oracle
import os
import logging
import logging.config

from Node import Node
from Tree import MultiTree, TreeNode
from utils import get_db_conn, postorder


#bean对象


#根据不同的需要组成输出不同的素组

class EtlManager:
    '''
    def findChild( string, nodes, result_list):
        children =[]
        temps = (a['producer_children'] for a in result_list if a['producer_father'] ==string)
        for temp in temps.split(","):

            child  = Node(temp.lower(),None)
            EtlManager.findChild(temp.lower(),nodes,result_list)
            children.append(child)
        node = Node(string,children)
        nodes.append(node)
    '''
    if __name__=="__main__":
        cn =get_db_conn().cursor()
        ssql ="select * from etl_manager";
        cn.execute(ssql)
        result_list =[]
        colunms = [colunm[0].lower() for colunm in  cn.description]
        results = cn.fetchall()
        producer_father_list =[]
        for result   in results :
            producer_father_list.append(result[1].lower())
            result_dict =dict(zip(colunms,result))
            result_list.append(result_dict)
        #print result_list[0]
        #变成Treenode
        roots = []
        T = MultiTree('tree')
        for result in result_list:
            val = result['producer_father'].lower()
            T.add(TreeNode(val))
            for temp in result['producer_children'].split(","):
                T.add(TreeNode(temp.lower()),TreeNode(val))
        T.show_tree()
        set=[]
        set =postorder(T.tree)

'''
        #增加方法，删除重复的，并且不改变顺序 (实际上，在组成树的时候已经判断了)
        func = lambda x,y:x if y in x else x + [y]
        set = reduce(func, [[], ] + ps)
        print set
        print len(set)
'''


