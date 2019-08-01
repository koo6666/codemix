import logging
import os
import shutil
from collections import defaultdict
from multiprocessing import Pool, cpu_count

from config import config
from code_generators.csharp_interceptor import CSharpGarbageCodeGenerator
from code_generators.garbagecodegenerator import DefaultGarbageCodeGenerator
import csharp_garbage_code_insert

interceptors = defaultdict(DefaultGarbageCodeGenerator)
default_interceptor = DefaultGarbageCodeGenerator()


def init():
    '''
    初始化配置
    :return:
    '''
    if os.path.exists(config.target_path):
        shutil.rmtree(config.target_path)
        logging.info('Work dir exist.Clearing...')
    if not os.path.exists(config.target_path):
        os.mkdir(config.target_path)
        logging.info('Create work dir.')
    if os.path.exists(config.method_api_out_path):
        os.remove(config.method_api_out_path)
        logging.info('Remove out put api file.')
    # 注册混淆拦截器
    interceptors['.cs'] = CSharpGarbageCodeGenerator()

    logging.info('Configure complete.')


def garbage_code_generate(src_path, target_path):
    def mkdir(file):
        dir_name = os.path.dirname(file)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def out_put_api():
        api = None
        while True:
            lines = yield api
            if lines is None:
                continue
            with open(config.method_api_out_path, 'a+', encoding='utf-8') as f:
                f.writelines(lines)

    def ignore(file):
        dir_name = os.path.dirname(file)
        for x in config.ignore_dirs:
            if x in dir_name:
                return True
        return False

    writer = out_put_api()
    next(writer)

    worker = Pool(cpu_count() * 2)
    if not config.parallel:
        worker.terminate()
        worker = None

    for root, dirs, files in os.walk(src_path):
        for file in files:
            file_name, file_type = os.path.splitext(file)
            src_file_path = os.path.join(root, file)
            target_file_path = src_file_path.replace(src_path, target_path)

            if ignore(src_file_path):
                dir_name = os.path.dirname(src_file_path)
                logging.info('Ignore dir:{0} file:{1}'.format(dir_name, file))

            mkdir(target_file_path)
            interceptor = interceptors[file_type]
            if ignore(src_file_path):
                dir_name = os.path.dirname(src_file_path)
                logging.info('Ignore dir:{0} file:{1} act by DefaultInterceptor.'.format(dir_name, file))
                interceptor = default_interceptor

            logging.debug('mixing file:{0} by {1}'.format(src_file_path, interceptor.__class__))
            if worker is not None:
                worker.apply_async(interceptor.generate_code, args=(src_file_path, target_file_path,),
                                   callback=lambda x: writer.send(x) if x is not None else 0)
            else:
                writer.send(interceptor.generate_code(src_file_path, target_file_path))
    if worker is not None:
        worker.close()
        worker.join()


def mix():
    '''
    混淆
    :return:
    '''
    garbage_code_generate(config.src_path, config.target_path)
    csharp_garbage_code_insert.insert_garbage_code(config.target_path)


def clear():
    '''
    执行之后的后续清理工作
    :return:
    '''
    if os.path.exists(config.method_api_out_path):
        os.remove(config.method_api_out_path)
        logging.info('Clear api out put file.')


def main():
    init()
    mix()
    clear()


if __name__ == '__main__':
    main()
