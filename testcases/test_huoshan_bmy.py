import random,os
import logging
from string  import  Template
import allure
import yaml
import requests
import pytest
from config.api_path import *
from common.yaml_util import YamlUtil


logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s', level=logging.DEBUG)

class Test_huoshan_bmy_activity:
    Token = "Token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6eyJ1c2VyX2lkIjozMCwicm9sZV9pZCI6MjYsInVzZXJfbmFtZSI6IumZiOmbquWzsCIsImZlaXNodV9vcGVuX2lkIjoib3VfMWE4NTM5MzY5ZjUwMmIzNzViOThkZDdkYTU2YjJhZjYiLCJ1dWlkIjoiMzAiLCJyb2xlIjoic3VwZXIiLCJwZXJtaXNzaW9uIjpbXX0sInR5cGUiOiJhY2Nlc3MiLCJleHAiOjE2NDkyOTY3OTB9.tDSJOr1vjpO1Wpkm8ExFa6mY6cfiKcrfuydLDOQedZo"
    host = HUOSHAN_HOST

    r = str(random.randint(99,9999))


    # @allure.title("创建报名页活动")
    # @pytest.mark.parametrize("args",YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml","new_activity"))
    # def test_01new_activity(self, args):
    #     print(args['name'])
    #     method = args['request']['method']
    #     url = self.host + args['request']['url']
    #     data = args['request']['data']
    #     res = requests.request(method, url, json=data, headers={"Cookie":self.Token })
    #     assert res.json()['code'] == args['validate']['code']


    @allure.title("获取活动列表")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml","get_activity_list"))
    def test_02get_activity_list(self,args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url']
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        global activity_id
        activity_id = res.json()['msg']['data'][0]['uuid']
        assert res.json()['code']  == args['validate']['code']


    @allure.title("查询单个活动信息")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "query_a_activity_info"))
    def test_03query_a_activity_info(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + activity_id
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    @allure.title("创建模块")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "create_module"))
    def test_04create_module(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + activity_id
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    @allure.title("模块列表")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml","module_list"))
    def test_05module_list(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + activity_id
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']
        global module_id
        module_id = []
        r = res.json()["msg"]
        for i in range(len(r)):
            id = r[i]['id']
            module_id.append(id)
        # if module_id != None:
        #     pass
        # else:
        #     raise Exception("此活动未创建模块")


    @allure.title("更新模块")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "update_module"))
    def test_06update_module(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url']
        data = args['request']['data']
        data['id'] = module_id[0]
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    @allure.title("删除模块")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "delete_module"))
    def test_07delete_module(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + str(module_id[-1])
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    def yaml_template(self):
        with open(os.getcwd()+'/testdata/huoshan_bmy_activity.yaml', encoding='utf-8') as f:
            read_yml_str = f.read()
            tempTemplate1 = Template(read_yml_str)
            #替换yaml文件中带$的参数
            c = tempTemplate1.safe_substitute(
                {'module_id_6': module_id[0], 'module_id_7': module_id[1],'module_id_8': module_id[2],
                 'module_id_9': module_id[3],'activity_id': activity_id})
            return yaml.safe_load(c)


    @allure.title("创建模块内容")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "create_module_content"))
    def test_08create_module_content(self,args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url']
        temp_data= self.yaml_template()['create_module_content'][0]['request']['data']
        for m_c in temp_data:
            data =m_c
            res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
            assert res.json()['code'] == args['validate']['code']


    @allure.title("查询模块内容列表")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "query_module_content_list"))
    def test_09query_module_content_list(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + str(module_id[3])
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']
        global module_content_id
        module_content_id = res.json()['msg'][0]['id']


    @allure.title("查询模块内容")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "query_module_content"))
    def test_10query_module_content(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + str(module_content_id)
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    @allure.title("更新模块内容")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "update_module_content"))
    def test_11update_module_content(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + str(module_content_id)
        temp_data = self.yaml_template()['update_module_content'][0]['request']['data']
        data = temp_data
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    @allure.title("创建模块样式")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "create_module_style"))
    def test_12create_module_style(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url']
        temp_data = self.yaml_template()['create_module_style'][0]['request']['data']
        for m_s in temp_data:
            data = m_s
            res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
            assert res.json()['code'] == args['validate']['code']


    @allure.title("更新模块样式")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "update_module_style"))
    def test_13update_module_style(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url']
        temp_data = self.yaml_template()['update_module_style'][0]['request']['data']
        for u_m_s in temp_data:
            data = u_m_s
            res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
            assert res.json()['code'] == args['validate']['code']


    @allure.title("查询当个模块信息")
    @pytest.mark.parametrize("args",YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "query_a_module_info"))
    def test_14query_a_module_info(self,args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + str(module_id[0])
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie":self.Token})
        assert  res.json()['code'] == args['validate']['code']


    @allure.title("更新活动")
    @pytest.mark.parametrize("args",YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "update_activity"))
    def test_15update_activity(self,args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + activity_id
        temp_data = self.yaml_template()['update_activity'][0]['request']['data']
        data = temp_data
        data['title'] = data['title'] + self.r
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    @allure.title("活动详情")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "activity_details"))
    def test_16activity_details(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + activity_id
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    @allure.title("获取活动地址二维码")
    @pytest.mark.parametrize("args", YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "get_activity_qrcode"))
    def test_17get_activity_qrcode(self, args):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + activity_id
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']


    @allure.title("更改活动状态")
    @pytest.mark.parametrize("status",["/normal"])
    @pytest.mark.parametrize("args",YamlUtil().read_yaml_file("huoshan_bmy_activity.yaml", "change_activity_status"))
    def test_18change_activity_status(self,args,status):
        print(args['name'])
        method = args['request']['method']
        url = self.host + args['request']['url'] + activity_id + status
        data = args['request']['data']
        res = requests.request(method, url, json=data, headers={"Cookie": self.Token})
        assert res.json()['code'] == args['validate']['code']
