# -*- coding: utf-8 -*-
#! path to your python
#
#
# This is math module for interval arithmetic.
# Packaged math function is below:
#
# Reccomended version of python is 2.7.x (or upper)
# Auth. era

# requirements of importing modules
#from interval import *
import numpy as np
from print_r import print_r


def factorial(n):
	""" the factorial of n

	"""
	val = 1
	for i in range(1, int(n + 1)):
		val = val * i
	return val


def isscalar(x):
	""" extend numpy.isscalar for interval

	"""
	if hasattr(x, "__isscalar__"):
		return x.__isscalar__()
	else:
		return np.isscalar(x)


def sin(x):
	""" sine fanction for interval

	"""
	if isinstance(x, np.ndarray):
		x = x.item()
	if hasattr(x, "__sin__"):
		return x.__sin__()
	else:
		return np.sin(x)


def cos(x):
	""" cosine fanction for interval

	"""
	if isinstance(x, np.ndarray):
		x = x.item()
	if hasattr(x, "__cos__"):
		return x.__cos__()
	else:
		return np.cos(x)


def asfarray(x):
	""" override of numpy.asfarray for interval

	"""
	if hasattr(x, '__asfarray__'):
		return x.__asfarray__()
	elif isinstance(x, np.ndarray):
		#if hasattr(x.item(0), '__asfarray__'):
		if hasattr(x.item(), '__asfarray__'):
			#return x.item(0).__asfarray__()
			return x.item().__asfarray__()
	return np.asfarray(x)


