# codemix
一个简单的代码混淆脚本  
C#垃圾代码生成，可以指定代码插入点引入垃圾代码调用

# install
>pip install chardet  
 pip install pyyaml


# config property
+ src_path：源文件目录
+ target_path：输出目录
+ ignore_dirs：忽略处理的文件夹目录，多个用“,”隔开
+ method_api_out_path：混淆api输出目录，不填默认脚本根目录
+ mix_api_max：生成垃圾api的最大数量，默认50
+ mix_api_min：生成垃圾api的最少数量，默认20
+ parallel:多进程并行执行开关（ture/false）默认开启
+ insert_min：api 每次插入最少数 默认1
+ insert_max：api 每次插入最大数 默认5
+ insert_point_config：插入点配置文件，默认/src/insert.yaml
+ word_path：随机API词库

# insert_point_config sample

```yaml

---
-
  file: /com/Foo.cs
  pattern:
    - void Start()
    - private void init()
```