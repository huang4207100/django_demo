from datetime import datetime
from pymongo import MongoClient

test_mongo_url = "mongodb://algo:algo2018!!!@39.106.49.104:10017/"
local_mongo_url = "mongodb://algo:dev2018@192.168.240.76:27011/"
real_mongo_url = "mongodb://algo:robot2018AI!!!@192.168.245.146:27017/"

def get(tid,url):
	#正式环境  mongodb://algo:robot2018AI!!!@192.168.245.146:27017/
	#研发环境  mongodb://algo:dev2018@192.168.240.76:27011/
	#测试环境  mongodb://algo:algo2018!!!@39.106.49.104:10017/
	client = MongoClient(url)
	db = client["algo_res"]
	coll = db["conf_algo"]
	one = coll.find_one({"tid": tid})
	client.close()
	return one


def update(tid, one,url,log):
	client = MongoClient(url)
	db = client["algo_res"]
	coll = db["conf_algo"]
	del one["_id"]
	one["tid"] = tid
	one["timestamp"] = str(datetime.now())
	coll.update({"tid": tid}, one, upsert=True)

	try:
		coll.update({"tid": tid}, {"$set": one}, upsert=True)
		log.info("update tid %d" % tid)
	except:
		coll.insert(one)
		log.warning("insert tid %d" % one)


def start_copy(srcurl,dsturl,srctid,dsttid,log):
	log.info("开始同步算法config")
	one = get(tid=srctid, url=srcurl)
	log.info(one)
	update(tid=dsttid, one=one, url=dsturl,log=log)

def synonym_sync_from_real_to_test(srctid,dsttid):
	one = get(tid=srctid,url=real_mongo_url)
	print(one)
	update(tid=dsttid,one=one,url=test_mongo_url)

def synonym_sync_from_test_to_local(srctid,dsttid):
	one = get(tid=srctid, url=test_mongo_url)
	print(one)
	update(tid=dsttid, one=one, url=local_mongo_url)
