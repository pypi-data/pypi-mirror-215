# coding:utf-8

# @Auther:liyubin
# @Time: 2023/5/10 10:20

# from memory_profiler import profile  # 调试内存占用
"""
连接sql lite （.db、.cfg） 和 执行sql语句
"""


class RunDbFileCase:

    def __init__(self, logger):
        self.connect = None
        self.cursor = None
        self.db = ''
        self.arg = {'file': '', 'type': ''}
        self.logger = logger

    def connect_sql_lite(self):
        try:
            if self.arg['type'].lower() == 'sqlite':
                import sqlite3, os
                db_file = self.arg['file']
                # 因加载c++需切换工作空间到上一层，可能用例中只有db操作，自动拼接尝试上一层路径
                if not os.path.exists(db_file):
                    db_file = os.path.join('../', db_file)
                    if not os.path.exists(db_file):
                        assert os.path.exists(db_file), 'sqlite3 db 文件不存在：{}'.format(db_file)
                self.connect = sqlite3.connect(db_file)  # 加载sql_lite3.db文件
                self.cursor = self.connect.cursor()
                sql = ''
            else:
                raise '数据库连接失败请检查type类型是：sqlite，file等于.db、.cfg 且 用例步骤中标记 APART'

            self.cursor.execute(sql)
            self.cursor.fetchone()

        except:
            self.logger.exception('*** {} connect is failure ***'.format(self.arg['type']))
            raise

    def fetchone(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            self.connect.commit()
            return data
        except:
            self.logger.exception('*** Fetchone failure ***')
            raise

    def fetchall(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            self.connect.commit()
            return data
        except:
            self.logger.exception('*** Fetchall failure ***')
            raise

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except:
            self.logger.exception('*** Execute failure ***')
            raise

    def __del__(self):
        if self.connect:
            self.connect.close()

    def dedup(self, text):
        """
        去掉 text 中括号及其包含的字符
        :param text:
        :return:
        """
        _text = ''
        n = 0

        for s in text:
            if s not in ('(', ')'):
                if n <= 0:
                    _text += s
            elif s == '(':
                n += 1
            elif s == ')':
                n -= 1
        return _text

    def sql(self, step, g):
        """
        sql 关键字
        :param step:
        :return:
        """
        _sql = step.get('_sql')

        self.logger.info('SQL: {}'.format(repr(_sql)))
        # 获取连接参数
        value = step.get('_content_value')
        self.arg = self.data_format(value)

        # 执行sql
        row = ()
        if step['page'] not in g.db.keys():
            g.db[step['page']] = self.connect_sql_lite()
        if _sql.lower().startswith('select'):
            row = self.fetchone(_sql)  # 查单条 (1, 2)
            # rows = self.fetchall(_sql)  # 查多条 ((1, 2), (3, 4))
            self.logger.info('SQL result: {}'.format(repr(row)))
            if not row:
                raise Exception('*** Fetch None ***')
        else:
            self.execute(_sql)

        result = {}
        # 组装成{key: value}
        if _sql.lower().startswith('select'):
            text = _sql[6:].split('FROM')[0].split('from')[0].strip()
            keys = self.dedup(text).split(',')
            for i, k in enumerate(keys):
                keys[i] = k.split(' ')[-1]
            result.update(dict(zip(keys, row)))
            self.logger.info('keys result: {}'.format(repr(result)))

        data = step['data']
        if not data:
            data = step['expected']

        self.logger.info('Expected: {}'.format(data))
        if data:
            for key in data:
                sv, pv = data[key], result[key]
                if 'str' in sv or 'int' in sv or 'float' in sv or 'bool' in sv or 'round' in sv:
                    sv = eval(sv)
                self.logger.info('key: {}, expect: {}, real: {}'.format(repr(key), repr(sv), repr(pv)))

                self.compare(sv, pv)

        output = step['output']
        if output:
            self.logger.info('output: {}'.format(repr(output)))
            for key in output:
                var_k = output[key].replace('<', '').replace('>', '')
                g.var[var_k] = result[key]

    """
    辅助函数 格式转换
    """

    def data_format(self, data):
        data = self.escape(data)
        if ',,' in data:
            data_list = data.split(',,')
        else:
            # data = data.replace('，', ',')  # 中文逗号不再视为分隔符
            data_list = []
            if data:
                data_list = data.split(',')
        data_dict = {}
        for data in data_list:
            # 只需要分割第一个'='号
            d = data.split('=', 1)
            d[-1] = self.recover(d[-1])  # 只有值需要转义恢复，<页面变量属性> or <变量名> 不应该出现转义字符
            if len(d) == 1:
                # 如果没有=号分割，说明只有内容，默认赋值给 text
                if not data_dict.get('text'):
                    data_dict['text'] = d[0]
            elif len(d) == 2:
                d[0] = d[0].strip()  # 清除 <页面变量属性> 2边的空格，如果有的话
                data_dict[d[0]] = d[1]
            else:
                raise Exception('Error: Testcase\'s Data is error, more "=" or less ","')
        return data_dict

    def escape(self, data):
        # 先把转义字符替换掉
        # 特殊符号的转换别名
        comma_lower = '#$%^&'
        return data.replace('\\,', comma_lower)

    def recover(self, data):
        # 再把转义字符恢复
        # 特殊符号的转换别名
        comma_lower = '#$%^&'
        return data.replace(comma_lower, ',')

    """
        辅助函数 结果校验
    """

    def compare(self, data, real):
        """sql查询结果校验"""
        if isinstance(data, str):

            if data.startswith('#'):
                assert data[1:] != str(real), 'CHECK ERROR: {} != {}'.format(data, real)
                return
            elif data.startswith(':'):
                exec('v=real;' + data[1:])
                return

            assert isinstance(real, str)

            if data.startswith('*'):
                assert data[1:] in real, 'CHECK ERROR: {} !in {}'.format(data[1:], real)
                return
            elif data.startswith('^'):
                assert real.startswith(data[1:]), 'CHECK ERROR: {} !startswith {}'.format(data[1:], real)
                return
            elif data.startswith('$'):
                assert real.endswith(data[1:]), 'CHECK ERROR: {} !endswith {}'.format(data[1:], real)
                return

            elif data.startswith('\\'):
                data = data[1:]

            assert data == real, '{} != {}'.format(data, real)

        elif isinstance(data, int):
            assert isinstance(real, int), 'CHECK ERROR: except type: {}, real type: {}'.format(data, real)
            assert data == real, 'CHECK ERROR: {} != {}'.format(data, real)
        elif isinstance(data, float):
            assert isinstance(real, float), 'CHECK ERROR: except type: {}, real type: {}'.format(data, real)
            data, p1 = self.str2float(data)
            real, p2 = self.str2float(real)
            p = min(p1, p2)
            assert round(data, p) == round(real, p), 'CHECK ERROR: {} != {}'.format(data, real)
        else:
            assert data == real, 'CHECK ERROR: {} != {}'.format(data, real)

    def str2float(self, s, n=None):
        s = str(s).replace(',', '')
        number = s.split('.', 1)
        if n:
            f = float(s)
            return round(f, n), n

        dot = '0'
        if len(number) == 2:
            dot = number[-1]
            dot = self.zero(dot)
        f = float(number[0] + '.' + dot)

        return round(f, len(dot)), len(dot)

    def zero(self, s):
        if s and s[-1] == '0':
            s = s[:-1]
            s = self.zero(s)
        return s

# 在 run_ctypes_k_obj_per.py 继承，必传logger，调用时传入 g
