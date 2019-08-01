import chardet


def get_encode(file_name):
    '''
    获取文本编码
    :param file_name:
    :return:
    '''
    with open(file_name, 'rb') as f:
        return chardet.detect(f.read(256))['encoding']
