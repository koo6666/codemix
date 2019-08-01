import logging
import os
from configparser import ConfigParser
import collections

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s:%(message)s')


def _two_abs_join(abs1, abs2):
    """
    将绝对路径将两个绝对路径拼接,
    就是将第二个的开路径（windows 的  C， D，E ... Linux 的 /root 最前面的 / 删除掉）
    :param abs1:  为主的路径
    :param abs2:  被拼接的路径
    :return: 拼接后的数值
    """
    # 1. 格式化路径（将路径中的 \\ 改为 \）
    abs2 = os.fspath(abs2)

    # 2. 将路径文件拆分
    abs2 = os.path.splitdrive(abs2)[1]
    # 3. 去掉开头的 斜杠
    abs2 = abs2.strip('\\/') or abs2
    return os.fspath(os.path.join(abs1, abs2))


class Config:
    __args = collections.defaultdict(lambda: lambda parser, section, option: parser.get(section, option))
    __args['ignore_dirs'] = lambda parser, section, option: parser.get(section, option).split(',')
    __args['parallel'] = lambda parser, section, option: parser.getboolean(section, option)
    __args['mix_api_max'] = lambda parser, section, option: parser.getintg(section, option)
    __args['mix_api_max'] = lambda parser, section, option: parser.getint(section, option)
    __args['insert_min'] = lambda parser, section, option: parser.getint(section, option)
    __args['insert_max'] = lambda parser, section, option: parser.getint(section, option)

    def __init__(self):
        self.project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        self.word_path = _two_abs_join(self.project_path, '/resource/word_list.json')
        self.method_api_out_path = _two_abs_join(self.project_path, '/api.txt')
        self.mix_api_max = 50
        self.mix_api_min = 20
        self.insert_min = 1
        self.insert_max = 5
        self.insert_point_config = '/insert.yaml'
        self.parallel = True
        # self.ignore_dirs = {'Tpls', 'PostProcessing'}

    def config(self):
        parser = ConfigParser()
        parser.read('config.ini')
        for x in parser.options('config'):
            self.__setattr__(x, Config.__args[x](parser, 'config', x))

        logging.info('project_path:{0}'.format(self.project_path))
        logging.info('src_path:{0}'.format(self.src_path))
        logging.info('target_path:{0}'.format(self.target_path))
        logging.info('method_api_out_path:{0}'.format(self.method_api_out_path))
        logging.info('ignore dirs:{0}'.format(self.ignore_dirs))
        logging.info('random api count:{0} - {1}'.format(self.mix_api_min, self.mix_api_max))
        logging.info('insert api count:{0} - {1}'.format(self.insert_min, self.insert_max))
        logging.info('parallel:{0}'.format(self.parallel))


config = Config()
config.config()
