# -*- coding:utf-8 -*-

import urllib2
import requests
import json
import ssl
import os,sys
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

desfolder = os.path.dirname(sys.argv[0])
if desfolder != '':
    os.chdir(desfolder)
print ("workspace is %s" % os.getcwd())

TRAIN_NUMBER = 4-1
GAOJIRUANWO = 22-1
RUANWO = 24-1
YINGWO = 29-1
YINGZUO = 30 - 1
WUZUO = 27 - 1
ERDENGZUO = 31-1
YIDENGZUO = 32-1
SHANGWUZUO = 33-1
TEDENGZUO = 26 - 1
seat_dict = {"高级软卧":GAOJIRUANWO,"无座":WUZUO,"硬卧":YINGWO,"软卧":RUANWO,"硬座":YINGZUO,"一等座":YIDENGZUO,"二等座":ERDENGZUO,"特等座":TEDENGZUO,"商务座":SHANGWUZUO}
import station
import configuration

#import monkey_ssl
#ssl.wrap_socket = monkey_ssl.getssl()
if sys.platform.find('darwin') != -1:
    ssl._create_default_https_context = ssl._create_unverified_context
elif sys.platform.find('linux') != -1:
    os.system("timedatectl set-timezone Asia/Shanghai > /dev/null")
url12306 = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=${train_date}$&leftTicketDTO.from_station=${from_station}$&leftTicketDTO.to_station=${to_station}$&purpose_codes=ADULT"
#url12306 = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=${train_date}$&leftTicketDTO.from_station=${from_station}$&leftTicketDTO.to_station=${to_station}$&purpose_codes=ADULT'
#url12306 = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=${train_date}$&leftTicketDTO.from_station=${from_station}$&leftTicketDTO.to_station=${to_station}$&purpose_codes=ADULT'
#xxxxxxxx = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2017-02-04&leftTicketDTO.from_station=BTC&leftTicketDTO.to_station=TJP&purpose_codes=ADULT"

#seat_dict = {"yw_num":u"硬卧","rw_num":u"软卧","yz_num":u"硬座","zy_num":u"一等座","ze_num":u"二等座","tz_num":u"特等座"}
#html = urllib2.urlopen(r'https://kyfw.12306.cn/otn/leftTicket/init')

notified=""

