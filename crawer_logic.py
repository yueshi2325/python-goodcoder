# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide the concrete realization of the crawler.

Authors: songyue02(songyue02@baidu.com)
Date:    2016/04/04
"""

import os
import re
import traceback
import logging
import urlparse
import collections
import urllib
import time
import threading
import multiprocessing.dummy
import Queue
import time
import ConfigParser

import crawer_page_util
import crawer_html_parser

class Crawler(object):
    """
    The main module that implements the function of the crawler
    
    Parameters:
        config_object: a handle of config file that the crawler can get some parameters
              
    """
    def __init__(self, conf_file_name):
        self.conf_name = conf_file_name

    def init(self):
        """
        init main logic module 
        
        Args:
            filename: name of config file

        member attributes:
            depth: the level of the crawler need to visit base on bfs
            current_depth: the level of the crawler now
            keyword: the target url the crawer need to visit and save the page. Can be None
            timeout: timeout of visiting url
            interval: interval between every visiting
            thread_pool: a instance of thread pool
            visited_hrefs: a set of urls that already visited
            unvisited_hrefs: a queue of urls that the the crawler need to visit
            is_crawling: the flag that the crawler is working or not. 
                False: Not working True: Working
            out_put: the path to store the page source of url
        
        Returns:
            bool, init success or fail
        """
        if self._init_conf_object(self.conf_name):
            # config member
            self.depth = int(self._get_config_value("spider", "max_depth"))  
            self.keyword = self._get_config_value("spider", "target_url")
            self.timeout = int(self._get_config_value("spider", "crawl_timeout"))
            self.interval = int(self._get_config_value("spider", "crawl_interval"))
            self.thread_count = int(self._get_config_value("spider", "thread_count"))
            self.out_put = self._get_config_value("spider", "output_directory")
            init_url_file = self._get_config_value("spider", "url_list_file")

            ### runtime member
            self.current_depth = 0
            self.visited_hrefs = set()  
            self.is_crawling = False
            self.thread_pool = multiprocessing.dummy.Pool(self.thread_count)
            self.unvisited_hrefs = collections.deque() 
            self.currentlevel_unvisited_count = 0   
            if self._read_unvisited_from_config(init_url_file):
                return True
            else:
                return False
        else:
            return False

    def start(self):
        """
        Start the crawler
        """
        
        # check output dir exist or not
        if os.path.exists(self.out_put) != True:
            os.makedirs(self.out_put)
        # get log singleton
        log = logging.getLogger('Spider.crawler')
        log.info('Start Crawling\n')
        self.is_crawling = True
        while self.current_depth < self.depth:
            # Make threads in thread pool to do the task at the same time
            # Operation is not block
            log.info('Depth %d Start. Total %d Links need to visit\n' % (
                self.current_depth, len(self.unvisited_hrefs) - len(self.visited_hrefs)))
            self._assign_current_depth_tasks()
            log.info('Depth %d Finish. Total visited Links: %d\n' % (
                self.current_depth, len(self.visited_hrefs)))
            self.current_depth += 1
        self.stop()

    def stop(self):
        """
        Quit the crawler
        
        """
        self.is_crawling = False
        self.thread_pool.close()
        self.thread_pool.join()
        # get log singleton
        log = logging.getLogger('Spider.crawler')
        log.info("Jobs Done. Bye Bye ^_^")

    def _assign_current_depth_tasks(self):
        # Url of current level need to visit
        current_unvisited_url_count = len(self.unvisited_hrefs)
        self.currentlevel_unvisited_count = (
            self.currentlevel_unvisited_count + current_unvisited_url_count
            )
        urls = []
        for url in self.unvisited_hrefs:
            urls.append(url)
        self.thread_pool.map(self._task_handler, urls) # sync!

    """
        *** crawler method seciton ***        
    """

    def _task_handler(self, url):
        """
        First get the source of web page, than save. Let thread to do this job
        
        Args:
            url: The url need to deal with 
            
        Returns:
            None
        
        """
        # get log singleton
        log = logging.getLogger('Spider.crawler')
        web_page = crawer_page_util.PageUtil(url, self.timeout)
        web_page.init_param()
        if web_page.request():
            log.info("[current depth]:" + str(self.current_depth) + " [request url ok]:" + url)
            self._save_page_to_file(web_page)
            self._add_unvisited_hrefs(web_page)
            self.visited_hrefs.add(url)
        else:
            log.error("[current depth]:" + str(self.current_depth) + "[request fail]:" + url)
            self.visited_hrefs.add(url)
        time.sleep(self.interval)
        
    def _save_page_to_file(self, webPage):
        """
        save page txt to file if url match the pattern
        
        Args:
            webPage: parsed html data
    
        Returns:
            None
        """
        log = logging.getLogger('Spider.crawler')
        url, page_source = webPage.get_data()
        if self.keyword:
            # get log singleton
            
            # python re has a bug. Use [a-zA-z0-9]*  instead
            try:
                if re.search(self.keyword, url, re.IGNORECASE):
                    log.info("[good case]:" + url)
                    self._do_save_page_file(url, page_source)
                else:
                    log.info("[bad case]" + url)
            except (TypeError, Exception) as e:
                # get log singleton
                log = logging.getLogger('Spider.crawler')
                log.error('[URL]: %s ' % url + traceback.format_exc())
                log.error(e)
        else:
            self._do_save_page_file(url, page_source)

    def _do_save_page_file(self, url, page_source):
        """
        save page txt to file if url match the pattern
        
        Args:
            url: url
            page_source: html txt string
    
        Returns:
            None
        """
        log = logging.getLogger('Spider.crawler')
        # Each page saved as a independent file, use the url to name it
        fname = urllib.quote_plus(url)  
        # Deal with the long path problem
        page_file = self.out_put + fname
        if len(page_file) < 1:
            log.error("file name too short")
            return
        if page_file[0] == '.':
            base = os.path.split(os.path.abspath(__file__))[0]
            page_file = base + page_file[1:]    
            if len(page_file) > 256:
                page_file = page_file[:255]
        else:
            if len(page_file) > 256:
                page_file = page_file[:255]
        try:
            with open(page_file, 'w') as fp:
                fp.write(page_source.encode('utf-8'))
                fp.flush()
        except (IOError, UnicodeEncodeError, Exception) as e:
            # get log singleton
            log = logging.getLogger('Spider.crawler')
            log.error('[URL]: %s ' % url + traceback.format_exc())
            log.error(e)

    def _add_unvisited_hrefs(self, webPage):
        """
        Add the url that does not visit yet.Make sure url meet the following requirements:
        1、Only get pages in type http or https
        2、Make sure each url only visit once
        
        Args:
            webPage: a instance of WebPage，through it can get url and the page source of it
            
        Returns:
            None        
        
        """
        url, page_source = webPage.get_data()
        hrefs = self._get_all_hrefs_from_page(url, page_source)
        for href in hrefs:
            if self._is_http_or_Https_protocol(href):
                if not self._is_href_repeated(href):
                    self.unvisited_hrefs.append(href)

    def _is_http_or_Https_protocol(self, href):
        protocal = urlparse.urlparse(href).scheme
        if protocal == 'http' or protocal == 'https':
            return True
        return False

    def _is_href_repeated(self, href):
        #print "check href:"+href
        if href in self.visited_hrefs or href in self.unvisited_hrefs:
            return True
        return False

    def _get_all_hrefs_from_page(self, url, page_source):
        '''解析html源码，获取页面所有链接。返回链接列表'''
        hrefs = []
        try:
            IParser = crawer_html_parser.Parselinks()
            IParser.feed(page_source)
            results = IParser.get_result()
            IParser.close()
            for href in results:
                # Deal with the relative link in js
                if href.find('"') > -1:
                    href = href.split('"')[1]
                if not href.startswith('http'):
                    href = urlparse.urljoin(url, href)  # Deal with the relative link
                hrefs.append(href)
            return hrefs
        except (TypeError, UnicodeEncodeError, Exception) as e:
            # get log singleton
            log = logging.getLogger('Spider.crawler')
            log.critical(traceback.format_exc())
            log.error(e)
            return hrefs

    """
        *** Init method seciton ***       
    """

    def _init_conf_object(self, filename):
        """
        Get handlt of the cpnfig file 
        
        Args:
            filename: name of config file
        
        Returns:
            bool, read conf success or fail
        """
        try:
            self.m_cfg = ConfigParser.ConfigParser()
            self.m_cfg.read(filename)
            return True
        except (Exception) as e:
            # get log singleton
            log = logging.getLogger('Spider.crawler')
            log.error('read config fail:%s. program will end.' % e)
            return False

    def _get_config_value(self, section, option):
        """
        Get option value from conf file 
        
        Args:
            section, option
        
        Returns:
            bool, read conf success or fail
        """
        return self.m_cfg.get(section, option)

    def _read_unvisited_from_config(self, filename):
        """
        Get list of the url the crawler need to visit
        
        Args:
            filename: input url file name
        """
        try:
            with open(filename, "r") as url_file:
                urlset = url_file.readlines()
            for url in urlset: 
                url = url.strip('\n')
                self.unvisited_hrefs.append(url)
            return True
        except IOError as e:
            # get log singleton
            log = logging.getLogger('Spider.crawler')
            log.error('read unvisited url from file error:%s' % e)
            return False