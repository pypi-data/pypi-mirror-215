# coding:utf-8

# @Auther:liyubin
# @Time: 2023/6/9 15:29


# write your function this file


import json
import platform
import logging
import os.path
import sys
import time
from os import mkdir

from lite_app.lib.struct import *  # json2dict时发现
from lite_app.lib.c import *
from lite_app.util.run_common_obj_per import RunDbFileCase
import gc

# from memory_profiler import profile  # 调试内存占用

"""
 run case-》持久化-》打包-》运行

 C++测试用例持久化打包运行
"""

"""
变量配置
"""

IS_WRITE = False
IS_LITE_RUN = False
WORK_PLACE = ''

if IS_WRITE:
    WORK_PLACE = os.path.dirname(os.path.abspath(__file__))  # 当前工作空间
else:
    work_place = './work_place.json'  # 通过配置驱动
    print('./work_place.json is exists: ', os.path.exists(work_place))
    if os.path.exists(work_place):
        with open(work_place, 'r') as fp_wp:
            fp_wp_json = json.load(fp_wp)
        WORK_PLACE = fp_wp_json.get('work_place')
        print('work_place.json', WORK_PLACE)
        IS_LITE_RUN = fp_wp_json.get('is_lite_run')
        EXECUTION_APP_PLACE = fp_wp_json.get('execution_app')
    else:
        work_place = './is_write.json'
        if os.path.exists(work_place):
            with open(work_place, 'r') as fp_wp:
                fp_wp_json = json.load(fp_wp)
            WORK_PLACE = fp_wp_json.get('work_place')
            IS_WRITE = True
    # WORK_PLACE = r'D:\Program Files (x86)\scada\bin\lite_app'  # 当前工作空间 写死完整路径  打包成 exe 后运行空间到了 c盘下temp了，所以写死

"""
日志初始化
"""


# @profile
def today():
    if IS_LITE_RUN:
        return 'log'  # lite中运行时固定一个日志文件
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')


