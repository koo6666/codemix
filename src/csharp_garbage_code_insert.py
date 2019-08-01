import linecache
import logging
import os
import random
import yaml

from config import config
from util.path_util import concat_abs_path


def insert_garbage_code(path):
    def get_random_api_text():
        text = random.choice(api)
        return '{0}//{1}'.format(text.replace('\n', ''),
                                 ''.join(random.sample(text, random.randint(8, 16))).replace('\n', '')) + '\n'

    def roll():
        return random.choice([True, False, False])

    def skip_num(line):
        """
        计算是否遇到不稳定的pattern，如果是 返回1
        :param line:
        :return:
        """
        pattern = ['foreach', 'for', 'if', 'else']
        return len(list(filter(lambda x: x in line, pattern)))

    api = linecache.getlines(config.method_api_out_path)

    insert_points_list = []
    with open('insert.yaml', 'r', encoding='utf-8') as f:
        insert_points_list = yaml.load(f, yaml.SafeLoader)

    for insert_points in insert_points_list:
        file_path = concat_abs_path(path, insert_points['file'])
        insert_points = insert_points['pattern']

        lines = linecache.getlines(file_path)
        out = lines.copy()

        find = False
        method_end_str = ''
        times = 0
        skip = 0
        for index, line in enumerate(lines):
            def validate_line(line):
                return line.find(';') != -1 and line.find('return') == -1

            if find and line == method_end_str:  # 重置函数位置
                find = False
                skip = 0
                continue

            if skip > 0:  # 跳过pattern的下一行
                skip = skip - 1
                continue

            if line.strip().startswith('//'):  # 跳过注释
                continue

            if len(list(filter(lambda x: x in line, insert_points))) > 0:  # 找到函数位置
                find = True
                method_end_str = lines[index + 1].replace('{', '}')  # 函数结束缩进
                times = 0
                continue

            skip = skip_num(line)  # 计算pattern
            if skip > 0:
                continue

            if find and validate_line(line) and roll():  # 找到插入点位置和roll到插入
                for i in range(random.randint(config.insert_min, config.insert_max)):
                    out[index] = out[index] + (line.replace('    ', '\t').count('\t')) * '\t' + get_random_api_text()
                    times = times + 1
        linecache.clearcache()
        with open(file_path, 'w') as f:
            f.writelines(out)
            logging.info('insert:{0} [{1}] times'.format(file_path, times))
