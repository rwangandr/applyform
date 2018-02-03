# -*- coding:utf-8 -*-

import urllib
import urllib2
'''
#request = urllib2.Request('https://172.16.51.146/nqsky-meap-tenant-manager/QA/index')
request = urllib2.Request('https://172.16.51.146/nqsky-meap-tenant-manager/QA/login?companyType=0&userName=admin&password=123456&_csrf=&_csrf_header=')
opener = urllib2.build_opener() #设置窃取的JSESSIONID
#request.add_header('Cookie','JSESSIONID=0DFC22ABF6498B732BFD574AB2469948')
hellodata=opener.open(request).read()
print hellodata
'''
import urllib2
request = urllib2.Request('https://172.16.51.146/nqsky-meap-tenant-manager/QA/main/portal/portalInfo/list')
opener = urllib2.build_opener()
#设置窃取的JSESSIONID
#5ECEE0A0DA8B132C53C5CC736FB795C5
request.add_header('Cookie','JSESSIONID=031AE19546C6F92134F5A9535E79F64C')
hellodata=opener.open(request).read()
print hellodata

