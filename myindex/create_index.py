#
#Author: zephyr
#Date: 2020-12-16 21:38:23
#LastEditors: zephyr
#LastEditTime: 2020-12-19 18:05:41
#FilePath: \IR_codes\myindex\create_index.py
#

import os, time

from jieba.analyse import ChineseAnalyzer
from whoosh.fields import *
from whoosh.index import create_in

from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser

def buildIndex(indexpath,datapath):
    if not os.path.exists(indexpath):
        os.makedirs(indexpath)
    start = time.time()
    analyser = ChineseAnalyzer()
    schema = Schema(url=TEXT(stored=True, analyzer=analyser),date=TEXT(stored=True, analyzer=analyser), title=TEXT(stored=True, analyzer=analyser),content=TEXT(stored=True, analyzer=analyser))
    ix = create_in(indexpath, schema=schema, indexname='list')
    writer = ix.writer()
    c = 0
    for fn in traverseFile(datapath):
        c+=1
        f = open(fn,encoding='UTF-8')
        url1 = f.readline()
        date1 = f.readline()
        title1 = f.readline()
        content1 = f.read()
        f.close()
        writer.add_document(url=url1,date=date1, title=title1, content=content1)

    writer.commit()
    end = time.time()
    print("Finished: " + str(c) + " files added")
    print("Time:" + "%.3f" % (end - start) + "s")

def traverseFile(root): #遍历
    flist = []
    for f in os.listdir(root):
        f_path = os.path.join(root, f)
        if os.path.isfile(f_path):
            flist.append(f_path)
        else:
            flist += traverseFile(f_path)
    return flist

# def search(key_word,indexpath):
#     result_list = []
#     my_index = open_dir(indexpath, indexname='list')
#     with my_index.searcher() as searcher:       #单字段匹配或多字段匹配
#         # parser1 = QueryParser("url", my_index.schema)
#         # parser2 = QueryParser("title", my_index.schema)
#         # parser3 = QueryParser("content", my_index.schema)
#         # my_query =  parser2.parse(key_word) and parser3.parse(key_word)
#         my_query = MultifieldParser(["title", 'content'], my_index.schema).parse(key_word)
#
#         results = searcher.search(my_query, limit=None)
#         count = 0
#         for i in range(len(results)):
#             print(results[i])
#         results.fragmenter.charlimit=None   #分片
#
#         for result_item in results:     #关键词高亮
#             a=result_item.highlights("title")
#             b=result_item.highlights("content")
#             count = count + 1
#             result_item = dict(result_item)
#             result_item["num"] = count
#             if a!="":                           #调整返回结果
#                 result_item["title"] = a
#             if b!="":
#                 result_item["content"] = b
#             result_list.append(result_item)
#         print(result_list)
#     return result_list

if __name__ == '__main__':
    indexpath=r"../index"    #索引存放位置
    datapath="../data"      #数据存放位置
    buildIndex(indexpath,datapath)    #创建索引

    # start = time.time()
    # result_list = []
    # resnum = 0
    # result_list = search("辽宁")
    #
    # resnum = len(result_list)
    # end = time.time()
    # print("%.6f" % (end - start))
    # print(resnum)