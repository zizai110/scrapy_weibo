"""
__Date__ : 2017/7/8
__Author__ : linyu
说明：该脚本用来获取西刺免费代理并且经过百度进行测试其有效性，同时将有效ip存入redis集合中，键为ip_list
"""
from lxml import etree

import requests

from util.connect_redis import get_redis
from util.log_util import get_logger

logger = get_logger('api.' + __file__.split('/')[-1][:-3])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3103.400 QQBrowser/9.6.11372.400'
}
r = get_redis()


def is_valid_ip(is_http, ip, port):
    proxies = {is_http: is_http + '://' + ip + ':' + port}
    sess = requests.session()
    sess.proxies = proxies
    r = sess.get('http://www.baidu.com', headers=headers)
    if r.status_code == 200:
        return True
    else:
        return False


def get_iplist():
    url = 'http://www.xicidaili.com/nn/%s'
    r.delete('ip_list')
    logger.info('清除redis中所有的过时ip，并开始重新收集有效的ip')
    sess = requests.session()
    idx = 0
    for i in range(2):
        res = sess.get(url % (i + 1), headers=headers)
        tree = etree.HTML(res.content)
        items = tree.xpath('//div[@class="clearfix proxies"]/table//tr')
        for item in items[1:]:
            tds = item.xpath('./td/text()')
            ip = tds[0]
            port = tds[1]
            is_http = tds[5]
            if is_valid_ip(is_http, ip, port):
                r.sadd('ip_list', is_http.lower() + '://' + ip + ':' + port)
                idx += 1
        logger.info("有效ip到现在有%s个" % idx)


if __name__ == '__main__':
    get_iplist()
