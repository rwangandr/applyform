# -*- coding: utf-8 -*-
import requests
import json
import sys

def send_msg(user,msg):
    my_token = __get_token()
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % my_token
    header = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'utf-8'}
    #userinfo = __getuserinfo()
    values = {
        "touser": user,
        "toparty": "",
        "totag": "",
        "msgtype": "text",
        "agentid": 1,
        "text":
            {"content": msg},
        "safe": 0}

    jdata = json.dumps(values, ensure_ascii=False)
    print jdata
    req = requests.post(url, data=jdata, headers=header)
    print req.content

def __get_token():
    # url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    # values = {'corpid': 'wxdc22dea7597102d4',
    #          'corpsecret': '8QBico5U8Fl-6BpPku8bnS8eUFbEKTC8wRT-1rhWy-9aDcYXk3wlmee8qE5m14s_',
    #          }
    # req = requests.post(url, params=values)
    myid = "wxdc22dea7597102d4"
    mysecrect = "8QBico5U8Fl-6BpPku8bnS8eUFbEKTC8wRT-1rhWy-9aDcYXk3wlmee8qE5m14s_"
    req = requests.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (myid, mysecrect))
    print req.content
    data = json.loads(req.content)
    return data["access_token"]


def __getuserinfo():
    my_token = __get_token()
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=%s" % my_token
    header = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'utf-8'}
    req = requests.get(url)
    print req.content


def main(argv):
    send_msg(argv[1],argv[2])

if __name__ == '__main__':
    main(sys.argv)
    #__getuserinfo()

    # if __name__ == '__main__':
    #    send_msg(u"硬卧，有")
