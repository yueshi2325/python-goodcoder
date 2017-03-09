# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide the unit-test for crawer_html_parser.py.

Authors: songyue02(songyue02@baidu.com)
Date:    2016/04/27 20:57
"""

import unittest
import sys
import requests

sys.path.append('..')
import crawer_html_parser


class CrawerHTMLParserTestCase(unittest.TestCase):
    """
    Class to test the crawer_html_parser Class
    
    Attributes:
        pagesource: html text for testing
        crawer_html_parser: the instance of crawer_html_parser class
    """
    def setUp(self): 
        self.page_source = u"""
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
                            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
                        </ul>
                    </body>
                </html>
            """
        self.crawer = crawer_html_parser.Parselinks()  
       
    def tearDown(self):
        self.crawer.close()
                
    def test_Parse(self):
        """
        Test the MakeUrlGood() function of CrawerPageUtil

        Args:
            none
    
        Returns:
            None
        """
        self.crawer.feed(self.page_source)
        self.crawer.print_result()


if __name__ == '__main__':
    unittest.main()
    pass