# @profile
def set_log(logger_, log_path):
    if not os.path.exists(log_path):
        mkdir(log_path)

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: #  %(message)s')

    # 文件日志
    # log_file = Path(log_path) / f'{today()}.log'
    log_file = os.path.join(log_path, '{}.log'.format(today()))
    file_handler = logging.FileHandler(filename=log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger_.addHandler(file_handler)
    logger_.addHandler(console_handler)

    # 指定日志的最低输出级别，默认为WARN级别
    # DEBUG，INFO，WARNING，ERROR，CRITICAL
    logger_.setLevel(logging.INFO)


# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("lite_app")

set_log(logger, 'log')

"""
全局变量初始化
"""


# @profile
def now():
    t = time.time()
    return time.strftime("@%Y%m%d_%H%M%S", time.localtime(t))


# @profile
def timestamp():
    # js 格式的时间戳
    return int(time.time() * 1000)


class Global:
    def __init__(self):
        self.start_time = now()
        self.start_timestamp = timestamp()
        self.plan_name = ''
        self.sheet_name = ''
        self.plan_data = {}
        self.testsuite_data = {}
        self.no = 1
        self.driver = ''
        self.mqtt_client_ = ''
        self.ctypes_client = None
        self.modbusTcpClient = None
        self.modbusRtuClient = None
        self.work_place = None

    def init(self, desired_caps, server_url):
        self.desired_caps = desired_caps
        self.server_url = server_url
        self.platform = desired_caps.get('platformName', '')
        self.browserName = desired_caps.get('browserName', '')
        self.headless = desired_caps.pop('headless', False)
        self.snapshot = desired_caps.pop('snapshot', False)
        self.executable_path = desired_caps.pop('executable_path', False)
        self.deviceName = desired_caps.get('deviceName')
        self.appPackage = desired_caps.get('appPackage')

    def set_driver(self):
        self.var = {'_last_': False}
        self.snippet = {}
        self.current_page = '通用'
        self.db = {}
        self.http = {}
        self.baseurl = {}
        self.action = {}

        # mqtt已在servers/mqtt_client.py中初始化 以及 设置全局变量 self.mqtt_client_

    def plan_end(self):
        self.plan_data['plan'] = self.plan_name
        # self.plan_data['task'] = self.start_timestamp
        self.plan_data['start_timestamp'] = self.start_timestamp
        self.plan_data['end_timestamp'] = int(time.time() * 1000)

        return self.plan_data


# @profile
def json2dict(s):
    if isinstance(s, dict):
        return s
    s = str(s)
    d = {}
    try:
        d = json.loads(s)
    except:
        try:
            d = eval(s)
        except:
            s = s.replace('true', 'True').replace('false', 'False').replace(
                'null', 'None').replace('none', 'None')
            d = eval(s)
    return d


"""
页面变量初始化
"""


class PageVariables:

    def __init__(self, page_variables=None, g=None):
        if page_variables is None:
            page_variables = {}
        self.page_variables = page_variables
        self.g = g

    def get(self, page_var, flag=False):
        ele = page_var.split('#')
        # #号后面的值，即用户输入的变量
        _v = []
        # 支持多个变量替代，但是顺序要对应
        if len(ele) >= 2:
            _el = ele[0] + '#'
            _v = ele[1:]
        else:
            _el = page_var
        el = self.page_variables.get(_el, '')
        if not el:
            if flag:
                return _el, ''
            return _el, page_var.split('#', 1)[-1]
        value = el['value']
        for v in _v:
            v = '#' if v == '^' else v  # 当 value 中的 # 无需替换时，用例中的页面变量使用 ^ 表示
            value = value.replace('#', v, 1)
        return el, self.replace_(value)

    def replace_(self, data):
        import re
        if data.startswith("'''") and data.endswith("'''"):
            return data[3:-3]

        left_angle = 'dsfw4rwfdfstg43'
        right_angle = '3dsdtgsgt43trfdf'
        left_delimiter = '<'
        right_delimiter = '>'
        data = data.replace(r'\<', left_angle).replace(r'\>', right_angle)

        if '<<' in data and '>>' in data:
            left_delimiter = '<<'
            right_delimiter = '>>'

            # 正则匹配出 data 中所有 <> 中的变量，返回列表
        keys = re.findall(r'%s' % (left_delimiter + '(.*?)' + right_delimiter), data)
        _vars = {}

        for k in keys:
            k = k.replace(left_angle, '<').replace(right_angle, '>')
            # 正则匹配出 k 中的 + - ** * // / % , ( ) 返回列表
            values = re.split(r'(\+|-|\*\*|\*|//|/|%|,|\(|\))', k)
            for v in values:
                # 切片操作处理，正则匹配出 [] 中内容
                s = v.split('[', 1)
                index = ''
                if len(s) == 2:
                    v = s[0]
                    index = '[' + s[1]

                if v in self.g.var and v not in _vars:
                    # 如果在 var 中是 list
                    if v.startswith('_') and isinstance(self.g.var[v], list) and not index:
                        # 是测试数据文件中的值，则 pop 第一个值
                        if len(self.g.var[v]) == 0:
                            raise Exception('The key:%s is no value in data csv' % v)
                        elif len(self.g.var[v]) == 1:
                            _vars[v] = self.g.var[v][0]
                            self.g.var['_last_'] = True
                        else:
                            _vars[v] = self.g.var[v].pop(0)

                    else:
                        _vars[v] = self.g.var[v]

            try:
                value = eval(k, globals(), _vars)
            except NameError:
                value = left_delimiter + k + right_delimiter

            if data == left_delimiter + keys[0] + right_delimiter:
                data = value
            # 否则需要替换，此时变量强制转换为为字符串
            else:
                data = data.replace(left_delimiter + k + right_delimiter, str(value))
                data = data.replace(left_angle, '<').replace(right_angle, '>')
        # testcase 中写 <\> 让autotest支持 字符<>
        data = data.replace(left_angle, '<').replace(right_angle, '>')
        return data


"""
 ctypes动态连接库 初始化
"""


class CtypesInit:

    def __init__(self, data):
        self.ctypes_client = None
        self.data = data
        self.dll_name = self.data.get('file', 'no dll file')

    # @profile
    def setup_ctypes_client(self, work_place):
        """初始化ctypes动态连接库"""
        if platform.system().lower() == 'windows':
            self.dll_name = '{}.dll'.format(self.dll_name)
        else:
            self.dll_name = 'lib{}.so'.format(self.dll_name)

        os.chdir(work_place)  # 连续加载dll先切回初始路径

        time.sleep(0.5)
        os.chdir('../')  # scada/bin/project/testcase/*.py 运行后切换到工作空间scada/bin, 最后写报告时切回./project

        dll_path = os.path.join('./', self.dll_name)
        assert os.path.exists(dll_path), 'C++文件不存在：{} \n'.format(dll_path) + "请检查C++文件：{}".format(
            self.dll_name) + ", 参数示例：json={'file': 'filename.dll'},,"
        self.ctypes_client = CDLL(dll_path)
        logger.info("--- Ctypes loaded {} Success ---".format(str(self.ctypes_client)))
        return self.ctypes_client  # 设置全局变量


"""
ctypes keywords
"""


class RunCase(RunDbFileCase):

    def __init__(self):
        super().__init__(logger)
        self.g = {}
        self.ctypes_client = None  # 不写在g里防止每次持久化覆盖
        self.is_load_c = False  # 如加载了dll 则执行 c++的 teardown
        self.testcase_title = 'None'
        self.data = None
        self.expected_ = None
        self.step = None
        self.IS_WRITE = IS_WRITE  # 是否只是写持久化
        self.WORK_PLACE = WORK_PLACE
        self.step_index = 0  # 持久化中总 step 数
        self.now_step_index = 0  # 持久化读到的 step_index 的次数就是 coll_c 次数，每次按index取step持久化
        self.setup_step_index_now_ = 0  # 可能有多个 setup 直到前置取不到值说明，前置结束
        self.teardown_step_index_now_ = 0
        self.now_teardown = False  # 当 True 最后只运行teardown内容
        self.now_load_c_data = ''  # 可以支持多个setup， 但 重新加载load_c 不同时，清空setup 并从0 开始
        self.report_summary = {}  # 报告汇总

    # @profile
    def setup_obj_persistence(self, kw, step):
        """持久化数据准备"""
        import json
        os.chdir(self.WORK_PLACE)
        ########################################################################
        # 对象持久化 在 json2dict 前
        # logger.info('--- {} , WORK_PLACE: {} ---'.format('Write' if self.IS_WRITE else 'Read', self.WORK_PLACE))
        if not self.IS_WRITE and not os.path.exists(os.path.join('./', '{}.json'.format(kw))):
            logger.warning('---不存在持久化文件: {}.dir ---'.format(kw))

        # 对象持久化 写
        if self.IS_WRITE:
            with open('page_variables.json', 'r') as fp11:
                e_json = json.load(fp11)
                e = PageVariables(e_json, self.g)

            # c++ 步骤数据准备
            if step['keyword'].lower() in ('load_c', 'call_c'):
                data = step['data']
                expected_ = step['expected']

                # 测试数据解析时，会默认添加一个 text 键，需要删除
                if 'text' in data and not data['text']:
                    data.pop('text')

                # 全局变量替换, 在json2dict前还未执行函数
                page_var_key_str = step['page_variables']
                page_var_key_list = []
                if len(page_var_key_str) > 0:
                    page_var_key_list = page_var_key_str.split(',,')  # 多个页面变量默认约定格式 var1,,var2

                for page_var_key in page_var_key_list:
                    page_name = step.get('page', 'no page')
                    if '{}-'.format(page_name) not in page_var_key:
                        page_var_value = e.get('{}-{}'.format(page_name, page_var_key), ())[1]
                    else:
                        page_var_value = e.get('{}'.format(page_var_key), ())[1]
                    if page_var_value:
                        page_var_key = page_var_key.replace('{}-'.format(step.get('page', 'no page')), '')

                        # 测试数据变量替换
                        data_json_ = data.get('json', '{}')
                        if data_json_ != '{}':
                            data['json'] = data_json_.replace('<{}>'.format(page_var_key), page_var_value)

                        # 预期值变量替换
                        except_json_ = expected_.get('json', '{}')
                        if except_json_ != '{}':
                            expected_['json'] = except_json_.replace('<{}>'.format(page_var_key), page_var_value)
            # sql 步骤数据准备
            elif step['keyword'].lower() == 'sql':
                kw = 'call_c'  # 因为步骤都写在call_c.json中
                page_var = step['page_variables']
                _sql = e.get(page_var)[1]
                _content_value = e.get(step['page'] + '-' + 'config')[1]
                data = {}
                expected_ = {}
                step.update({'_sql': _sql, '_content_value': _content_value})
            else:
                return

            # 用例标题步骤
            with open('testcase_title.json', 'r') as fp10:
                testcase_data = json.load(fp10)
                testcase_title = testcase_data.get('testcase_title', 'no testcase title')
                self.step_index = testcase_data.get('step_index', 0)

            data_json = {'testcase_title': testcase_title, 'data': data, 'expected_': expected_, 'step': step,
                         'step_index': self.step_index}

            # 重置
            if self.step_index == 0 or not os.path.exists('{}.json'.format(kw)):  # 不存在的情况
                with open('{}.json'.format('load_c'), 'w') as fp_0:
                    json.dump({'step_index': 0}, fp_0)
                with open('{}.json'.format('call_c'), 'w') as fp_00:
                    json.dump({'step_index': 0}, fp_00)

            if self.setup_step_index_now_ == 0 or not os.path.exists('{}.json'.format('setup_c')) or (
                    kw == 'load_c' and self.now_load_c_data != data) or self.step_index == 0:
                # 初始、不存在、load_c 变化时 都重置setup,teardown，可以支持多个setup， 但重新加载load_c 不同时，清空setup 并从0 开始
                self.setup_step_index_now_ = 0
                with open('{}.json'.format('setup_c'), 'w') as fp_01:
                    json.dump({}, fp_01)

            if self.teardown_step_index_now_ == 0 or not os.path.exists('{}.json'.format('teardown_c')) or (
                    kw == 'load_c' and self.now_load_c_data != data):
                self.teardown_step_index_now_ = 0
                with open('{}.json'.format('teardown_c'), 'w') as fp_01_t:
                    json.dump({}, fp_01_t)

            # 读历史
            if kw == 'call_c' and step.get('score', '') == 'STEP_SETUP':
                with open('{}.json'.format('setup_c'), 'r') as fp_1:
                    data_json_old = json.load(fp_1)
            elif kw == 'call_c' and step.get('score', '') == 'STEP_TEARDOWN':
                with open('{}.json'.format('teardown_c'), 'r') as fp_1_t:
                    data_json_old = json.load(fp_1_t)
            else:
                with open('{}.json'.format(kw), 'r') as fp_1:
                    data_json_old = json.load(fp_1)

            # 记录当前 dll 信息，不同时重置 setup
            if kw == 'load_c':
                self.now_load_c_data = data

            # 前后置有独立的 index初始
            if step.get('score', '') == 'STEP_SETUP':
                step_index_1 = self.setup_step_index_now_
            elif step.get('score', '') == 'STEP_TEARDOWN':
                step_index_1 = self.teardown_step_index_now_
            else:
                step_index_1 = self.step_index

            data_json_old['step_index'] = step_index_1
            data_json_old['step_index_now_{}'.format(step_index_1)] = data_json

            # 写
            if kw == 'call_c' and step.get('score', '') == 'STEP_SETUP':
                with open('{}.json'.format('setup_c'), 'w') as fp_kw:
                    json.dump(data_json_old, fp_kw)
            elif kw == 'call_c' and step.get('score', '') == 'STEP_TEARDOWN':
                with open('{}.json'.format('teardown_c'), 'w') as fp_kw:
                    json.dump(data_json_old, fp_kw)
            else:
                with open('{}.json'.format(kw), 'w') as fp_kw1:
                    json.dump(data_json_old, fp_kw1)

            if step.get('score', '') == 'STEP_SETUP':
                self.setup_step_index_now_ += 1
            elif step.get('score', '') == 'STEP_TEARDOWN':
                self.teardown_step_index_now_ += 1
            else:
                self.step_index += 1  # 每次写step_index加1，读的时候按这个次数获取持久化数据
            os.chdir('../')  # 加载完持久化切换到 scada/bin 下
            return False

        # 对象持久化 读
        # teardown
        if kw == 'call_c' and self.now_teardown:
            with open('{}.json'.format('teardown_c'), 'r') as fp_kw2:
                data_json = json.load(fp_kw2)
            if data_json != {}:
                teardown_step_index_now_ = 'step_index_now_{}'.format(self.teardown_step_index_now_)
                step_index_now_json = data_json.get(teardown_step_index_now_, 'no index setup')
                if step_index_now_json != 'no index setup':
                    self.testcase_title = step_index_now_json.get('testcase_title')
                    self.data = step_index_now_json.get('data')
                    self.expected_ = step_index_now_json.get('expected_')
                    self.step = step_index_now_json.get('step')
                    self.teardown_step_index_now_ += 1
                else:
                    logger.warning('not teardown data')
                    return False
                logger.info('--- teardown start ---')
                return True
        # setup
        step_index_now_json = 'no index setup'
        if kw == 'call_c':  # 先读 setup 存在性，每次执行 call_c 前都运行 setup， 因为每次加载 dll 都需要前置
            with open('{}.json'.format('setup_c'), 'r') as fp_kw2:
                data_json = json.load(fp_kw2)

            if data_json != {}:
                setup_step_index_now_ = 'step_index_now_{}'.format(self.setup_step_index_now_)
                step_index_now_json = data_json.get(setup_step_index_now_, 'no index setup')
                if step_index_now_json != 'no index setup':
                    self.testcase_title = step_index_now_json.get('testcase_title')
                    self.data = step_index_now_json.get('data')
                    self.expected_ = step_index_now_json.get('expected_')
                    self.step = step_index_now_json.get('step')
                    self.setup_step_index_now_ += 1
        # case
        if step_index_now_json == 'no index setup':  # 前置为空 走正常流程
            step_index_now_ = 'step_index_now_{}'.format(self.now_step_index)
            with open('{}.json'.format(kw), 'r') as fp_kw4:
                data_json = json.load(fp_kw4)

            step_index_now_json = data_json.get(step_index_now_)
            if step_index_now_json:
                step_index_now_json_ = step_index_now_json
            else:
                logger.info('retry add load_c.json... {}'.format(kw))
                # 说明用例第一步不是c++ 的load_c，直接加载 call_c 走其他关键字
                with open('{}.json'.format('call_c'), 'r') as fp_kw5:
                    data_json = json.load(fp_kw5)
                step_index_now_json_ = data_json.get(step_index_now_)
                if not step_index_now_json_:
                    return False  # 说明真的没有步骤了

            self.testcase_title = step_index_now_json_.get('testcase_title')
            self.data = step_index_now_json_.get('data')
            self.expected_ = step_index_now_json_.get('expected_')
            self.step = step_index_now_json_.get('step')
            if self.step_index == 0 and step_index_now_json_.get('step_index', 0) == 0:
                self.step_index = 1  # 总step数量, 首次添加
            else:
                self.step_index = data_json.get('step_index', 1)

        # 首次读默认值
        if not self.g:
            self.g = Global()
            self.g.set_driver()  # 初始化 var
        return True
        ########################################################################

    # @profile
    def main(self, kw, step):
        """主入口关键字实际执行函数"""
        try:
            flag = self.setup_obj_persistence(kw, step)
            if not flag:
                return

            logger.info('--------------------------------------------------')
            logger.info('>>> Run the TestCase: {}'.format(self.testcase_title))
            logger.info('--- step test data: {} ---'.format(self.data))

            data = self.data
            expected_ = self.expected_
            step = self.step
            kw = step.get('keyword', 'ABC').lower()  # 以step中kw为主，因call_c中新增了sql

            _data = {}

            if kw in ('load_c', 'call_c'):
                try:
                    _data['json'] = json2dict(data.get('json', '{}'))
                except Exception as ex:
                    logger.warning('请检查 测试数据、预期结果、输出数据的 值， error{}'.format(str(ex)))

            for k in data:
                for s in ('{', '[', 'False', 'True'):
                    if s in data[k]:
                        try:
                            data[k] = eval(data[k])
                        except:
                            logger.warning('Try eval data failure: %s' % data[k])
                        break

            expected_['json'] = json2dict(expected_.get('json', '{}'))
            timeout = float(expected_.get('timeout', 0))
            expected_['time'] = float(expected_.get('time', 0))
            expected_['text'] = expected_.get('text', None)

            time.sleep(timeout)
            # 加载dll/so
            if kw == 'load_c':
                self.ctypes_client = CtypesInit(_data['json']).setup_ctypes_client(self.WORK_PLACE)
                if self.ctypes_client:
                    self.is_load_c = True

            # 调用dll/so中函数
            if kw == 'call_c':
                response, kwargs_ = self.execute_call_c(_data['json'])
                self.get_response_expect_var(expected_, step, response, kwargs_)

            # 执行sql
            if kw == 'sql':
                self.sql(step, self.g)

            self.report_summary.update({'{}'.format(self.testcase_title): 'success'})  # 记录成功

            # index处理 是否还有其他步骤
            if self.step_index > self.now_step_index:
                self.now_step_index += 1
                time.sleep(2)
                call_c(None)
            if step.get('score', '') == 'STEP_SETUP':  # 如果当前步骤是前置 -1
                self.now_step_index -= 1
                time.sleep(2)
                call_c(None)
        except Exception as ex1:
            self.report_summary.update({'{}'.format(self.testcase_title): 'fail'})  # 记录失败
            logger.info('异常捕获: {}'.format(str(ex1)))
            # 是否还有其他步骤
            if self.step_index > self.now_step_index:
                self.now_step_index += 1
                time.sleep(2)
                call_c(None)
            if step.get('score', '') == 'STEP_SETUP':  # 如果当前步骤是前置 -1
                self.now_step_index -= 1
                time.sleep(2)
                call_c(None)

    # @profile
    def execute_call_c(self, data):
        """
        执行 调用c++方法
        :param data:
        :return: 函数运行结果, 运行结果取值变量
        """
        c_func_name = data.get('c_func_name', '')
        assert '当前C++文件%s \n 请输入C++函数名：c_func_name 的值' if not c_func_name else True

        kwargs = {}  # 返回值取值时使用
        args = []  # 运行函数传值时使用
        for k, v in data.items():
            if k != 'c_func_name':
                # 测试数据中变量替换，如果提取的变量是对象、指针等时，直接在 g.var 中获取原始数据，而不是 '<var>' 方式写在用例中的话 对象就变str了
                if isinstance(v, str) and v.startswith('$'):
                    v = self.g.var.get(v.replace('$', ''), None)
                if 'byref' in k:  # byref.：传给函数 前 加指针， .byref：传给函数 时 加指针
                    args.append(byref(v))
                else:
                    args.append(v)
                kr = k.replace('.byref', '').replace('byref.', '')
                kwargs.update(**{kr: byref(v)} if 'byref.' in k else {kr: v})  # byref.前置时 对象取值也加指针

        # 先组装 eval(func) = g.ctypes_client.动态函数名(),  而不是 g.ctypes_client.c_func_name()
        func = 'self.ctypes_client.{}'.format(c_func_name)
        logger.info('execute c++ func: {}, args: {}, kwargs: {}'.format(func, str(args), str(kwargs)))
        return self.pyramid_run(func, args), kwargs

    # @profile
    def pyramid_run(self, func, kwargs):
        """
        待执行函数与原始数据组装运行
        :param func: 待运行函数
        :param kwargs: 原始参数
        :return: 原始返回值
        """
        os.chdir('../')
        length = len(kwargs)
        if length == 0:
            return eval(func)()
        elif length == 1:
            return eval(func)(kwargs[0])
        elif length == 2:
            return eval(func)(kwargs[0], kwargs[1])
        elif length == 3:
            return eval(func)(kwargs[0], kwargs[1], kwargs[2])
        elif length == 4:
            return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3])
        elif length == 5:
            return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4])
        elif length == 6:
            return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5])
        elif length == 7:
            return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5], kwargs[6])
        elif length == 8:
            return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5], kwargs[6], kwargs[7])
        elif length == 9:
            return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5], kwargs[6], kwargs[7],
                              kwargs[8])
        elif length == 10:
            return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5], kwargs[6], kwargs[7],
                              kwargs[8], kwargs[9])

    # @profile
    def get_response_expect_var(self, expected_, step_, response_, kwargs_):
        """
        预期值处理
        变量处理
        需注意函数返回的数据类型和结构是不定的，在这里只提供通用断言相等、包含、大小、是否返回值 和 全局变量设置
        """

        response = json2dict(response_)  # 函数返回
        kwargs_ = json2dict(kwargs_)  # 对象取值
        full_kwargs_ = kwargs_
        real_kwargs_ = {}
        var = {}  # 存储所有输出变量

        logger.info('Expected: {}'.format(step_["expected"]))

        if expected_['text']:
            logger.info('Response: {}'.format(response))
            if expected_['text'].startswith('*'):
                if expected_['text'][1:] not in response:
                    raise Exception('text | EXPECTED:{}, REAL:{}'.format(repr(expected_["text"]), repr(response)))
            elif expected_['text'].startswith('!'):
                if eval(expected_['text'][1:]) == response:  # 校验不相等，相等抛异常
                    raise Exception('text | EXPECTED:{}, REAL:{}'.format(repr(expected_["text"]), repr(response)))
            else:
                if eval(expected_['text']) != response:  # 函数执行默认返回str、int、bytes，或其他类型通过自定义函数进一步验证
                    raise Exception('text | EXPECTED:{}, REAL:{}'.format(repr(expected_["text"]), repr(response)))

        if expected_['json']:
            real_kwargs_, real_expected_, full_kwargs_ = self.reset_except_response(expected_, response_,
                                                                                    kwargs_)  # 重组预期值和实际值
            logger.info('Response: {}'.format(real_kwargs_))

            # 校验
            result = check(real_expected_, real_kwargs_)
            logger.info('json check result: %s' % result)
            if result['code'] != 0:
                raise Exception(
                    'json | EXPECTED:{}\nREAL:{}\nRESULT: {}'.format(repr(real_expected_), repr(real_kwargs_), result))
            elif result['var']:
                var = dict(var, **result['var'])
                self.g.var = dict(self.g.var, **result['var'])
                logger.info('Json var: {}'.format(repr(result['var'])))

        output = step_['output']
        if output:
            logger.info('output: {}'.format(repr(output)))

        for k, v in output.items():
            if k == 'text':
                v = v.replace('<', '').replace('>', '')
                self.g.var[v] = response
                logger.info('{} var: {}'.format(v, repr(self.g.var[v])))
            if k == 'json':
                sub = json2dict(output.get('json', '{}'))
                result = check(sub, full_kwargs_)  # 对比后变量'<var>' 值变为key，value为full_kwargs_中key对应的value
                var = dict(var, **result['var'])  # 提取到的变量字典
                self.g.var = dict(self.g.var, **result['var'])  # 设置变量字典到全局变量字典中
                logger.info('Json var: {}'.format(repr(result['var'])))

        if var:
            step_['_output'] += '\n||output=' + str(var)

    # @profile
    def reset_except_response(self, expected_, response_, kwargs_, key_name='json'):
        """
        通过预期值结构提取函数运行后对象中的值，组成相同的结构断言
        :return:
        """
        try:
            real_kwargs_ = {}  # 对象按断言所需字段取值后的实际结果
            real_expected_ = {}

            # 按预期expected-> json={k.v: exc_value}中取值方式对kwargs_对象取值, 可能取多次、或设置全局变量，所以组成新的数据结构
            for e_k_, e_v in expected_[key_name].items():
                if type(e_v) in (str, int, float, bool):  # value支持的类型
                    e_k_k_ = e_k_.split('.')[0]  # 用 e_k_ 作为key 因传递一个参会提取多个值，相同时会被覆盖
                    # e_k_v = e_k_.split('.')[1] # e_k_v可能是一层也可能是多层，如：e_k_k_.e_k_v_1.e_k_v_2
                    e_k_v = e_k_[len(e_k_k_) + 1:]

                    if '[' in e_k_k_ and ']' in e_k_k_:  # 对象包含多个数据按index取值
                        e_k_k = e_k_k_.split('[')[0]
                        e_k_k_index = '[{}'.format(e_k_k_.split('[')[1])
                        if e_k_v:
                            e_k_v_v = eval('kwargs_.get(e_k_k){}.{}'.format(e_k_k_index, e_k_v))
                        else:
                            e_k_v_v = eval('kwargs_.get(e_k_k){}'.format(e_k_k_index))
                    else:
                        e_k_k = e_k_k_
                        if e_k_v:
                            e_k_v_v = eval('kwargs_.get(e_k_k).{}'.format(e_k_v))
                        else:
                            e_k_v_v = eval('kwargs_.get(e_k_k)')
                    if isinstance(e_k_v_v, bytes):
                        e_k_v = e_k_v.replace('.', '_')  # 多层级a.b.c时: . 替换 _
                        try:
                            # 默认bytes转str， check不对bytes类型支持
                            real_kwargs_['{}_{}'.format(e_k_k, e_k_v)] = e_k_v_v.decode('utf-8')
                        except Exception as exx:
                            real_kwargs_['{}_{}'.format(e_k_k, e_k_v)] = str(exx)  # 可能非完整bytes类型转str报错
                    else:
                        e_k_v = e_k_v.replace('.', '_')  # 多层级a.b.c时: . 替换 _
                        real_kwargs_['{}_{}'.format(e_k_k, e_k_v)] = e_k_v_v

                    real_expected_['{}_{}'.format(e_k_k, e_k_v)] = e_v

                # 批量断言
                elif isinstance(e_v, list):  # 批量对象取值断言，只支持一层list {list: [{}, {}]}
                    real_kw_list = []
                    real_ex_list = []
                    for e_v_index, e_v_dict in enumerate(e_v):
                        real_expected_batch = {}
                        real_kwargs_batch = {}
                        for e_v_d_k, e_v_d_v in e_v_dict.items():
                            e_v_d_k_k_ = e_v_d_k.split('.')[0]
                            # e_v_d_k_v = e_v_d_k.split('.')[1] # e_k_v可能是一层也可能是多层，如：e_k_k_.e_k_v_1.e_k_v_2
                            e_v_d_k_v = e_v_d_k[len(e_v_d_k_k_) + 1:]

                            if '[' in e_v_d_k_k_ and ']' in e_v_d_k_k_:  # 对象包含多个数据按index取值
                                e_v_d_k_k = e_v_d_k_k_.split('[')[0]
                                e_k_k_index = '[{}'.format(e_v_d_k_k_.split('[')[1])
                                if e_v_d_k_v:
                                    e_k_v_v = eval('kwargs_.get(e_v_d_k_k){}.{}'.format(e_k_k_index, e_v_d_k_v))
                                else:
                                    e_k_v_v = eval('kwargs_.get(e_v_d_k_k){}'.format(e_k_k_index))
                            else:
                                e_v_d_k_k = e_v_d_k_k_
                                if e_v_d_k_v:
                                    e_k_v_v = eval('kwargs_.get(e_v_d_k_k).{}'.format(e_v_d_k_v))
                                else:
                                    e_k_v_v = eval('kwargs_.get(e_v_d_k_k)')

                            if isinstance(e_k_v_v, bytes):
                                e_v_d_k_v = e_v_d_k_v.replace('.', '_')  # 多层级a.b.c时: . 替换 _
                                try:
                                    # 默认bytes转str， check不对bytes类型支持
                                    real_kwargs_batch['{}_{}'.format(e_v_d_k_k, e_v_d_k_v)] = e_k_v_v.decode('utf-8')
                                except Exception as exx1:
                                    # 可能非完整bytes类型转str报错
                                    real_kwargs_batch['{}_{}'.format(e_v_d_k_k, e_v_d_k_v)] = str(exx1)
                            else:
                                e_v_d_k_v = e_v_d_k_v.replace('.', '_')  # 多层级a.b.c时: . 替换 _
                                real_kwargs_batch['{}_{}'.format(e_v_d_k_k, e_v_d_k_v)] = e_k_v_v

                            real_expected_batch['{}_{}'.format(e_v_d_k_k, e_v_d_k_v)] = e_v_d_v

                        real_kw_list.append(real_kwargs_batch)
                        real_ex_list.append(real_expected_batch)

                    real_kwargs_[e_k_] = real_kw_list
                    real_expected_[e_k_] = real_ex_list

            kwargs_.update(real_kwargs_)  # full_kwargs_ 包含了定义的所有参数，不参与断言，只提取变量：指针或结构体等
            return real_kwargs_, real_expected_, kwargs_
        except Exception as ex:
            raise '参数提取异常: {}'.format(str(ex))