def ticket(url,trains,except_trains,seats,notifys, msg_title, webchatuser="@all", notifyonce=True):
    #url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2017-02-04&leftTicketDTO.from_station=BTC&leftTicketDTO.to_station=TJP&purpose_codes=ADULT"
    #notifyonce = False
    nfind = False
    html = ""
    try:
        #print url
        #html = urllib2.urlopen(url,timeout=10)
        html = requests.get(url, verify=False)
        #print r.content
    except Exception, e:
        print "requests.get(url, verify=False):" + str(e.message)
        return nfind
    #print html.read()
    #return
    #exit(1)
    #data = html.read()
    data = html.content
    #print data
    if data == "" or data.find('data') == -1: #or data.find('validateMessagesShowId') == -1
        print 'data is invalid'
        #print data
        return nfind
    try:
        ojson = json.loads(data)
        dumy = len(ojson['data'])
    except Exception,e:
        print "json.loads(data):"+e.message
        return nfind
    #print "ojson is:", ojson
    hjson = ojson['data']['result']
    #print "hjson is:",hjson

    for i in range(0, len(hjson)):
        l_info = hjson[i].split("|")
        '''
        if l_info[TRAIN_NUMBER] == 'K1302':
            #print l_info
            print "TRAIN_NUMBER",l_info[TRAIN_NUMBER]
            print "GAOJIRUANWO",l_info[GAOJIRUANWO]
            print "RUANWO",l_info[RUANWO]
            print "YINGWO",l_info[YINGWO]
            print "YINGZUO", l_info[YINGZUO]
            print "WUZUO", l_info[WUZUO]
            print "ERDENGZUO",l_info[ERDENGZUO]
            print "YIDENGZUO",l_info[YIDENGZUO]
            print "SHANGWUZUO",l_info[SHANGWUZUO]
            print "TEDENGZUO", l_info[TEDENGZUO]
            print "==============================="
        continue
        '''
        mon_train = l_info[TRAIN_NUMBER]
        if except_trains != "" and except_trains.find(mon_train) != -1:
            continue
        if trains == "":
            pass
            #print "======",mon_train,"======"
        else:
            if trains.find(mon_train) != -1:
                pass
                #print "======",mon_train,"======"
            else:
                continue
        for seat_name in seats:
            seat = seat_dict[seat_name]
            seat_ret = l_info[seat]
            #print "=="+seat_ret+"=="
            if seat_ret == u"无" or seat_ret == "--" or seat_ret == "*" or seat_ret == "": #无票或票类不符或尚未预售
                #print seat_name, seat_ret.encode('utf-8')
                continue
            else:
                nfind = True
                print "======", mon_train, "======"
                print seat_name, "", (seat_ret+"!!!!!!").encode('utf-8')

            global notified
            #msg_record = mon_train+","+seat_dict[seat]+","
            msg_record = mon_train+","+seat_name.decode('utf-8')+","+seat_ret
            #msg_record = mon_train + seat_name.decode('utf-8')
            if notified != "" and notified.find(msg_record) != -1:
                dup = True
            else:
                dup = False
                notified += msg_record

            if notifyonce and dup:
                continue
            else:
                msg = mon_train+","+seat_name.decode('utf-8')+","+seat_ret + "\n" + msg_title.decode('utf-8')
                for notify in notifys:
                    if notify == "sound":
                        os.popen("nohup python playsound.py >>sound.log &")
                    elif notify == "popup":
                        os.popen("nohup python popup.py '%s' >>popup.log &" %msg.encode('utf-8'))
                    elif notify == "webchat":
                        os.popen("nohup python webchat.py '%s' '%s' >>webchat.log &"
                                 % (webchatuser, msg.encode('utf-8')))
                    else:
                        print "Notification type configuration error!!!"
                #playwav.soundStart()
                #popup.showMessage(mon_train+","+seat_dict[seat]+","+seat_ret)


    #print hjson['summary']
    #os.system("clear")
    return nfind

while True:
    c = configuration.configuration()
    c.fileConfig("config/config.ini")
    items = c.getValue("Monitor", "items").split(",")
    notifys = c.getValue("Monitor","notifys").split(",")
    notifyonce = (c.getValue("Monitor", "notifyonce") == "True")
    for item in items:
        train_date = c.getValue(item, "train_date")
        station_from_hanzi = c.getValue(item, "from_station")
        from_station = station.get_station_code_by_name(station_from_hanzi)[0]
        station_to_hanzi = c.getValue(item, "to_station")
        #print station_to_hanzi
        to_station = station.get_station_code_by_name(station_to_hanzi)[0]
        seat_type = c.getValue(item, "seat_type").split(",")
        train_code = c.getValue(item, "train_code")
        except_train = c.getValue(item, "except_train")
        webchat_user = c.getValue(item, "user")
        if webchat_user == "":
            webchat_user = "@all"
        #from_station = c.getValue(item, "from_station")
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        title = station_from_hanzi + "-->" + station_to_hanzi + " on " + train_date + " at " + otherStyleTime
        print "***************************\n",title,"\n***************************"
        yoururl = url12306.replace("${train_date}$",train_date).replace("${from_station}$",from_station).replace("${to_station}$",to_station)
        #print yoururl
        ret = ticket(yoururl,train_code, except_train, seat_type,notifys,title,webchat_user,notifyonce)
        #break
        time.sleep(10)
    #break
    time.sleep(10)
    '''
        if ret:
            c.setValue(item,"Find", "True")
            if c.getValue(item, "breakonget") == "True":
                continue
        #break
    '''


#nohup python ticket.py >nohup.log 2>&1 0</dev/null &