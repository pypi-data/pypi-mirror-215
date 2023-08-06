#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import logging
import colorlog

class Logger:
    def __init__(self, set_level="INFO",name='main',log_file=''):
        """
        :param set_level: 日志级别["NOTSET"|"DEBUG"|"INFO"|"WARNING"|"ERROR"|"CRITICAL"]，默认为INFO
        :param name: 日志中打印的name
        :param log_file: 日志文件
        """

        self.__logger = logging.getLogger(name)
        if not set_level:
            set_level = self._exec_type()
        self.setLevel(getattr(logging, set_level.upper()) if hasattr(logging, set_level.upper()) else logging.INFO)


        if log_file:
            file_handler = logging.FileHandler(log_file,'a',encoding='utf-8')
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
            self.__logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_color_formatter())
        self.__logger.addHandler(console_handler)

    def _get_color_formatter(self):
        color_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "green",
                "INFO": "blue",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            reset=True
        )
        return color_formatter
 
    def __getattr__(self, item):
        return getattr(self.logger, item)
 
    @property
    def logger(self):
        return self.__logger
 
    @logger.setter
    def logger(self, func):
        self.__logger = func
 
    def _exec_type(self):
        return "DEBUG" if os.environ.get("IPYTHONENABLE") else "INFO"
    