# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide the concrete realization of the Parselinks.

Authors: songyue02(songyue02@baidu.com)
Date:    2016/04/04
"""

import HTMLParser
import urllib
import sys

class Parselinks(HTMLParser.HTMLParser):
    """
    This module implements interfaces to parse html elements and get urls
    
    Attributes:
        urls: url results that we want
        href: flag, if a url element starts
        linkname: maybe html data is a urldesc. if flag==1,  keep it
        data: url desc. just for debug
              
    """

    def __init__(self):
        self.data = []
        self.urls = []
        self.href = 0
        self.linkname = ''
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs): 
        if tag == 'a': 
            for name, value in attrs: 
                if name == 'href': 
                    self.href = 1
                    self.urls.append(value)

    def handle_data(self, data): 
        if self.href: 
            self.linkname += data

    def handle_endtag(self, tag): 
        if tag == 'a':
            self.linkname = ''.join(self.linkname.split())
            self.linkname = self.linkname.strip()
        if  self.linkname:
            self.data.append(self.linkname)
            self.linkname = ''
            self.href = 0

    def get_result(self): 
        """
            Get url list from html 
            
            Args:
                None
            
            Returns:
                urls list
        """
        return self.urls

    def print_result(self): 
        """
            print debug data 
            
            Args:
                None
            
            Returns:
                strings to stdout
        """
        print "[value]:"
        for value in self.data:
            print value
            print "[urls]:"
        for url in self.urls:
            print url
      
if __name__ == "__main__": 
    """ Example for using this module."""
    page_source = u"""
        <!DOCTYPE html>
            <html>
                <head>
                    <meta charset=utf8>
                    <title>Crawl Me</title>
                </head>
                <body>
                    <ul>
                        <li><a href=page1.html>page 1</a></li>
                        <li><a href="page2.html">page 2</a></li>
                        <li><a href='page3.html'>page 3</a></li>
                        <li><a href='mirror/index.html'>mirror</a></li>
                        <li><a href='javascript:location.href="page4.html"'>
                            page 4</a></li>
                    </ul>
                </body>
            </html>
        """
    IParser = Parselinks()
    IParser.feed(page_source)
    IParser.print_result()
    IParser.close()