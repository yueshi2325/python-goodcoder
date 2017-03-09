# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
The module implements page downloading. done

Authors: songyue02(songyue02@baidu.com)
Date:    2016/06/04
"""

import re
import logging
import requests 

def make_url_good(raw_value):
    """
    Deal with the http header of url

    Args:
        raw_value: the orignal url
    
    Returns:
        The url that has http header    
    """
    if not raw_value.startswith('http'):
        raw_value = 'http://' + raw_value
    return raw_value


class PageUtil(object):
    """
    The class to send http requests, get the response, and deal with the data of response
    
    Attributes:
        url: the raw url to deal with 
        page_source: the code of web page
        web_timeout: the timeout for visiting the url
    """

    def __init__(self, url, timeout):
        self._url = url
        self._page_source = None
        self._web_timeout = timeout
        self._headers = ""

    def init_param(self):
        """
        1. ensure url start with "http". 
        2. init request headers.
        """
        self._url = make_url_good(self._url)
        self.custome_headers()

    def request(self, retry=2, proxies=None):
        """
        Get the code of the html file
        
        Args:
            retry: the time that this function try to visit the url, default is 2
            proxies: the proxy list this function use to visit the url, default is None
    
        Returns:
            a value of bool type.True means everything is ok.False means there is a Error happens
            
        Raises:
            AttributeError: An error occurred visit the unkown properties of object .
            KeyError: An error occurred access a key in the dict that does not exist.
            Exception: deal with the unkown error
        
        """
        try:
            response = requests.get(self._url, headers=self._headers,
                timeout=self._web_timeout, proxies=proxies)
            if self._is_response_avaliable(response):
                self._handle_encoding(response)
                self._page_source = response.text
                return True
            else:
                log = logging.getLogger('Spider.crawler')
                log.warning('[Page not avaliable]. Status code:%d URL: %s \n' % (
                    response.status_code, self._url))
        except (AttributeError, KeyError, Exception) as e:
            if retry > 0:  # try to visit again
                return self.request(retry - 1)
            else:
                log = logging.getLogger('Spider.crawler')
                log.error(str(e) + ' URL: %s \n' % self._url)
        return False

    def custome_headers(self, **kargs):
        """
        Get the custom headers of http request
        Can use the parameter, kargs, to overwrite the default value,
        or add new value, such as cookies
        
        Args:
            kargs: the header of http request
            
        Returns:
            None
        
        """    
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko)'         
        user_agent = user_agent + ' Chrome/22.0.1229.79 Safari/537.4'      
        self._headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': "'" + user_agent + "'",
            'Referer': "'" + self._url + "'",
        }
        self._headers.update(kargs)

    def get_data(self):
        """
        Get the url and the page source of this url
        
        Args:
            None
    
        Returns:
            None
        """
        return self._url, self._page_source

    def _is_response_avaliable(self, response):
        # Only get html page, when the response code is 200 
        if response.status_code == requests.codes.ok: 
            if 'html' in response.headers['Content-Type']:
                return True
        return False

    def _handle_encoding(self, response):
        # Get the real type of encode
        if response.encoding == 'ISO-8859-1':
            charset_re = re.compile("((^|;)\s*charset\s*=)([^\"']*)", re.M)
            charset=charset_re.search(response.text) 
            charset=charset and charset.group(3) or None 
            response.encoding = charset

