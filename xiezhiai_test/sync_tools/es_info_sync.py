
import json
from elasticsearch import Elasticsearch, helpers

import sys
import os

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

from . import config

TEST_ES_URL = "http://39.106.49.104:10200"
DEVELOP_ES_URL = "http://192.168.240.76:9200"
REAL_ES_URL = "http://192.168.245.147:9200"

def delete_all(url, index, doc,log):
	"""
	删除指定文档的全部记录。
	:param url:  elastic search host
	:param index: index name
	:param doc: doc name
	:return: (n, ok or not)
	"""
	es_client = Elasticsearch(hosts=url)
	rsp = es_client.delete_by_query(index, body={"query": {"match_all": {}}}, doc_type=doc)
	log.info(rsp)


def scan_all_question(url, index_name, tenant_id):
	"""
	获取 tenant id 的所有问句
	:return:
	"""
	es = Elasticsearch(hosts=url)
	results = helpers.scan(es, index=index_name, doc_type=str(tenant_id), preserve_order=True, query={"query": {"match_all":{}}})
	ret = []
	for item in results:
		ret.append(item)
	return ret


def load_all_qa_from_file(name):
	ret = []
	with open(name, mode="r", encoding="UTF-8") as fi:
		for l in fi.readlines():
			ret.append(json.loads(l.strip("\n"), encoding="UTF-8"))
	return ret


def sync_2_dst(url, items, tid, index_name):
	client = Elasticsearch(hosts=url)
	actions = list()
	for item in items:
		del item["_score"]
		item["_type"] = str(tid)
		item["_index"] = index_name
		actions.append(item)
	helpers.bulk(client, actions)


def start_copy(srcurl,dsturl,srctid,dsttid,log):
	log.info("开始同步es")
	ret = scan_all_question(srcurl, config.INDEX_NAME, srctid)
	delete_all(dsturl, config.INDEX_NAME, str(dsttid),log=log)
	sync_2_dst(dsturl, ret, dsttid, config.INDEX_NAME)

def es_sync_from_real_to_test(srctid,dsttid):
	index_name = "qa_pair"
	ret = scan_all_question(REAL_ES_URL, index_name, srctid)
	delete_all(TEST_ES_URL, index_name, str(dsttid))
	sync_2_dst(TEST_ES_URL, ret, dsttid, index_name)

def es_sync_from_test_to_local():
	tid = 28
	index_name = "qa_pair"
	ret = scan_all_question(TEST_ES_URL, index_name, 28)
	delete_all(DEVELOP_ES_URL, index_name, str(tid))
	sync_2_dst(DEVELOP_ES_URL, ret, tid, index_name)