# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide the unit-test for CrawerLogic.py.

Authors: songyue02(songyue02@baidu.com)
Date:    2016/04/27 21:00:03
"""
import os
import unittest
import argparse
import sys
import logging

sys.path.append('..')
import crawer_logic
import crawer_page_util


class CrawerTestCase(unittest.TestCase):  
    """
    Class to test the CrawerLogic Class
    
    Attributes:
        targs: replace the command line
        configpath: the path of config file
        parser: a instance to deal with the commmand line input
        args: transfer the list 'target' to cammand line
        crawer: the instance of CrawerLogic class
    """

    def setUp(self): 
        # log
        log = logging.getLogger('Spider.crawler')
        log.setLevel(100)
        formatter = logging.Formatter(
            '[%(levelname)s-%(asctime)s]-tid:%(thread)d-%(filename)s-%(lineno)d:%(message)s')
        fh = logging.FileHandler('test.log')  
        fh.setLevel(logging.DEBUG) 
        fh.setFormatter(formatter) 

        ch = logging.StreamHandler()  
        ch.setLevel(100)  
        ch.setFormatter(formatter)
        
        log.addHandler(ch)  
        log.addHandler(fh)

        # config
        self.targs = ['crawer_test.py', 
                      '-c', 
                      'config_test.ini']
        configpath = r'config_test.ini'
        self.parser = argparse.ArgumentParser(description = 'A mini spider', 
                                              version = "mini_spider 1.0.0") 
        self.parser.add_argument('-c', type = str, metavar = 'FILE', 
                                 default = configpath, 
                                 dest = 'cfg_file',
                                 help = 'The Config file path')
        self.args = self.parser.parse_args(args = self.targs[1:])
        conf_file_name = self.args.cfg_file  #argparse里设置的dest
        self.crawer = crawer_logic.Crawler(conf_file_name)
        self.crawer.init()
           
    def tearDown(self):
        self.crawer = None   
       
    def test_initCrawer(self):
        """
        Test the init function of Crawler class
        
        Args:
            None
    
        Returns:
            None
        """
        self.assertEquals(1, self.crawer.depth)
        self.assertEquals(1, self.crawer.interval)
        self.assertEquals(1, self.crawer.timeout)
        self.assertEquals(8, self.crawer.thread_count)
          
    def test_1_saveTaskResultsNormalWithoutKeyword(self):
        """
        Test the _SavePageToFile function of Crawler class
        Normal Situation, without keyword
        
        Args:
            None
    
        Returns:
            None
        """
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
                            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
                        </ul>
                    </body>
                </html>
            """
        url = "http://pycm.baidu.com:8081"
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko)'
        user_agent = user_agent + ' Chrome/22.0.1229.79 Safari/537.4'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': user_agent,
            'Referer': url,
        }
        timeout = 2
        webpage = crawer_page_util.PageUtil(url, timeout)
        webpage._page_source = page_source
        webpage._headers = headers
        out_put_local = self.crawer.out_put
        self.crawer.out_put = "./test" + self.crawer.out_put.replace('.', '')
        file_normal_without_key = out_put_local + "http%3A%2F%2Fpycm.baidu.com%3A8081"
        self.crawer._save_page_to_file(webpage)
        self.assertEquals(True, os.path.exists(file_normal_without_key))
        os.remove(file_normal_without_key)
          
    def test_2_saveTaskResultsNormalWithKeywordPass(self):
        """
        Test the _SavePageToFile function of Crawler class
        Normal Situation, with keyword and match it
        
        Args:
            None
    
        Returns:
            None
        """       
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
                            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
                        </ul>
                    </body>
                </html>
            """
        url = "http://pycm.baidu.com:8081/test.gif"
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko)'
        user_agent = user_agent + ' Chrome/22.0.1229.79 Safari/537.4'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': user_agent,
            'Referer': url,
        }
        timeout = 1
        webpage = crawer_page_util.PageUtil(url, timeout)
        webpage._page_source = page_source
        webpage._headers = headers
        out_put_local = self.crawer.out_put
        self.crawer.out_put = "./test" + self.crawer.out_put.replace('.', '')
        self.crawer.keyword = '.*.(gif|png|jpg|bmp)$'  
        self.crawer._save_page_to_file(webpage)
        file_nor_with_key = out_put_local + "http%3A%2F%2Fpycm.baidu.com%3A8081%2Ftest.gif"
        self.assertEquals(True, os.path.exists(file_nor_with_key))
        os.remove(file_nor_with_key) 
     
    def test_3_saveTaskResultsNormalWithKeywordFail(self):
        """
        Test the _SavePageToFile function of Crawler class
        Normal Situation, with keyword and not match it
        
        Args:
            None
    
        Returns:
            None
        """ 
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
                            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
                        </ul>
                    </body>
                </html>
            """
        url = "http://pycm.baidu.com:8081"
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko)'
        user_agent = user_agent + ' Chrome/22.0.1229.79 Safari/537.4'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': user_agent,
            'Referer': url,
        }
        timeout = 1
        webpage = crawer_page_util.PageUtil(url, timeout)
        webpage._page_source = page_source
        webpage._headers = headers
        out_put_local = self.crawer.out_put
        self.crawer.out_put = "./test" + self.crawer.out_put.replace('.', '')
        self.crawer.keyword = '.*.(gif|png|jpg|bmp)$'  
        self.crawer._save_page_to_file(webpage)
        file_nor_with_key = out_put_local + "http%3A%2F%2Fpycm.baidu.com%3A8081"
        self.assertEquals(False, os.path.exists(file_nor_with_key))
                
    def test_4_saveTaskResultsLongUrlWithoutKeyword(self):
        """
        Test the _save_page_to_file function of Crawler class
        Long url, without keyword
        
        Args:
            None
    
        Returns:
            None
        """ 
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
                            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
                        </ul>
                    </body>
                </html>
            """
        url = "http://redirect.simba.taobao.com/rd?c=un&w=unionpost&f=http%3A%2F%2Fwww.taobao.com"
        url = url + "%2Fgo%2Fact%2Fmmbd%2Fhd-home.php%3Fpid%3Dmm_15890324_2192376_23736178%26uni"
        url = url + "d%3D&k=b93d93a3e5c25156&p=mm_15890324_2192376_23736178"
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko)'
        user_agent = user_agent + ' Chrome/22.0.1229.79 Safari/537.4'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': user_agent,
            'Referer': url,
        }
        timeout = 1
        webpage = crawer_page_util.PageUtil(url, timeout)
        webpage._page_source = page_source
        webpage._headers = headers
        out_put_local = self.crawer.out_put
        if os.path.exists(out_put_local) != True:
            os.makedirs(out_put_local)
        self.crawer.out_put = "./test/test" + self.crawer.out_put.replace('.', '')
        self.crawer._save_page_to_file(webpage) 
        self.assertEquals(True, len(os.listdir(out_put_local)) > 0)     
     
    def test_5_saveTtaskResultsLongUrlWithKeyword(self):
        """
        Test the _SavePageToFile function of Crawler class
        Long url, with keyword
        
        Args:
            None
    
        Returns:
            None
        """ 
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
                            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
                        </ul>
                    </body>
                </html>
            """
        url = "http://redirect.simba.taobao.com/rd?c=un&w=unionpost&f=http%3A%2F%2Fwww.taobao.com"
        url = url + "%2Fgo%2Fact%2Fmmbd%2Fhd-home.php%3Fpid%3Dmm_15890324_2192376_23736178%26uni"
        url = url + "d%3D&k=b93d93a3e5c25156&p=mm_15890324_2192376_23736178"
        user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko)'
        user_agent = user_agent + ' Chrome/22.0.1229.79 Safari/537.4'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': user_agent,
            'Referer': url,
        }
        timeout = 1
        webpage = crawer_page_util.PageUtil(url, timeout)
        webpage._page_source = page_source
        webpage._headers = headers
        out_put_local = self.crawer.out_put
        if os.path.exists(out_put_local) != True:
            os.makedirs(out_put_local)
        self.crawer.out_put = "./test/test" + self.crawer.out_put.replace('.', '')        
        self.crawer.keyword = 'taobao'
        self.crawer._save_page_to_file(webpage)
        self.assertEquals(True, len(os.listdir(out_put_local)) > 0)
                
    def test_getAllHrefsFromPage(self):
        """
        Test the _GetAllHrefsFromPage function of Crawler class
        
        Args:
            None
    
        Returns:
            None
        """ 
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
                            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
                            <li><a href='javascript:location.href="page5.html"'>page 5</a></li>
                        </ul>
                    </body>
                </html>
            """
        url = "http://pycm.baidu.com:8081"
        hrefs = ['http://pycm.baidu.com:8081/page1.html', 
                 'http://pycm.baidu.com:8081/page2.html', 
                 'http://pycm.baidu.com:8081/page3.html', 
                 'http://pycm.baidu.com:8081/mirror/index.html', 
                 'http://pycm.baidu.com:8081/page4.html', 
                 'http://pycm.baidu.com:8081/page5.html']
        self.assertEquals(hrefs, self.crawer._get_all_hrefs_from_page(url, page_source))
         
    def test_getAllHrefsFromPageWrong(self):
        """
        Test the _GetAllHrefsFromPage function of Crawler class
        Exception
        
        Args:
            None
    
        Returns:
            None
        """ 
        url = "http://pycm.baidu.com:8081"
        self.assertEquals([], self.crawer._get_all_hrefs_from_page(url, None))
        

if __name__ == '__main__':
    unittest.main()
