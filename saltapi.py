#!/usr/bin/python
#coding:utf-8
###################################################################
# File Name: saltapi.py
# Author: Cian
# E-mail: chenzhangan_cian@163.com
# Created Time: Mon 25 Dec 2017 01:21:08 PM CST
#=============================================================
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


restful = ["/login","/jobs"]
url = "https://192.168.36.152:7878"
header = {"Accept" : "application/json"}

class Salt_Api:
    def __init__(self, url, username, password, header):
        self.url = url
        self.username = username
        self.password = password
        self.header = header

    def Get_Token(self):
        data = {
            "username" : self.username,
            "password" : self.password,
            "eauth" : "pam"
        }
        loginurl = self.url + restful[0]
        req = requests.post(loginurl, data=data, headers=self.header, verify=False)
        print req.json()
        return req.json()["return"][0]["token"]
 
    def Check_Jids(self):
        self.header['X-Auth-Token'] = self.Get_Token()
        header = self.header
        print header
        jid = sys.argv[1]
        #jid_url = self.url + "/" + restful[1] + "/" + jid
        jid_url = self.url + "{0}/{1}" .format(restful[1],jid)
        print jid_url
        req = requests.get(jid_url, headers=header, verify=False)
        print req.json()
         

def main():
    ss=Salt_Api(url,"saltapi","saltapi",header)
    #ss.Get_Token()
    ss.Check_Jids()


if __name__ == '__main__':
    main()