"""
在这里并不希望任何意外错误导致运行终止
"""
R = RunCase()


# @profile
def load_c(step=None):
    """加载c++文件 dll/so"""
    try:
        R.main('load_c', step)
    except Exception as ex1:
        logger.warning(str(ex1))


# @profile
def call_c(step=None):
    """调用c++中函数"""
    try:
        R.main('call_c', step)
    except Exception as ex1:
        logger.warning(str(ex1))


# @profile
def teardown(step=None):
    """调用c++中函数"""
    try:
        R.now_teardown = True  # 开始teardown
        if R.is_load_c:
            R.main('call_c', step)
        else:
            logger.info('no teardown')
    except Exception as ex1:
        logger.warning(str(ex1))
    finally:
        # 输出报告汇总
        with open(os.path.join(EXECUTION_APP_PLACE, 'log', 'report_summary.json'), 'w')as fp_rs:
            json.dump(R.report_summary, fp_rs)


"""
连接sql lite （.db、.cfg） 和 执行sql语句
"""


def sql(step=None):
    """执行sql"""
    try:
        R.main('sql', step)
    except Exception as ex1:
        logger.warning(str(ex1))


"""
 injson_ok
"""


def rule(data):
    result = []
    for k in data:
        result.append(data[k]['code'])
    return result


