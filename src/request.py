'''
Created on 2013-5-10

@author: chenko
'''


import cookielib
import urllib2
from contextlib import closing


# Set session ID: t from renren.com cookie via Chrome
COOKIE_T = r"39edfcf8f8d6afdc6bb1cc7cb5565fc93"


class Request():
    '''HTTP request to a specific RenRen page

    Logged in is required to skip the verification code
    '''
    my_cookie = "".join(["t=", COOKIE_T])

    def __init__(self, url):
        '''Initialize the self.url
        '''
        self.url = url

    def get_response(self):
        '''Get response content from the HTTP request
        '''
        opener = urllib2.build_opener(
                 urllib2.HTTPCookieProcessor(
                 cookielib.CookieJar()))
        urllib2.install_opener(opener)
        req = urllib2.Request(self.url)
        req.add_header('Cookie', self.my_cookie)

        with closing(urllib2.urlopen(req)) as page:
            response = page.read()
            return response
