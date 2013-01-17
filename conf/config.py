# -*- coding: utf-8 -*-
#! path to your python

######################################################################
#
# This is cnfiguration file for all-solution.
#
# Auth. era, 2012/11/20
######################################################################


""" Import modules """
import os, sys


""" Define module-path """
ABS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ABS_APP_PATH = ABS_DIR_PATH + '/../'
LIB_DIR_NAME = 'lib'
ABS_LIB_PATH = ABS_APP_PATH + LIB_DIR_NAME
LIB_EXT_DIR_NAME = 'ext'
ABS_LIB_EXT_PATH = ABS_LIB_PATH + '/' + LIB_EXT_DIR_NAME


""" Set sys.path """
sys.path.append(ABS_LIB_EXT_PATH)


