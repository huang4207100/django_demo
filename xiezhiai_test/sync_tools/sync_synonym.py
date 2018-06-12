from datetime import datetime
from pymongo import MongoClient

test_mongo_url = "mongodb://algo:algo2018!!!@39.106.49.104:10017/"
local_mongo_url = "mongodb://algo:dev2018@192.168.240.76:27011/"
real_mongo_url = "mongodb://algo:robot2018AI!!!@192.168.245.146:27017/"


def get(tid, url,log):
    # 正式环境  mongodb://algo:robot2018AI!!!@192.168.245.146:27017/
    # 研发环境  mongodb://algo:dev2018@192.168.240.76:27011/
    # 测试环境  mongodb://algo:algo2018!!!@39.106.49.104:10017/
    client = MongoClient(url)
    db = client["algo_res"]
    coll = db["synonym_level_3"]
    one = coll.find_one({"tenant_id": tid})
    client.close()
    return one


def update(tid, one, url,log):
    client = MongoClient(url)
    db = client["algo_res"]
    coll = db["synonym_level_3"]
    del one["_id"]
    one["timestamp"] = str(datetime.now())

    try:

        one["tenant_id"] = tid
        coll.update({"tenant_id": tid}, one, upsert=True)
        log.info("update tenant_id %d" % tid)
        #coll.update({"tenant_id": tid}, {"$set": one}, upsert=True)
    except:
        one["tenant_id"] = tid
        coll.insert(one)
        log.info("insert tenant_id %d" % one)


#one = get(tid=81,url=test_mongo_url)
#print(one)
# update(tid=22,one=one,url=test_mongo_url)

def start_copy(srcurl,dsturl,srctid,dsttid,log):
    log.info('开始同义词复制')
    one = get(tid=srctid, url=srcurl,log=log)
    log.info(one)
    update(tid=dsttid, one=one, url=dsturl,log=log)

def synonym_sync_from_real_to_test(srctid, dsttid):
    one = get(tid=srctid, url=real_mongo_url)
    print(one)
    update(tid=dsttid, one=one, url=test_mongo_url)


def synonym_sync_from_test_to_local(srctid, dsttid):
    one = get(tid=srctid, url=test_mongo_url)
    print(one)
    update(tid=dsttid, one=one, url=local_mongo_url)