def optimum(sub, result, path):
    from copy import deepcopy
    if path != '/':
        path += '.'

    res = result
    for k in sub:
        result = deepcopy(res)
        temp = res
        res = []
        flag = False
        for data in result:
            if path + k not in data:
                flag = True
                res.append(data)
        if not flag:
            temp.sort(key=lambda d: rule(d))
            return temp[0]
    result.sort(key=lambda d: rule(d))
    return result[0]


def list2dict(data):
    keys = ['[' + str(i) + ']' for i in range(len(data))]
    return dict(zip(keys, data))


def check(sub, parent, sp='/', pp='/'):
    """
    sp: sub_path
    pp: parent_path
    :param sub:
    :param parent:
    :param sp:
    :param pp:
    :return:
    """
    re = {'code': 0, 'result': {}, 'var': {}, 'none': []}
    if sp != '/':
        sp += '.'
    if pp != '/':
        pp += '.'

    def _in(k, data):
        try:
            return eval('data[k]')
        except:
            return ''

    for k, sv in sub.items():
        # 判断键值是否是 <value> 格式，如果是，则表明是变量赋值
        var_flag = isinstance(sv, str) and sv.startswith('<') and sv.endswith('>')
        index = ''
        _k = k

        if '.' in k:
            s = k.split('.')
            for _s in s[1:]:
                if '[' in _s:
                    d = _s.split('[', 1)
                    index += '[\'' + d[0] + '\']' + '[\'' + d[1]
                else:
                    index += '[\'' + _s + '\']'
            if '[' in s[0]:
                k = s[0].split('[', 1)[0]
                index = '[' + s[0].split('[', 1)[1] + index
            else:
                k = s[0]

        elif '[' in k:
            s = k.split('[', 1)
            index = '[' + s[1]
            k = s[0]

        # 预期键不存在
        if sv == '-':
            # 预期键不存在，实际键存在
            if k in parent:
                re['result'][sp + _k] = {'code': 4, 'sv': sv, 'pp': pp + _k, 'pv': parent[k]}

        # 预期键存在
        elif sv == '+':
            # 预期键存在，实际键不存在
            if k not in parent:
                re['result'][sp + _k] = {'code': 3, 'sv': sv, 'pp': None, 'pv': None}

        elif k in parent:
            if index:
                try:
                    pv = eval('parent[k]' + index)
                except:
                    if var_flag:
                        re['var'][sv[1:-1]] = None
                        re['none'].append(sv[1:-1])
                    else:
                        re['result'][sp + _k] = {'code': 3, 'sv': sv, 'pp': None, 'pv': None}
                    continue
            else:
                pv = parent[k]

            code = 0

            if var_flag:
                re['var'][sv[1:-1]] = pv
                continue

            elif isinstance(sv, str):
                if sv.startswith('#'):
                    if sv[1:] == str(pv):
                        code = 1
                elif sv.startswith('<>'):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv == float(sv[2:]):
                        code = 1
                elif sv.startswith('>='):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv < float(sv[2:]):
                        code = 1
                elif sv.startswith('>'):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv <= float(sv[1:]):
                        code = 1
                elif sv.startswith('<='):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv > float(sv[2:]):
                        code = 1
                elif sv.startswith('<'):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv >= float(sv[1:]):
                        code = 1
                elif not isinstance(pv, str):
                    code = 2  # 键值的数据类型不一致
                elif sv.startswith('*'):  # 包含
                    if sv[1:] not in pv:
                        code = 1
                elif sv.startswith('^'):  # 开头包含
                    if not pv.startswith(sv[1:]):
                        code = 1
                elif sv.startswith('$'):
                    if not pv.endswith(sv[1:]):  # 结尾包含
                        code = 1
                elif sv.startswith('\\'):
                    sv = sv[1:]
                elif sv != pv:  # 等于
                    code = 1  # 键值不等

            elif isinstance(sv, int):
                if not isinstance(pv, int):
                    code = 2  # 键值的数据类型不一致
                elif sv != pv:
                    code = 1  # 键值不等

            elif isinstance(sv, float):
                if not isinstance(pv, float):
                    code = 2  # 键值的数据类型不一致
                elif sv != pv:
                    code = 1  # 键值不等

            elif isinstance(sv, list):
                if not isinstance(pv, list):
                    code = 2  # 键值的数据类型不一致

                else:
                    for i in range(len(sv)):  # 把二级列表转换为 dict
                        if isinstance(sv[i], list):
                            sv[i] = list2dict(sv[i])
                    for i in range(len(pv)):  # 把二级列表转换为 dict
                        if isinstance(pv[i], list):
                            pv[i] = list2dict(pv[i])

                    if isinstance(sv[0], dict):  # list 子项为 dict
                        for i, sv_i in enumerate(sv):
                            result = []
                            flag = False
                            for j, pv_i in enumerate(pv):
                                r = check(sv_i, pv_i, sp + _k + '[%s]' % i, pp + _k + '[%s]' % j)
                                if r['code'] == 0:
                                    flag = True
                                    re['var'] = dict(re['var'], **r['var'])
                                    break
                                else:
                                    result.append(r['result'])
                            if result:
                                o = optimum(sv_i, result, sp + k + '[%s]' % i)
                            else:
                                o = {}
                            re['var'] = dict(re['var'], **re['var'])

                            if not flag:
                                re['result'] = dict(re['result'], **o)

                    else:  # list 子项为 int/str/float/None/False/True
                        for v in sv:
                            if v not in pv:
                                code = 5  # 预期的 list 值在实际值的 list 不存在
                                re['result'][sp + _k] = {'code': 5, 'sv': sv, 'pp': pp + _k, 'pv': pv}

            elif isinstance(sv, dict):
                if not isinstance(pv, dict):
                    code = 2  # 键值的数据类型不一致
                else:
                    r = check(sv, pv, sp + k, pp + k)
                    if r['code'] == 0:
                        re['var'] = dict(re['var'], **r['var'])
                        continue
                    else:
                        re['result'] = dict(re['result'], **r['result'])
                        for k in r['var']:
                            r['var'][k] = None
                            if k not in re['none']:
                                re['none'].append(k)
                        re['var'] = dict(re['var'], **r['var'])

            if code != 0:
                re['result'][sp + _k] = {'code': code, 'sv': sv, 'pp': pp + _k, 'pv': pv}
        else:  # 键不存在
            if var_flag:
                re['var'][sv[1:-1]] = None
                re['none'].append(sv[1:-1])
            else:
                re['result'][sp + _k] = {'code': 3, 'sv': sv, 'pp': None, 'pv': None}

    re['code'] = len(re['result'])
    return re


"""
垃圾释放
"""


# @profile
def g_c():
    """
    垃圾释放 删除测试数据 也是当前用例运行结束的标志
    :return:
    """
    for json_file in ['load_c.json', 'call_c.json', 'page_variables.json']:
        try:
            os.remove(os.path.join(WORK_PLACE, json_file))
        except Exception as ex1:
            logger.info(str(ex1))
    gc.collect()


if __name__ == '__main__':
    """
    入口
    """
    logger.info('Test start...\n')

    load_c(None)

    teardown(None)

    logger.info('\n')
    logger.info('Test end...')

    # import psutil
    # print('A：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    g_c()
    # print('B：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
