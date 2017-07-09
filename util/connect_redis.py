import redis

from util.log_util import get_logger

logger = get_logger('api.'+__file__.split('/')[-1][:-3])


def get_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        logger.info("成功连接redis数据库！")
        return r
    except:
        logger.info('redis数据库连接失败！')


if __name__ == '__main__':
    r = get_redis()
    r.sadd('weibo_id', '1')
    r.sadd('weibo_id', '2')