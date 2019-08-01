import os


def concat_abs_path(abs_path_1: str, *abs_paths: iter) -> str:
    """
    拼接绝对路径
    :param abs_path_1:路径
    :param abs_paths:拼接段
    :return: 绝对路径
    """

    def get_path(path):
        fspath = os.fspath(path)
        fspath = fspath.strip('\\/') or fspath
        return fspath

    return os.path.abspath(os.path.join(abs_path_1, *(list(map(get_path, abs_paths)))))
