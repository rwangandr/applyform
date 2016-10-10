__author__ = 'rwang'
import urllib2, urllib, json


def request_ajax_data(url,data, referer=None, **headers):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116')
    if referer:
        req.add_header('Referer',referer)
    if headers:
        for k in headers.keys():
            req.add_header(k,headers[k])

    params = urllib.urlencode(data)
    response = urllib2.urlopen(req, params)
    jsonText = response.read()
    return json.loads(jsonText)


ajaxRequestBody = {"blogId":blogId,"postId":entryId,"blogApp":blogApp,"blogUserGuid":blogUserId}
ajaxResponse = request_ajax_data('http://outofmemory.cn/fakeAjax',ajaxRequestBody)