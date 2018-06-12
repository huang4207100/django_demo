# from final.sync_config_algo import *
# from final.es_info_sync import *
# from final.algo_word_sync import *
from . import algo_word_sync
from . import sync_config_algo
from . import es_info_sync
from . import config
from . import sync_synonym
import logging

def start_copy(srcurl,dsturl,srctid,dsttid,control):

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("log.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    srcurl = srcurl
    if srcurl==1:
        src_es_url = config.TEST_ES_URL
        src_word_url = config.TEST_WORD_URL
        src_mongo_url = config.TEST_MONGO_URL
    elif srcurl==2:
        src_es_url = config.DEVELOP_ES_URL
        src_word_url = config.DEVELOP_WORD_URL
        src_mongo_url = config.DEVELOP_MONGO_URL
    elif srcurl==3:
        src_es_url = config.REAL_ES_URL
        src_word_url = config.REAL_WORD_URL
        src_mongo_url = config.REAL_MONGO_URL

    dsturl = dsturl
    if dsturl == 1:
        dst_es_url = config.TEST_ES_URL
        dst_word_url = config.TEST_WORD_URL
        dst_mongo_url = config.TEST_MONGO_URL
    elif dsturl == 2:
        dst_es_url = config.DEVELOP_ES_URL
        dst_word_url = config.DEVELOP_WORD_URL
        dst_mongo_url = config.DEVELOP_MONGO_URL

    srctid = srctid
    dsttid = dsttid

    control = control
    if control==1:
        print("start_copy algo_word_sync")
        algo_word_sync.start_copy(srcurl=src_word_url,dsturl=dst_word_url,srctid=srctid,dsttid=dsttid,log=logger)
        print("start_copy sync_synonym")
        sync_synonym.start_copy(srcurl=src_mongo_url,dsturl=dst_mongo_url,srctid=srctid,dsttid=dsttid,log=logger)
        print("start_copy es_info_sync")
        es_info_sync.start_copy(srcurl=src_es_url,dsturl=dst_es_url,srctid=srctid,dsttid=dsttid,log=logger)
        print("start_copy sync_config_algo")
        sync_config_algo.start_copy(srcurl=src_mongo_url,dsturl=dst_mongo_url,srctid=srctid,dsttid=dsttid,log=logger)
    elif control==2:
        algo_word_sync.start_copy(srcurl=src_word_url,dsturl=dst_word_url,srctid=srctid,dsttid=dsttid,log=logger)
    elif control==3:
        es_info_sync.start_copy(srcurl=src_es_url,dsturl=dst_es_url,srctid=srctid,dsttid=dsttid,log=logger)
    elif control==4:
        sync_synonym.start_copy(srcurl=src_mongo_url,dsturl=dst_mongo_url,srctid=srctid,dsttid=dsttid,log=logger)
    elif control==5:
        sync_config_algo.start_copy(srcurl=src_mongo_url,dsturl=dst_mongo_url,srctid=srctid,dsttid=dsttid,log=logger)