import pickle
import time
import os

problem_and_code = {'000':'不存在问题',
                    '001':'参数id类型错误',
                    '002':'参数time_check类型错误',
                    '003':'参数details类型错误',
                    '004':'参数id长度错误',
                    '005':'参数id内容包含非法字符错误',
                    '006':'参数id不合法',
                    '007':'参数id中包含不存在的地区',
                    '008':'参数id中包含不存在的时间'
                    }

def code_to_location(code: list|tuple) -> list:
    '''
    通过中华人民共和国县以上行政区划代码获取对应单位名称(地方名称)\n
    数据来自《2020年12月中华人民共和国县以上行政区划代码》\n
    注：暂无三沙市西沙区和三沙市南沙区代码)\n
    \n
    参数\n
    code: list|tuple -> 将六位代码依顺序两位为一个元素传入\n
    例：'410102'则传入['41', '01', '02']\n
    输出\n
    list -> [<省>, <市>, <县>]\n
    注：不存在地区的返回值为空字符串\n
    '''

    # 参数检查
    ...

    # 查询
    workplace = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    with open('./RegionCode', 'rb') as f:
        region_code: dict = pickle.load(f)  # 例{code:name}
    result = [region_code.get(f'{code[0]}0000', ''), 
              region_code.get(f'{code[0]}{code[1]}00', ''), 
              region_code.get(f'{code[0]}{code[1]}{code[2]}', '')]
    os.chdir(workplace)
    return result
            
def mod112(id: str, time_check: bool=True, details: bool=False) -> bool|dict:
    """
    检验传入的ID是否是符合规范的中华人民共和国公民身份号码。\n
    该检验无法接入公安系统故无法检验传入的ID是否真实存在。\n
    \n
    参数\n
    id: str -> 传入内容即为需要检验的ID，最后一位自动忽略大小写\n
    time_check：bool -> 传入True则会检验时间是否合法以防止出现不存在的时间，时间基准来自于本机\n
    details: bool -> 传入True则会输出一个dict, 传入False则会输出一个bool\n
    输出\n
    bool -> True即表示id合法，False则表示不合法\n
    dict -> {'id':<你传入的id:str>,\n
             'province':[<编号:int>, <名称:str>],\n
             'city':[<编号:int>, <名称:str>],\n
             'county':[<编号:int>, <名称:str>],\n
             'birth_date':[<年:int>, <月:int>, <日:int>],\n
             'gender':<性别:int>,\n
             'result':<检验结果:bool>,\n
             'problem':<问题代码:str>}\n
    注0：不存在的会用空字符串代替\n
    注1：'gender'中1指代男性 0指代女性\n
    注2：获取问题详情请使用problem(code=<问题代码:str>)\n
    注3：问题代码为'000'时表示不存在问题\n
    """

    # 结束函数
    def analyse(code:str='000') -> bool|dict:
        # 参数检查
        ...

        # 输出处理
        if details:
            result = {'id':'',  
                      'province':['', ''], 
                      'city':['', ''], 
                      'county':['', ''],
                      'birth_date':['', '', ''],
                      'gender':'',
                      'result':False,
                      'problem':code}
            if code == '000':
                result['result'] = True
            if code == '001':
                pass
            else:
                result['id'] = id
            if code == '004':
                pass
            else:
                result['birth_date'] = birth_date
                result['gender'] = gender
            if len(location) == 0:
                pass
            else:
                result.update(location)
            return result
        else:
            if code == '000':
                return True
            else:
                return False

    # 参数类型检查
    ...

    # 变量设置
    location = {}

    # 参数预处理
    if len(id) == 18:
        address = [id[:2], id[2:4], id[4:6]]
        birth_date = [id[6:10], id[10:12], id[12:14]]
        gender = int(id[16:17])%2
        check_code = id[17:18]
    else: 
        return analyse('004')

    # 校验1
    calculation_result = 0
    list1 = list(id[:17])
    for position, i in enumerate(list1):  # mod11-2(1)
        calculation_result += int(i)*2**(18-(position+1))
    calculation_result = (12 - (calculation_result % 11)) % 11  # mod11-2(2)
    if check_code in ('x', 'X') and calculation_result == 10:
        pass
    elif str(calculation_result) == check_code:
        pass
    else:
        return analyse('006')

    # 校验2
    location = {'province':[address[0], ''], 'city':[address[1], ''], 'county':[address[2], '']}
    location['province'][1], location['city'][1], location['county'][1] = code_to_location([address[0], address[1], address[2]])
    if location['province'][1] == '':
        return analyse('007')
    
    # 校验3
    if time_check:  # 对出生日期合法性的检查
        if int(birth_date[0]) <= int(time.strftime("%Y", time.localtime())):  # 年
            if int(birth_date[1]) <= 12 and 1 <= int(birth_date[1]):  # 月
                if birth_date[1] in ["01","03","05","07","08","10","12"]:  # 大月
                    if int(birth_date[2]) <= 31 and 1 <= int(birth_date[2]):
                        pass
                    else:
                        return analyse('008')
                elif birth_date[1] in ["04","06","09","11"]:  # 小月
                    if int(birth_date[2]) <= 30 and 1 <= int(birth_date[2]):
                        pass
                    else:
                        return analyse('008')
                else:
                    if int(birth_date[0]) % 4 == 0:  # 闰月
                        if int(birth_date[2]) <= 29 and 1 <= int(birth_date[2]):
                            pass
                        else:
                            return analyse('008')
                    else:  # 平月
                        if int(birth_date[2]) <= 28 and 1 <= int(birth_date[2]):
                            pass
                        else:
                            return analyse('008')
            else:
                return analyse('008')
        else:
            return analyse('008')
    else:
        pass

    # 返回值
    return analyse('000')

def problem(code: str) -> str:
    '''
    用问题代码查找对应的问题详情
    '''

    return problem_and_code[code]


if __name__ == '__main__':
    # 效果演示(实例来自于GB11643-1999)
    # 北京市朝阳区1949年12月31日出生的一女性公民
    print(mod112('11010519491231002X', details=True))
    # 广东省汕头市朝阳县1880年1月1日出生的一男性公民
    print(mod112('440524188001010014', details=True))
