"""
__Date__ : 2017/7/8
__Author__ : linyu
"""

from os.path import join as pjoin
from os.path import abspath

ROOT_DIR = abspath(pjoin(abspath(__file__), '..', '..'))
DATA_DIR = abspath(pjoin(ROOT_DIR, 'data'))
LOG_DIR = abspath(pjoin(ROOT_DIR, 'log'))
CONF_DIR = abspath(pjoin(ROOT_DIR, 'weibo.config'))
