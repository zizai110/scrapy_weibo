"""
__Date__ : 2017/7/8
__Author__ : linyu
说明：此脚本用获取新浪微博账号, config[0], config[1]使用账号
"""


from util.path_util import CONF_DIR


def get_config():
    config = {}
    with open(CONF_DIR) as f:
        conf = [line.strip().split(',') for line in f.readlines()]
        idx = 0
        for item in conf:
            config[idx] = item
            idx += 1
    return config