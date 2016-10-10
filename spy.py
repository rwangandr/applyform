__author__ = 'rwang'
# -*- coding:utf-8 -*-

import ssl
import monkey_ssl
ssl.wrap_socket = monkey_ssl.getssl()
import mechanize
import cookielib
import configuration
import os
import webbrowser
import BeautifulSoup
MODE_CONFIG = 0
MODE_INPUT = 1
STR_INPUT_SELECT_RADIO = "Please input the index (0,1,2 for instance) of %s:\t"
STR_INPUT_CHECKBOX = "Check on %s?:(Y/N)\t"
STR_INPUT_TEXT_PWD = "Please input the value of %s:\t"

class spy:
    def __init__(self):
        self.__mode = MODE_INPUT
        self.__config = configuration.configuration()

        self.__pageinfo = ""
        # Browser
        self.__br = mechanize.Browser()
        self.__br_i = mechanize.Browser()

        #self.__br = mechanize.urlopen("https://taobao.com")

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        self.__br.set_cookiejar(cj)
        self.__br_i.set_cookiejar(cj)

        # Browser options
        self.__br.set_handle_equiv(True)
        self.__br.set_handle_gzip(True)
        self.__br.set_handle_redirect(True)
        self.__br.set_handle_referer(True)
        self.__br.set_handle_robots(False)

        # Browser options
        self.__br_i.set_handle_equiv(True)
        self.__br_i.set_handle_gzip(True)
        self.__br_i.set_handle_redirect(True)
        self.__br_i.set_handle_referer(True)
        self.__br_i.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        self.__br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Follows refresh 0 but not hangs on refresh > 0
        self.__br_i.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #br.set_debug_http(True)
        #br.set_debug_redirects(True)
        #br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        self.__br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.__br_i.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def __getiCode(self):
        icode_url = self.__config.getValue("iCode", "url")

        if icode_url == "":
            return False
        self.__br_i.open(icode_url)
        validation = self.__br_i.response().read()
        with open('resource/icode.jpg','wb') as file:
            file.write(validation)
        #os.system("open -a safari 'icode.jpg'")
        webbrowser.open("file://" + os.getcwd() + "/" + 'resource/icode.jpg', autoraise=0)
        return True

    def __checkiCode(self, control):
        if control.name.lower().find("verif") != -1 or control.name.lower().find("code") != -1:
            user_input = raw_input("get iCode?(Y/N)\t")
            if user_input.lower() == "y":
                while True:
                    self.__getiCode()
                    user_input = raw_input("Is it clear?(Y/N):\t")
                    if user_input.lower() == "y":
                        break


    def __addressString(self,strKeyWord):
        if strKeyWord is None:
            return ""
        strRange = ""
        if self.__pageinfo == "":
            return ""

        index = self.__pageinfo.find(strKeyWord)
        if index != -1:
            strRange = self.__pageinfo[index-100:index+len(strKeyWord)+100]
        return strRange

    def __submit(self):
        submit_page = self.__br.submit()
        print self.__br.response()
        url = self.__br.response().geturl()
        print url
        webbrowser.open(url, autoraise=0)
        #self.handlePage(url)
        #print self.__br.response().read()
        self.__saveAllImg(submit_page)
        self.__handleForm(url)

    def __getFormControlValue(self, control):
        value = ""
        strTip = ""
        if MODE_INPUT == self.__mode:
            if control.type == "select" or control.type == "radio":
                strTip = STR_INPUT_SELECT_RADIO
            elif control.type == "checkbox":
                strTip =STR_INPUT_CHECKBOX
            elif control.type == "text" or control.type == "password" or control.type == "textarea" or control.type == "hidden":
                self.__checkiCode(control)
                strTip = STR_INPUT_TEXT_PWD
            value = raw_input(strTip %control.name)
        elif MODE_CONFIG == self.__mode:
            value = self.__config.getValue("FormData",control.name)
        return value

    def __handleControlSelectAndRadio(self, form, control):
        print "options is:"
        options = []
        for item in form.find_control(control.name).items:
            print item.name
            options.append(item.name)

        user_input = self.__getFormControlValue(control)

        if user_input == "":
            return

        j = 0
        for j in range(0,len(options)):
            if j == int(user_input):
                form.find_control(control.name).get(options[j]).selected = True
            else:
                form.find_control(control.name).get(options[j]).selected = False

    def __handleControlCheckbox(self, form, control):
        user_input = self.__getFormControlValue(control)
        if user_input == "":
            return
        elif user_input.lower() == "y":
            form.find_control(control.name).items[0].selected=True
        elif user_input.lower() == "n":
            form.find_control(control.name).items[0].selected=False

    def __handleControlText(self, form, control):
        user_input = self.__getFormControlValue(control)
        if user_input == "":
            return
        print self.__br
        print control.name
        # name=None, type=None, kind=None, id=None,predicate=None, nr=None,label=None
        #form.find_control(control.name, control.type, None, control.id, None, None, None)
        form.find_control(control.name).readonly = False
        self.__br[control.name] = str(user_input)
        form.find_control(control.name).readonly = True

    def __handleControlHidden(self, form, control):
        user_input = self.__getFormControlValue(control)
        if user_input == "":
            return
        print self.__br
        print control.name
        # name=None, type=None, kind=None, id=None,predicate=None, nr=None,label=None
        #form.find_control(control.name, control.type, None, control.id, None, None, None)
        form.find_control(control.name).readonly = False
        self.__br[control.name] = str(user_input)
        form.find_control(control.name).readonly = True

    def __fillForm(self,form):
        bRet = True
        while True:
            i = 0
            for control in self.__br.form.controls:
                print "==============The %i input================="%i
                i += 1
                print control, control.type, control.name

                if control.type == "submit" or control.type == "buttonbutton":
                    continue

                print "---------Tip---------\n", \
                    self.__addressString(control.name).replace("\n","").replace(" ","").replace("\t",""),\
                    "\n------End of Tip-----"

                if control.type == "hidden":
                    self.__handleControlHidden(form, control)
                elif control.type == "select" or control.type == "radio":
                    self.__handleControlSelectAndRadio(form, control)
                elif control.type == "checkbox":
                    self.__handleControlCheckbox(form, control)
                elif control.type == "text" or control.type == "password" or control.type == "textarea":
                    self.__handleControlText(form, control)

            print "The filled form is:\n", form, "\nDone"

            user_input = raw_input("Do you confirm the filled and Submit it?(Y/N)\t")
            if user_input.lower() == "y":
                break
            else:
                user_input = raw_input("To re-fill?(Y/N)\t")
                if user_input.lower() != "y":
                    print "Quit this form"
                    bRet = False
                    break

        return bRet

    def apply(self, mode, filename):
        self.__mode = mode
        self.__config.fileConfig("config/" + filename)
        url = self.__config.getValue("Link", "url")
        if url == "":
            print "Please give url"
            return ""

        print "To open the page %s" %url
        try:
            page = self.__br.open(url)
        except:
            return -1
        print "this is the page %s" %page
        webbrowser.open(url, autoraise=0)
        #print page.info()
        self.__saveAllImg(page)
        self.__handleForm(url)
        return 0

    def __saveAllImg(self, page):

        soup = BeautifulSoup.BeautifulSoup(page.get_data())
        imgs = soup.findAll('img')
        print "==========Image Link, might include the validate code link=========="
        for img in imgs:
            try:
                print img['src']
                image_response = self.__br.open_novisit(img['src'].strip("."))
            except:
                continue
            image = image_response.read()
            arrayImgLink = img['src'].split("/")
            image_filename = arrayImgLink[len(arrayImgLink)-1]
            if image_filename != "":
                with open("resource/" + image_filename,'wb') as file:
                    file.write(image)
        print "==================Image Link search done============================="

    def __handleForm(self,url):
        if url == "":
            print "Please give url"
            return ""

        urls = url.split("/")
        localName = urls[len(urls)-1] + ".html"

        self.__pageinfo = self.__br.response().read()

        with open("resource/" + localName,'wb') as file:
            file.write(self.__pageinfo)
        #os.system ("open -a safari %s" %localName)
        #webbrowser.open("file:///Users/rwang/Documents/sihuo/browser_code/mechanize/toReg.html")
        #webbrowser.open("file://" + os.getcwd() + "/" + "resource/" + localName, autoraise=0)
        try:
            print self.__br.title()
        except:
            print "It's not a valid html file"
            return
        try:
            fs = self.__br.forms()
        except:
            print "read forms error"
            return
        i = -1
        for f in self.__br.forms():
            i += 1
            print "=====The %i form is======" % (i+1)
            print f
            user_input = raw_input("Is it the form you want?(Y/N):\t")
            if user_input.lower() != "y":
                continue

            self.__br.select_form(nr=i)
            if self.__fillForm(f):
                self.__submit()
        print "Complete all forms"



