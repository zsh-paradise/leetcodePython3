#coding=utf-8
#读取数据组装成多叉树
class Node:
    def __init__(self, val, children):
        self.val = val
        self.children = children
