import shutil
from abc import abstractmethod


class GarbageCodeGenerator:
    @abstractmethod
    def generate_code(self, src_file_path, target_file_path):
        pass


class DefaultGarbageCodeGenerator(GarbageCodeGenerator):
    def generate_code(self, src_file_path, target_file_path):
        shutil.copy2(src_file_path, target_file_path)
