'''
Created on 2013-5-10

@author: chenko
'''


# import urllib.request
# import urllib.parse
# import urllib.error
import cookielib
import urllib2
from contextlib import closing


# Set session ID: t from renren.com cookie via Chrome
COOKIE_T = r"7a1816c8b2b641b9db415d0490acf46a3"

# # Directory to store the fetched page
# RSP_HTML_DIR = r"./page.html"


class Request():
    '''HTTP request to a specific RenRen page

    Logged in is required to skip the verification code
    '''
    my_cookie = "".join(["t=", COOKIE_T])

    def __init__(self, url):
        self.url = url
#         self.rsp_html_dir = RSP_HTML_DIR

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

#         finally:
#             page.close()
#         except urllib2.URLError as e:
#             if hasattr(e, "reason"):  # URL error
#                 print("URL Error occurred.")
#                 print('Reason: ', e.reason)
#             elif hasattr(e, "code"):  # HTTP error
#                 print("HTTP Error occurred.")
#                 print("Error code: ", e.code)
