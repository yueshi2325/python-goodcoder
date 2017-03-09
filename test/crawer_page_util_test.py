# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide the unit-test for CrawerPageUtil.py.

Authors: songyue02(songyue02@baidu.com)
Date:    2016/04/26 23:50
"""

import unittest
import sys
import requests

sys.path.append('..')
import crawer_page_util 
import crawer_log 


class CrawerPageUtilTestCase(unittest.TestCase):
    """
    Class to test the CrawerPageUtil Class
    
    Attributes:
        url: the url to deal with 
        user_agent: the user_agent fielg in http header
        headers: a custom headers used to be part of the request
        timeout: the timeout of visiting url
        CrawerPageUtil: the instance of CrawerPageUtil class
    """
    def setUp(self): 
        self.url = "http://www.baidu.com/"
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko)'         
        user_agent = user_agent + ' Chrome/22.0.1229.79 Safari/537.4'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': user_agent,
            'Referer': self.url,
        }
        self.timeout = 1 
        self.crawer = crawer_page_util.PageUtil(self.url, self.timeout)  
        self.crawer.init_param()
       
    def tearDown(self):
        self.webpage = None
                
    def test_MakeUrlGood(self):
        """
        Test the MakeUrlGood() function of CrawerPageUtil

        Args:
            none
    
        Returns:
            None
        """
        self.assertEquals("http://www.baidu.com",
                          crawer_page_util.make_url_good("www.baidu.com")) 
        self.assertEquals("http://www.baidu.com", 
                          crawer_page_util.make_url_good("http://www.baidu.com")) 

    def test_Request(self):
        """
        Test the Request() function of WebPage

        Args:
            None
    
        Returns:
            None
        """
        # Normal situation
        self.assertEquals(True, self.crawer.request()) 
        # Exception
        fetchtest = crawer_page_util.PageUtil("http://pycm.baidu.com", self.timeout)
        self.assertEquals(False, fetchtest.request())
        fetchtest = None
    
    def test__is_response_avaliable(self):
        """
        Test the _is_response_avaliable() function of WebPage

        Args:
            None
    
        Returns:
            None
        """
        # Normal situation
        response = requests.get(self.url, headers = self.headers, timeout = self.timeout)
        self.assertEquals(True, self.crawer._is_response_avaliable(response)) 
        # Response code is 404
        response.status_code = 404
        self.assertEquals(False, self.crawer._is_response_avaliable(response))
        # Response code is 503
        response.status_code = 503
        self.assertEquals(False, self.crawer._is_response_avaliable(response))
          
    def test__handle_encoding(self):
        """
        Test the _handle_encoding() function of WebPage

        Args:
            None
    
        Returns:
            None
        """
        response = requests.get(self.url, headers = self.headers, timeout = self.timeout)
        # Encoding is not ISO-8859-1的情况
        encodeorg = response.encoding
        self.crawer._handle_encoding(response)
        self.assertEquals(encodeorg, response.encoding)
        # Encoding is ISO-8859-1的情况
        response.encoding = "ISO-8859-1"
        self.crawer._handle_encoding(response)
        ret = True
        if response.encoding == "ISO-8859-1":
            ret = False
        self.assertEquals(True, ret)


if __name__ == '__main__':
    crawer_log.init_log("./log/my_program", "Spider.crawler", 10)

    unittest.main()
    pass
