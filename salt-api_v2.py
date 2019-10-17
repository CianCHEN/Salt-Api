#!/usr/bin/evn python
#coding:utf-8

import json
from urlparse import urljoin
from functools import wraps
import requests
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib3
urllib3.disable_warnings()

class SaltApi:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.headers = {'Content-type': 'application/json'}
        self.resturi = ['/login','/jobs','/minions']
        self.token = self.getToken()

    def webReq(self, url, data, headers):
        try:
            req = requests.post(url, data = json.dumps(data), headers = headers, verify = False)
        except Exception, e:
            raise Exception(e)
        else:
            if req.status_code == 200:
                json_con = req.json()
                return json_con
            else:
                return False

    def getToken(self):
        """
        获取API请求token
        """
        fullurl = urljoin(self.url, self.resturi[0])
        data = {
            'username': self.username,
            'password': self.password,
            'eauth': 'pam'
        }
        token = self.webReq(fullurl, data, self.headers)
        if token is not False:
            return token['return'][0]['token']
        else:
            raise

    def myReq(self, prefix = '/', json_data = None, headers = None):
        """
        通用请求函数，统一返回 API json数据
        """
        post_url = urljoin(self.url, prefix)
        if headers is None:
            headers = {'X-Auth-Token': self.token, 'Accept': 'application/json'}
        else:
            headers = headers.update({'X-Auth-Token': self.token})
        results = requests.post(post_url, json = json_data, headers = headers, verify = False)
        return results.json()

    def Get_keys(self):
        """
        获取所有minions_pre minions_accept keys
        @return tunple
        """
        json_data = {'client': 'wheel', 'fun': 'key.list_all'}
        content = self.myReq(json_data = json_data)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre

    def Single_module(self, tgt, fun, isblock = False, isgroup = False, arg = None, **kwargs):
        """
        同步(block)/异步(noblock)  执行模块函数
        分组(isgroup)或者单机      执行
        @params
            tgt:       minion_id/group name      --> game-host-s1/qxh5-danfu
            fun:       function name             --> [test.ping|state.sls]
            isblock:   block or noblock          --> True or False
            isgroup:   group module or not       --> True or False
            arg:       args for fun if it's need --> arg='sls.compress.compress-html'
            **kwargs:  exart params              --> saltenv="game"
        @return list
        """ 
        json_data = {'tgt': tgt, 'fun': fun}
        if isblock:
            json_data['client'] = 'local'
        else:
            json_data['client'] = 'local_async'
        if isgroup:
            json_data.update({'expr_form': 'nodegroup'})
        if arg:
            json_data.update({'arg': arg})
        if kwargs:
            json_data.update({'kwarg': kwargs})
        print(json_data)
        content = self.myReq(json_data = json_data)
        return content['return']

    def Group_sls_async(self, tgt, arg, **kwargs):
        """
        分组异步执行sls

        @params
            tgt: group name          --> qxh5-danfu 
            arg: path to sls         --> sls.compress.compress-html
            **kwargs:  exart params  --> saltenv="game"

        @return list
        """
        json_data = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        if kwargs:
            json_data.update({'kwarg': kwargs})
        content = self.myReq(json_data = json_data)
        return content['return']

    def Jid_status(self, jid):
        """
        获取jid结果查询
        """
        json_data = {"client": "runner", "fun": "jobs.lookup_jid", "jid": jid}
        content = self.myReq(json_data = json_data)
        return content['return'][0]

    def Jobs_active(self):
        """
        获取当前活动的jobs
        @return list
        """
        json_data = {"client": "runner", "fun": "jobs.active"}
        content = self.myReq(json_data = json_data)
        return content['return']





if __name__ == '__main__':
    url = 'https://salt-api-url:salt-api-port'
    api = SaltApi(url, 'username', 'password')
    #print(api.Get_keys())
    #print(api.Jobs_active())
    #print(api.Jid_status("20191016104530606245"))
    #print(api.Single_module('qxh5-danfu', 'state.sls', isgroup = True, arg = 'dtest', saltenv = 'game'))
    #print(api.Single_module('h5-salt-manager', 'state.sls', arg = 'sls.compress.compress-html', saltenv = 'game'))
    #print(api.Single_module('h5-salt-manager', 'test.ping'))
    #print(api.Group_sls_async('qxh5-danfu', 'dtest', saltenv = 'game'))
    #print(api.Group_sls_async('qxh5-danfu', 'dtest'))
