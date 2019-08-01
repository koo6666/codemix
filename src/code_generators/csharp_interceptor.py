import logging
import os
import random
from abc import abstractmethod
from string import Template

from config import config
from code_generators.garbagecodegenerator import GarbageCodeGenerator
from util import api_generator, encode_util

'''
CSharp垃圾代码生成
'''
class FunctionTemplate:
    '''
    插入函数的模板
    '''
    function_content = r'''
    public static $type $function_name()
    {
    $content
    }
    '''
    line_content = r'''
        $line
    '''
    line_template = Template(line_content)
    function_template = Template(function_content)

    @staticmethod
    def get_line(line):
        return FunctionTemplate.line_template.substitute({'line': line})

    @abstractmethod
    def get_function_content(self, **kw):
        pass

    @abstractmethod
    def get_function_type(self):
        pass

    def get_function(self, function_name):
        args = {
            'type': self.get_function_type(),
            'function_name': function_name,
            'content': self.get_function_content()
        }
        return FunctionTemplate.function_template.substitute(args)


class VoidTemplate(FunctionTemplate):

    def get_function_type(self):
        return 'void'

    def get_function_content(self, **kw):
        def get_raw_string(content):
            ret = r'''
        $content
            '''
            return Template(ret).substitute({'content': content})

        def random_line():
            randoms = [
                get_raw_string(
                    'var {0} = {1}+{2};'.format(api_generator.get_random_api_name(), random.random(), random.random())),
                get_raw_string('var {0}{1} = "{2}";'.format(api_generator.get_random_api_name(),
                                                            random.randint(0, 64),
                                                            api_generator.get_random_api_name())),
                get_raw_string(
                    'for(int i=0;i<{0};i++)UnityEngine.Debug.Log("{1}()...");'.format(random.randint(0, 3),
                                                                                      kw['function_name']))
            ]
            return random.choice(randoms)

        content = ''
        for i in range(5):
            content += FunctionTemplate.get_line(random_line())
        return content

    def get_function(self, function_name):
        args = {
            'type': self.get_function_type(),
            'function_name': function_name,
            'content': self.get_function_content(function_name=function_name)
        }
        return FunctionTemplate.function_template.substitute(args)


class IntTemplate(FunctionTemplate):

    def get_function_type(self):
        return 'int'

    def get_function_content(self, **kw):
        content_template = r'''
        var ret = 0;
        for(int i=0;i<$n;i++)
        ret+=i;
        return ret;
        '''
        return Template(content_template).substitute({'n': random.randint(16, 64)})


class BoolTemplate(FunctionTemplate):
    def get_function_type(self):
        return 'bool'

    def get_function_content(self, **kw):
        content_template = r'''
        var ret = true;
        for(int i=0;i<$n;i++)
            ret = !ret;
        return ret;
                '''
        return Template(content_template).substitute({'n': random.randint(0, 16)})


method_templates = {
    'void': VoidTemplate(),
    'int': IntTemplate(),
    'bool': BoolTemplate()
}


def random_method(filters=None):
    method_name = api_generator.get_random_api_name()
    if filters is not None:
        while method_name in filters:
            method_name = api_generator.get_random_api_name()
    filters.add(method_name)
    template = random.choice(list(method_templates.values()))
    return template.get_function(method_name)


def random_class(class_name, method_count):
    class_template_content = r'''
public class $class_name
{
    $methods
}
    '''
    class_template = Template(class_template_content)
    method_names = set()
    methods = ''
    for i in range(method_count):
        methods += '\n{0}\n'.format(random_method(filters=method_names))
    return class_template.substitute({'class_name': class_name, 'methods': methods}), method_names


class CSharpGarbageCodeGenerator(GarbageCodeGenerator):
    def generate_code(self, src_file_path, target_file_path):
        encoding = encode_util.get_encode(src_file_path)
        file_name = os.path.splitext(os.path.basename(src_file_path))[0]
        method_count = random.randint(config.mix_api_min, config.mix_api_max)
        class_name = file_name + api_generator.get_random_api_name()
        class_content, methods = random_class(class_name, method_count)

        content = ''
        with open(src_file_path, 'r', encoding=encoding, errors='ignore') as f:
            for line in f.readlines():
                content += line
        content += class_content
        with open(target_file_path, 'w', encoding=encoding) as f:
            f.write(content)
        logging.info('Mixing file:{0} is completed and generate {1} methods.'.format(src_file_path, method_count))
        return list(map(lambda x: '{0}.{1}();\n'.format(class_name, x), methods))
