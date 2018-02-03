# -*- coding:utf-8 -*-

import urllib2
import json
import ssl
import os,sys
import time

desfolder = os.path.dirname(sys.argv[0])
if desfolder != '':
    os.chdir(desfolder)
print ("workspace is %s" % os.getcwd())

import station
import configuration

#import monkey_ssl
#ssl.wrap_socket = monkey_ssl.getssl()
if sys.platform.find('darwin') != -1:
    ssl._create_default_https_context = ssl._create_unverified_context
elif sys.platform.find('linux') != -1:
    os.system("timedatectl set-timezone Asia/Shanghai > /dev/null")
#url12306 = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=${train_date}$&leftTicketDTO.from_station=${from_station}$&leftTicketDTO.to_station=${to_station}$&purpose_codes=ADULT"
url12306 = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=${train_date}$&leftTicketDTO.from_station=${from_station}$&leftTicketDTO.to_station=${to_station}$&purpose_codes=ADULT'
#xxxxxxxx = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2017-02-04&leftTicketDTO.from_station=BTC&leftTicketDTO.to_station=TJP&purpose_codes=ADULT"
seat_dict = {"硬卧":"yw_num","软卧":"rw_num","硬座":"yz_num","一等座":"zy_num","二等座":"ze_num","特等座":"tz_num"}
#seat_dict = {"yw_num":u"硬卧","rw_num":u"软卧","yz_num":u"硬座","zy_num":u"一等座","ze_num":u"二等座","tz_num":u"特等座"}
#html = urllib2.urlopen(r'https://kyfw.12306.cn/otn/leftTicket/init')

notified=""

def search(url,trains,seats,notifys, msg_title, webchatuser="@all", notifyonce=True):
    #url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2017-02-04&leftTicketDTO.from_station=BTC&leftTicketDTO.to_station=TJP&purpose_codes=ADULT"
    nfind = False
    html = ""
    try:
        html = urllib2.urlopen(url,timeout=5)
    except Exception, e:
        print e
    #print html.read()
    #return
    #exit(1)
    if html == "":
        return nfind
    try:
        hjson = json.loads(html.read())
        dumy = len(hjson['data'])
    except Exception,e:
        print e
        return nfind
    #print hjson['data']
    #print "hjson is:",hjson
    for i in range(0, len(hjson['data'])):
        mon_train = hjson['data'][i]['queryLeftNewDTO']['station_train_code']
        if trains == "":
            print "======",mon_train,"======"
        else:
            if trains.find(mon_train) != -1:
                print "======",mon_train,"======"
            else:
                continue
        for seat_name in seats:
            seat = seat_dict[seat_name]
            seat_ret = hjson['data'][i]['queryLeftNewDTO'][seat]
            if seat_ret == u"无" or seat_ret == "--" or seat_ret == "*": #无票或票类不符或尚未预售
                print seat_name, seat_ret.encode('utf-8')
                continue
            else:
                nfind = True
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
        webchat_user = c.getValue(item, "user")
        if webchat_user == "":
            webchat_user = "@all"
        #from_station = c.getValue(item, "from_station")
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        title = station_from_hanzi + "-->" + station_to_hanzi + " on " + train_date + " at " + otherStyleTime
        print title
        yoururl = url12306.replace("${train_date}$",train_date).replace("${from_station}$",from_station).replace("${to_station}$",to_station)
        #print yoururl
        ret = search(yoururl,train_code, seat_type,notifys,title,webchat_user,notifyonce)
        #break
    #break
    time.sleep(1)
    '''
        if ret:
            c.setValue(item,"Find", "True")
            if c.getValue(item, "breakonget") == "True":
                continue
        #break
    '''