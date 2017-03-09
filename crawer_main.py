# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module implements arg parse for crawer.py.

Authors: songyue02(songyue02@baidu.com)
Date:    2016/04/04
"""

import os
import sys
import logging

import argparse

import crawer_log
import crawer_logic

def get_parser():
    """
        Get arg parser object
        Args:
            None
        Returns:
            arg parser object
    """
    configpath = r'config.ini'
    parser = argparse.ArgumentParser(
        description = 'A mini crawer',
        version = "mini_crawer 1.0.0")
    parser.add_argument(
        '-c',
        type = str,
        metavar = 'FILE',
        default = configpath,
        dest = 'cfg_file',
        help = 'The Config file path. defalut config.ini')
    parser.add_argument(
        '-l',
        type = int,
        metavar = 'LOGLEVEL',
        default = 10,
        dest = 'loglevel',
        help = 'log level. default info(10)')
    return parser

if __name__ == '__main__':
    arg_parser = get_parser()
    args = arg_parser.parse_args()

    crawer_log.init_log("./log/my_program", "Spider.crawler", args.loglevel)

    log = logging.getLogger('Spider.crawler') # Get log Singleton
    conf_file_name = args.cfg_file  # argparse里设置的dest
    log.info("conf name:" + conf_file_name)
    # check config file exist or not
    if os.path.exists(conf_file_name) != True:
        log.error('config file not exist. program end.')
    else:
        if os.path.isfile(conf_file_name) != True:
            log.error('config file is not file. program end.')
        else:
            crawerx = crawer_logic.Crawler(conf_file_name)
            if crawerx.init():
                crawerx.start()
            else:
                log.error('read config fail. program end.')