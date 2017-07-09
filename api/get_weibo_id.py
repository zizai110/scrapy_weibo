"""
__Date__ : 2017/7/8
__Author__ : linyu
说明：该脚本用来获取待爬取的微博id，并将该id存储至redis库中键为weibo_id的集合中
输入为微博账号和用户名
"""

import json

import time
from lxml import etree

from util.config import get_config
from util.connect_redis import get_redis
from util.log_util import get_logger
from util.get_login_session import login, headers

logger = get_logger('api.' + __file__.split('/')[-1][:-3])


if __name__ == '__main__':
    id_url = 'http://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803_ctg1_1760_-_ctg1_1760&pagebar=0&tab=home&current_page=%d&pre_page=1&page=1&pl_name=Pl_Core_NewMixFeed__3&id=102803_ctg1_1760_-_ctg1_1760&script_uri=/&feed_type=1&domain_op=102803_ctg1_1760_-_ctg1_1760'
    config = get_config()
    sess = login(config[0][0], config[0][1])

    r = get_redis()
    for i in range(100):
        page = sess.get(id_url % i, headers=headers)
        data = json.loads(page.content.decode('utf-8'))['data']
        tree = etree.HTML(data)
        mid = tree.xpath('//div[@class="WB_cardwrap WB_feed_type S_bg2"]/@mid')
        for idx in mid:
            r.sadd("weibo_id", idx)

        if i % 10 == 0:
            logger.info("第%s页的微博id存入redis库中......" % (i + 1))
    time.sleep(0.2)
