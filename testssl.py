__author__ = 'rwang'

import ssl
old_wrap_socket = ssl.wrap_socket
def wrap_socket(sock, keyfile=None, certfile=None,
                server_side=False, cert_reqs=ssl.CERT_NONE,
                ssl_version=ssl.PROTOCOL_SSLv3, ca_certs=None,
                do_handshake_on_connect=True,
                suppress_ragged_eofs=True, ciphers=None):
    return old_wrap_socket(sock, keyfile, certfile,
                           server_side, cert_reqs, ssl_version,
                           ca_certs, do_handshake_on_connect,
                           suppress_ragged_eofs, ciphers)
ssl.wrap_socket = wrap_socket

#ssl.wrap_socket = monkey_wrap_socket

import mechanize
import cookielib

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
r = br.open('https://taobao.com')


