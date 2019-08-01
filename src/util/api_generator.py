import json
import random

from config import config

mix_keys = [
    '''
    mix_keys是随机生成api的前缀后缀
    {'name': 'Foo', 'pre': 'pre_', 'suf': '_suf'}
    '''
]

words = [
    '''
    api随机生成的名字列表
    '''
]


def get_random_api_name():
    if len(words) == 0:
        init()
    patten = random.choice(mix_keys)
    return '{0}{1}{2}'.format(
        patten['pre'],
        random.choice(words),
        patten['suf'])

def init():
    '''
    以文件配置的形式录入名字列表
    :return:
    '''
    global words
    with open(config.word_path, 'r') as f:
        words = json.load(f)
