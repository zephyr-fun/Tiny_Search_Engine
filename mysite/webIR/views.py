#
#Author: zephyr
#Date: 2020-12-16 21:38:24
#LastEditors: zephyr
#LastEditTime: 2020-12-19 18:06:47
#FilePath: \IR_codes\mysite\webIR\views.py
#
from django.shortcuts import render
from django.shortcuts import HttpResponse
from whoosh.index import open_dir
from whoosh.qparser import QueryParser,MultifieldParser
import os, time

# Create your views here.

def index(request):
    # return HttpResponse("hello world!")

    return render(request,"index.html")

def result(request):
    # return HttpResponse("hello world!")
    if request.method == 'POST':
        key=request.POST.get("keyword",None)
        start = time.time()
        result_list = search(key)
        end = time.time()
        resnum =len(result_list)
        times="%.6f" % (end - start)
    return render(request,"result.html",{"data": result_list,"keyword":key,"num":resnum,"time":times})

def search(key_word):
    result_list = []
    my_index = open_dir("../index", indexname='list')    #索引位置
    with my_index.searcher() as searcher:
        my_query = MultifieldParser(["title", 'content'], my_index.schema).parse(key_word)
        results = searcher.search(my_query, limit=None)
        print(results)
        for result_item in results:
            a = result_item.highlights("title")
            b = result_item.highlights("content")
            result_item = dict(result_item)
            if a != "":
                result_item["title"] = a
            if b != "":
                result_item["content"] = b
            result_item['url'] = result_item['url'][3:]
            result_list.append(result_item)
    return result_list