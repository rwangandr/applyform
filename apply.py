__author__ = 'rwang'
# -*- coding:utf-8 -*-

import spy
import sys
import getopt
import webbrowser
import os
MODE_CONFIG = 0
MODE_INPUT = 1


def Usage():
    print 'apply.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-o, --output: input an output verb'
    print '--mode: operation mode, [input|config], optional, default value is input'
    print '--file: client information filename which should be in the folder of config, required, szty1.ini for instance'

def Version():
    print 'apply.py 0.1'

def OutPut(args):
    print 'Hello, %s'%args

def main(argv):
    handle_mode = MODE_INPUT
    filename = ""
    mode = ""

    try:
        opts, args = getopt.getopt(argv[1:], 'hvo:', ['output=', 'mode=', 'file='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif o in ('-o', '--output'):
            OutPut(a)
            sys.exit(0)
        elif o in ('--mode'):
            mode=a
            #print mode
        elif o in ('--file'):
            filename=a
            #print filename
        else:
            print 'unhandled option'
            sys.exit(3)

    if mode == "config":
        handle_mode = MODE_CONFIG
        if file == "":
            Usage()
            sys.exit(2)

    s = spy.spy()
    while True:
        nRet = s.apply(handle_mode, filename)
        if nRet == 0:
            break


    '''
    #s.handlePage("http://localhost/test2.html")
    #s.handlePage("http://localhost/hd18y.html")
    #s.handlePage("http://221.204.177.81:8080/school-admin-web/reg/toReg")
    #s.handlePage(url = "http://221.204.177.81:8080/school-admin-web/school/tsStudentInfo/saveInfo")
    #s.handlePage(url = "http://221.204.177.81:8080/school-admin-web/reg/toEnrollment")

    #s.handlePage("http://renren.com")
    #s.handlePage(url = "https://baidu.com")
    #s.handlePage(url = "https://taobao.com")
    '''
if __name__ == '__main__':
    main(sys.argv)