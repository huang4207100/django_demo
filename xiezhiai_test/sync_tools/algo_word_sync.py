# -*- coding: utf-8 -*-
from urllib import parse,request
import json

#测试环境地址
test_url = 'http://39.106.49.104:9981'
#研发环境地址
local_url = 'http://192.168.240.76:9981'
#正式环境地址
real_url = 'http://192.168.245.146:9981'


'''
get请求获取测试环境的全局短语：
test_url测试环境地址
local_url研发环境地址
'''
def get_general_word(url=test_url):
    URL = '%s/general_word_phrase' %(url)
    req = request.Request(url='%s' %(URL))
    res = request.urlopen(req)
    res = res.read()
    res = json.loads(res)
    if res["succ"] == True:
        return res
    return False

#print(get_general_word(url=local_url))

#研发环境的全局短语操作
def post_general(url=local_url,title="图灵",action="delete"):
    textmod = {"w": title,"action": action}
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    print(textmod)
    URL = '%s/general_word_phrase' % (url)
    req = request.Request(url=URL, data=textmod)
    res = request.urlopen(req).read()
    res = json.loads(res)
    return res

#print(post_general(url=local_url,title="干什么阿阿",action="insert"))

'''
获取的全局口语化：
url测试环境地址
url1研发环境地址
'''
def get_spoken_language(url=test_url):
    URL = '%s/spoken_language' %(url)
    req = request.Request(url='%s' %(URL))
    res = request.urlopen(req)
    res = res.read()
    res = json.loads(res)
    if res["succ"] == True:
        return res
    return False

#print(get_spoken_language(url=local_url))

'''
操作全局口语化：
只是操作研发环境的新增和删除
'''
def post_spoken_language(url=local_url,action = "insert",key = "小晓科技", val = "邂智科技"):
    textmod = {"action": action,"key": key,"val": val}
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    URL = '%s/spoken_language' % (url)
    req = request.Request(url=URL, data=textmod)
    res = request.urlopen(req).read()
    res = json.loads(res)
    return res


#print(post_spoken_language(action="insert",key="中华小昂家",val="小当家"))

'''
获取强制分词的结果：
url为测试环境
url1为研发环境
'''
def get_split_world(url=test_url):
    URL = '%s/split_word_phrase' % (url)
    req = request.Request(url='%s' % (URL))
    res = request.urlopen(req)
    res = res.read()
    res = json.loads(res)
    if res["succ"] == True:
        return res
    return False

#print(get_split_world(url=local_url))


'''
操作全局强制分词-研发环境
'''
def post_split_word(url=local_url,action = "insert",key = "小晓科技", val = ["小晓","科技"]):
    textmod = {"action": action, "key": key, "val": val}
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    URL = '%s/split_word_phrase' % (url)
    req = request.Request(url=URL, data=textmod)
    res = request.urlopen(req).read()
    res = json.loads(res)
    return res

#print(post_split_word(url=local_url,action="insert",key="中华小当家",val=["中华","小当家"]))

'''
知识库级短语
'''
def get_custom_word_phrase_by_tid(url= test_url,tid=75):
    final_url = '%s/custom_word_phrase/%s' % (url,tid)
    print(final_url)
    req = request.Request(url='%s' % (final_url))
    res = request.urlopen(req)
    res = res.read()
    res = json.loads(res)
    if res["succ"] == True:
        return res
    return False

#print(get_custom_word_phrase_by_tid(url=test_url,tid=75))

def post_custom_word_phrase_by_tid(url=test_url,tid=75,ws=[]):
    textmod = {"tenant_id":tid,"ws":ws}
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    final_url = '%s/custom_word_phrase' % (url)
    req = request.Request(url=final_url, data=textmod)
    res = request.urlopen(req).read()
    res = json.loads(res)
    return res



#print(post_custom_word_phrase_by_tid(url=local_url,tid=75,ws=["邂智科技","中华小当家"]))

def del_local_data(src,log):
    #删除全局短语
    local_word = get_general_word(url=src)
    for x in local_word["word_phrase"]:
        post_general(url=src,action="delete",title=x)

    #删除口语化改写
    local_spoken = get_spoken_language(url=src)
    for x in local_spoken["word_phrase"]:
        post_spoken_language(url=src,action="delete",key=x["key"],val=x["val"])

    #删除全局分词
    local_split = get_split_world(url=src)
    for x in local_split["word_phrase"]:
        post_split_word(url=src,action="delete",key=x["key"],val=x["val"])

    #删除知识库短语
    #get_custom_word_phrase_by_tid(url=src,tid=75)
    #post_custom_word_phrase_by_tid(url=local_url,tid=28,ws=[])

def sync_test_to_local(src_url,dst_url,src_tid,dst_tid,log):
    log.info("开始短语口语同步")
    #先删除dst_url的数据
    del_local_data(src=dst_url,log=log)
    log.info("删除本地环境完成")
    #复制全局短语
    test_word =  get_general_word(url=src_url)
    for x in test_word["word_phrase"]:
        post_general(url=dst_url,action="insert",title=x)
    log.info("复制全局短语完成")

    #复制口语化改写
    test_spoken = get_spoken_language(url=src_url)
    for x in test_spoken["word_phrase"]:
        post_spoken_language(url=dst_url, action="insert", key=x["key"], val=x["val"])
    log.info("复制口语化改写")

    #复制全局分词
    test_split = get_split_world(url=src_url)
    for x in test_split["word_phrase"]:
        post_split_word(url=dst_url, action="insert", key=x["key"], val=x["val"])
    log.info("复制全局分词")

    #复制知识库短语
    test_word_tid = get_custom_word_phrase_by_tid(url=src_url,tid=src_tid)
    try:
        post_custom_word_phrase_by_tid(url=dst_url, tid=dst_tid, ws=test_word_tid["ws"])
    except KeyError:
        log.warning("ws是空的,不用更新")
    log.info("复制知识库短语完成")

def start_copy(srcurl,dsturl,srctid,dsttid,log):
    sync_test_to_local(src_url=srcurl, dst_url=dsturl, src_tid=srctid, dst_tid=dsttid,log=log)

def word_sync_from_real_to_test(srctid,dsttid):
    sync_test_to_local(src_url=real_url,dst_url=test_url,src_tid=srctid,dst_tid=dsttid)

def word_sync_from_test_to_local(srctid,dsttid):
    sync_test_to_local(src_url=test_url,dst_url=local_url,src_tid=srctid,dst_tid=dsttid)







