#!/usr/bin/python3
# -*- coding: utf-8 -*-

from wsgiref.handlers import CGIHandler
from web import app as application

if __name__ == '__main__':
    CGIHandler().run(application)
