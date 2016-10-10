__author__ = 'rwang'

#sudo easy_install mechanize

import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup


# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Open some site, let's pick a random one, the first that pops in mind:
#r = br.open('http://baidu.com')

'''
br.open('http://icode.renren.com/getcode.do?t=web_login&amp;rnd=Math.random()')
validation = br.response().read()
with open('icode.jpg','wb') as file:
    file.write(validation)
icode = raw_input("please check the file of icode.jpg and input the validation code: ")
'''
#r = br.open('http://renren.com')

#r = br.open('http://localhost/hd18y.html')
r = br.open('http://localhost/test2.html')

html = r.read()
'''
with open('/Library/WebServer/Documents/test.html','wb') as file:
    file.write(html)
'''
# Show the source
#print html
# or
#print br.response().read()

print "===========Begin==============="
r = br.response().read()
soup = BeautifulSoup(r)
inputs = soup.findAll('input')
for input in inputs:
    print input
    if input['type'] != 'submit':
        print input['name']
print "===========Done==============="




# Show the html title
#print br.geturl()
#print br.title()


# Show the response headers
#print r.info()
# or
#print br.response().info()

# Show the available forms


i = 1
for f in br.forms():
    #print i
    print "=====The %i form is======" %i
    i += 1
    print f





# Select the first (index zero) form
br.select_form(nr=0)
#print br.form.find_control("None")

print "========action========="
print br.form.action
print "========attrs========="
print br.form.attrs
print "========backwards_compat========="
print br.form.backwards_compat
print "========controls========="
#print br.form.controls
for item in br.form.controls:
    #print item
    #print item.attrs

    for input_check in inputs:
        if input_check['type'] != 'submit':
            if item.name == input_check['name']:
                print "item.name is: "+item.name
                #print "item.value is: "+  str(item.value)
                soup_div = BeautifulSoup(r)
                #inputs = soup.findAll('div')
                third_producer = soup_div.findAll('div', {'id':item.name + 'Tip'})

                print third_producer
                '''
                #print "input_check.value is: "+  str(input_check['value'])
                third_producer = soup.find('input', {'name': item.name})
                #print(third_producer['name'])
                #third_producer.append("producer")
                #soup.find('input', {'name': item.name})['value'] = 'rocky'
                div_number = soup.find('input', {'name': item.name})
                div_ecosystem = soup.new_tag("div")
                div_ecosystem['class'] = "ecosystem"
                div_ecosystem.append("soil")
                div_number.insert_after(div_ecosystem)
                print div_number
                #print(third_producer.prettify())
                '''

    #print item
    #if item.attrs['value'] == '':
    #    print item.attrs['name']

print "========enctype========="
print br.form.enctype
print "========method========="
print br.form.method
print "========name========="
print br.form.name

'''
with open('soup.html','wb') as file:
    file.write(r)
'''

'''
for name in br.form:
    print "here"
    keyword = name.split("(")[1].split(")")[0]
    if keyword[len(keyword)-1] == "=":
        keyword = keyword.split("=")[0]
        print keyword
'''
'''
# Let's login
br.form['email']='rocky_wang2003@hotmail.com'
br.form['password']='P@ssw0rd'
br.form['icode']="sss"
br.submit()
print br.response().read()

print "===========Begin==============="
r = br.response().read()
soup = BeautifulSoup(r)
movie = soup.findAll('form')
print movie
print "===========Done==============="
print br.geturl()
#print br.response().info()
print br.title()


# Show the available forms
i = 1
for f in br.forms():
    #print i
    print "=====The %i form is======" %i
    i += 1
    print f
'''
exit(0)
# Let's search
br.form['wd']='mechanize select form using id'
br.submit()
#print br.response().read()
br.response().read()


# Looking at some results in link format
for l in br.links(url_regex='python'):
    print l
