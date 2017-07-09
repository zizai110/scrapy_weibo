"""
__Date__ : 2017/7/8
__Author__ : linyu
说明：此脚本用来进行微博模拟登陆使用
"""

import base64
import json
import re
import time
from lxml import etree
from urllib.parse import quote_plus

import binascii

import requests
import rsa

from util.log_util import get_logger

logger = get_logger('api.' + __file__.split('/')[-1][:-3])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'}


def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


def get_server_data(su, session):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    pre_url += str(int(time.time() * 1000))
    pre_data_res = session.get(pre_url, headers=headers)
    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))
    return sever_data


def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


def login(username, password, proxies=None):
    index_url = "http://weibo.com/login.php"
    session = requests.session()
    session.proxies = proxies
    try:
        session.get(index_url, headers=headers, timeout=2)
    except:
        session.get(index_url, headers=headers)

    su = get_su(username)
    sever_data = get_server_data(su, session)
    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    password_secret = get_password(password, servertime, nonce, pubkey)

    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    login_page = session.post(login_url, data=postdata, headers=headers)
    login_loop = (login_page.content.decode("GBK"))
    pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    loop_url = re.findall(pa, login_loop)[0]

    login_index = session.get(loop_url, headers=headers, timeout=2)
    uuid = login_index.text
    uuid_pa = r'"uniqueid":"(.*?)"'
    uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
    weibo_page = session.get(web_weibo_url, headers=headers, timeout=2)

    weibo_pa = r'<title>(.*?)</title>'
    userID = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    logger.info("用户%s已经成功登陆！" % userID)

    return session


def get_example(session):
    url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=4117589250507557&root_comment_max_id_type=0&page=1'
    page = session.get(url.format(10000), headers=headers)
    data = json.loads(page.content.decode('utf-8'))['data']
    pagenums = data['page']['totalpage']
    print(pagenums)
    html = str(data['html'])

    tree = etree.HTML(html)
    user_list = tree.xpath(
            '//div[@class="list_ul"]/div[@class="list_li S_line1 clearfix"]/div[@class="list_con"]/div[@class="WB_text"]/a/text()')
    return user_list


if __name__ == '__main__':
    username = input("用户名:")
    password = input('密码:')
    login(username, password)
