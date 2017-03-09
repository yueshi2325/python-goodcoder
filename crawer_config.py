# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module implements config reader. done

Authors: songyue02(songyue02@baidu.com)
Date:    2016/04/14
"""
import ConfigParser

class Config(object):
    """
    Class of config model

    Attributes:
        _cfg_file: the path of config file
    """
    def __init__(self, cfg_file):
        '''
        Constructor
        '''
        self._cfg_file = cfg_file
        
    def get(self, section, option):
        """
        Get specify value from the config file
        
        Args:
            section: specify the section of value we need to get
            option: specify the option of value we need to get
    
        Returns:
            The value we need to get
    
        Raises:
            IOError: An error occurred access to the config file.
        """
        cfg = ConfigParser.ConfigParser()
        cfg.read(self._cfg_file)
        return cfg.get(section, option)