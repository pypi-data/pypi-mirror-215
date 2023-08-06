# pymod112

一个基于Python开发的公民身份号码检验与地区代码查找程序

## 安装 Installation

使用pip安装

```sh
pip install pymod112
```

## 使用 Usage

基础使用

```python
import pymod112

pymod112.mod112('11010519491231002X', details=True)
'''返回值为(dict)
{'id': '11010519491231002X', 
 'province': ['11', '北京市'], 
 'city': ['01', ''], 
 'county': ['05', '朝阳区'], 
 'birth_date': ['1949', '12', '31'], 
 'gender': 0, 
 'result': True, 
 'problem': '000'}
'''

```

拓展功能(查询地区代码对应的地区名)

```python
import pymod112

pymod112.code_to_location(['51', '01', '06'])
'''返回值为(list)
['四川省', '成都市', '金牛区']
'''
```

## 许可证 License
BSD 3-Clause License
