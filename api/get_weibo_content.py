"""
__Date__ : 2017/7/8
__Author__ : linyu
说明：该脚本用来爬取单条微博的评论以及详细内容
"""

import json
from multiprocessing.pool import Pool

import requests
from lxml import etree

from util.config import get_config
from util.connect_redis import get_redis
from util.get_login_session import login, headers
from util.log_util import get_logger

logger = get_logger('api.' + __file__.split('/')[-1][:-3])


def get_weibo_content(sess, url, weibo_id):
    try:
        page = sess.get(url % weibo_id, headers=headers, timeout=2)
        data = json.loads(page.content.decode('utf-8'))['data']
        # pagenums = data['page']['totalpage']
        # print(pagenums)
        html = str(data['html'])
        tree = etree.HTML(html)
        user_list = tree.xpath(
                '//div[@class="list_ul"]/div[@class="list_li S_line1 clearfix"]/div[@class="list_con"]/div[@class="WB_text"]/a/text()')
        return user_list

    except:
        logger.info('爬取微博%s失败 ！' % weibo_id)


def is_valid_proxy(proxy):
    sess = requests.session()
    sess.proxies = proxy
    try:
        r = sess.get('http://weibo.com/login.php', headers=headers, timeout=2)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def get_valid_session():
    config = get_config()
    proxy = None
    while 1:
        ip = r.spop('ip_list').decode('utf-8')
        if ip[4] == 's':
            proxy = {'https': ip}
        else:
            proxy = {'http': ip}
        if is_valid_proxy(proxy):
            break
    try:
        sess = login(config[0][0], config[0][1], proxy)
        return sess
    except:
        logger.info('代理不成功，登陆失败！！')


def get_comment_with_proxy():
    url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&root_comment_max_id_type=0&page=1'
    sess = get_valid_session()
    weibo_id = r.spop('weibo_id').decode('utf-8')
    print(get_weibo_content(sess, url, weibo_id))


def main():
    pool = Pool()
    pass


if __name__ == '__main__':
    r = get_redis()
    get_comment_with_proxy()
