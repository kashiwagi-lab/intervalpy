# -*- coding: utf-8 -*-
#! path to your python

######################################################################
#
# This module is for only defining target functions.
#
######################################################################
# importing modules for defining functions
import numpy as np
import scipy as sp
import FuncDesigner as fd
from interval import *


class fdFunc(object):

	""" define variable x """
	# no : x-dimention
	xDimList  = { \
		0: 2,\
		1: 2,\
		2: 2,\
		3: 2,\
		4: 2,\
		5: 3,\
		6: 3,\
		7: 2,\
		8: 2,\
		9: 2,\
		10: 2,\
		11: 2,\
		12: 2,\
		13: 2,\
		14: 5,\
		15: 3,\
		16: 4\
		}

	def __init__(self, no):
		""" Function No. """
		self.no = no
		self.x = [0.0 for i in range(self.xDimList[no])]


	def initFunc(self):
		""" return selected function

		"""
		if self.no == 0:
			return self.default_function
		elif self.no == 1:
			return self.sample_function_1
		elif self.no == 2:
			return self.sample_function_2
		elif self.no == 3:
			return self.sin_function
		elif self.no == 4:
			return self.sincos_function
		elif self.no == 5:
			return self.function_3_dim
		elif self.no == 6:
			return self.function_3_dim_2
		elif self.no == 7:
			return self.badCond
		elif self.no == 8:
			return self.Burden
		elif self.no == 9:
			return self.Nosol
		elif self.no == 10:
			return self.GE1
		elif self.no == 11:
			return self.Duffing
		elif self.no == 12:
			return self.Shinohara1
		elif self.no == 13:
			return self.Shinohara2
		elif self.no == 14:
			return self.Shinohara3
		elif self.no == 15:
			return self.Cyclo
		elif self.no == 16:
			return self.Kinkox
		else:
			raise ValueError("Variable 'no' is invalid value.")


	def getFunc(self):
		""" return selected initial function

		"""
		return self.initFunc()(self.x)


	def initI(self):
		""" return selected initial interval

		"""
		return self.initFunc()(self.x, True)



	######################################################################
	#
	# List of Sample Functions
	#
	######################################################################


	def default_function(self, x, retI = False):
		""" no = 0: default function

		{ x1^2 + x2^2 -1 = 0
		{ x1 - x2 = 0
		one true solution which sample function has is below:
		x1 = x2 = (2^(1/2))/2
		(=~ 0.70710678)

		"""
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		y[0] = x[0] * x[0] + x[1] * x[1] - 1
		y[1] = x[0] - x[1]
		if retI == True:
			#return np.matrix([[interval(-1.1, 1.)], [interval(-1., 1.)]])
			return np.matrix([[interval(-10., 10.)], [interval(-10., 10.)]])
		return y


	def sample_function_1(self, x, retI = False):
		""" no = 1: sample function 1

		{ x1^2 - x2 = 0
		{ (1/2)*x1 - x2 = 0
		true value
		(x1, x2) = (0, 0), (0.5, 0.25)

		"""
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		y[0] = x[0] * x[0] - x[1]
		y[1] = 0.5 * x[0] - x[1]
		if retI == True:
			return np.matrix([[interval(-2.2, 2.1)], [interval(-1., 2.)]])
		return y


	def sample_function_2(self, x, retI = False):
		""" no = 2: sample function 2

		{ x1^2 - x2 = 0
		{ -x1^2 + 2*x1 - x2 = 0
		true value
		(x1, x2) = (0, 0), (1, 1)

		"""
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		y[0] = x[0] * x[0] - x[1]
		y[1] = -x[0] * x[0] + 2 * x[0]  - x[1]
		if retI == True:
			return np.matrix([[interval(-10., 10.)], [interval(-10., 10.)]])
		return y


	def sin_function(self, x, retI = False):
		""" no = 3: function including sin

		{ (pi/2)*sin(x1) - x2 = 0
		{ x1 - x2 = 0
		true value
		(x1, x2) = (0, 0), (1.57079633.., 1.57079633..), (-1.5709633.., -1.57079633..)

		"""
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		#y[0] = 1.57079633 * fd.sin(x[0]) - x[1]
		y[0] = (np.pi/2) * fd.sin(x[0]) - x[1]
		y[1] = x[0] - x[1]
		if retI == True:
			return np.matrix([[interval(-3.1, 3.)], [interval(-2., 2.)]])
		return y


	def sincos_function(self, x, retI = False):
		""" no = 4: function including sine and cosine

		{ sin(x1)*cos(x1) - x2 = 0
		{ x1^2 - 6*x1 + 8 - x2 = 0
		true value
		(x1, x2) = (,), (,)

		"""
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		'''
		y[0] = fd.sin(x[0]) * fd.cos(x[0]) - x[1]
		y[1] = x[0] * x[0] - 6 * x[0] + 8 - x[1]
		'''
		'''
		y[0] = fd.sin(x[0])*fd.cos(x[1]) - x[0] + 1.
		y[1] = fd.cos(x[0])*fd.sin(x[1]) + x[1] - 1.
		'''
		y[0] = fd.sin(x[0]) + fd.cos(x[1]) - x[0]
		y[1] = fd.cos(x[0])*fd.sin(x[1]) - x[1] + 1.
		if retI == True:
			return np.matrix([[interval(-100., 100.)], [interval(-100., 100.)]])
		return y


	def function_3_dim(self, x, retI = False):
		""" no = 5: function of 3-dimention

		{ x1 + x2 + x3 = 6
		{ 3*x1 + 2*x2 -2*x3 = 1
		{ 2*x1 - x2 + 3*x3 = 9
		true value
		(x1, x2, x3) = (1, 2, 3)

		"""
		y = [0.0 for i in range(3)]
		x[0], x[1], x[2] = fd.oovars('x0', 'x1', 'x2')
		y[0] = x[0] + x[1] + x[2] - 6
		y[1] = 3*x[0] + 2*x[1] - 2*x[2] - 1
		y[2] = 2*x[0] - x[1] + 3*x[2] - 9
		if retI == True:
			#return np.matrix([[interval(-1.1, 5.)], [interval(-1., 5.)], [interval(-1., 5.1)]])
			return np.matrix([[interval(-50., 50.)], [interval(-50., 50.)], [interval(-50., 50.)]])
		return y


	def function_3_dim_2(self, x, retI = False):
		""" no = 6: function of 3-dimention

		{ x1*x2 - 9 = 0
		{ x2*x3 - 6 = 0
		{ x3*x1 - 6 = 0
		true value
		(x1, x2, x3) = (3, 3, 2), (-3, -3, -2)

		"""
		y = [0.0 for i in range(3)]
		x[0], x[1], x[2] = fd.oovars('x0', 'x1', 'x2')
		y[0] = x[0] * x[1] - 9
		y[1] = x[1] * x[2] - 6
		y[2] = x[2] * x[0] - 6
		if retI == True:
			#return np.matrix([[interval(-6.1, 5.)], [interval(-5., 6.)], [interval(-6., 7.1)]])
			#return np.matrix([[interval(-10.1, 15.)], [interval(-15., 20.)], [interval(-16., 10.1)]])
			return np.matrix([[interval(-100, 100.)], [interval(-100., 100.)], [interval(-100., 100.)]])
		return y


	def badCond(self, x, retI = False):
		""" no = 7: BadCond

		{ x1^2 - x2 = 0
		{ (1 - param) * x1^2 - x2 + param = 0
		true value
		(x1, x2) = (, ), (, )

		"""
		#param = 0.0000001
		#param = 0.01
		param = 0.001
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		y[0] = x[0]*x[0] - x[1]
		y[1] = (1 - param)*x[0]*x[0] - x[1] + param
		if retI == True:
			return np.matrix([[interval(-10., 10.)], [interval(-10., 10.)]])
		return y


	def Burden(self, x, retI = False):
		""" no = 8: Burden

		{ x1*(4 - 0.0003*x1 - 0.0004*x2) = 0
		{ x2*(2 - 0.0002*x1 - 0.0001*x2) = 0
		true value
		(x1, x2) = ?

		"""
		#param = 0.0001
		param = 0.1
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		y[0] = x[0]*(4. - 3.*param*x[0] - 4.*param*x[1])
		y[1] = x[1]*(2. - 2.*param*x[0] - 1.*param*x[1])
		if retI == True:
			#return np.matrix([[interval(0., pow(10., 10))], [interval(0., pow(10., 10))]])
			return np.matrix([[interval(-1., pow(10., 10))], [interval(0., pow(10., 10)+1)]])
		return y


	def Nosol(self, x, retI = False):
		""" no = 9: No-solutions

		{ x1^2 - x2 = 0
		{ x1^2 - x2 + param
		true value
		(x1, x2) = None

		"""
		param = 0.001
		#param = 0.1
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		y[0] = x[0]*x[0] - x[1]
		y[1] = x[0]*x[0] - x[1] + param
		if retI == True:
			return np.matrix([[interval(-10., 10.)], [interval(-10., 10.)]])
		return y


	def GE1(self, x, retI = False):
		""" no = 10: GE1

		{ -1/(1 + x1) + x2/(1 + x2) = 0
		{ 1/(1 + x1) - x2/(x1 + x2) = 0
		true value = ?

		"""
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		y[0] = -1./(1. + x[0]) + x[1]/(1. + x[1])
		y[1] = 1./(1. + x[0]) - x[1]/(x[0] + x[1])
		if retI == True:
			return np.matrix([[interval(1e-4, 100.)], [interval(1e-4, 100.)]])
			#return np.matrix([[interval(0.1, 10.)], [interval(0.01, 11.)]])
		return y


	def Duffing(self, x, retI = False):
		""" no = 11: Duffing-equation

		{ y(0) = -x(0) + B + 0.1 * x(1) + 0.75 * (x(0)*x(0)*x(0) + x(0) *x(1) * x(1))
		{ y(1) = - x(1) + 0.1 * x(0) + 0.75 * (x(0)*x(0)*x(1) + x(1)*x(1)*x(1))
		true value = 5?

		"""
		#B = 0.
		B = 0.15
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		y[0] = -1.*x[0] + B + 0.1*x[1] + 0.75*(x[0]*x[0]*x[0] + x[0]*x[1]*x[1])
		y[1] = -1.*x[1] + 0.1*x[0] + 0.75*(x[0]*x[0]*x[1] + x[1]*x[1]*x[1])
		if retI == True:
			return np.matrix([[interval(-1e+8, 1e+8)], [interval(-1e+8, 1e+8)]])
			#return np.matrix([[interval(-1e+4, 1e+4)], [interval(-1e+4, 1e+4)]])
		return y


	def Shinohara1(self, x, retI = False):
		""" no = 12: Shinohara1

		{ y(0) = p*p*p*p*p - 10.*p*p*p*q*q + 5.*p*q*q*q*q
				- 2.*p*p*p*p + 12.*p*p*q*q - 2.*q*q*q*q
				+ 10.*p*p*p - 30.*p*q*q - 9.*p + 3.
		{ y(1) = q*q*q*q*q - 10.*p*p*q*q*q + 5.*p*p*p*p*q
				- 8.*p*p*p*q + 8.*p*q*q*q + 30.*p*p*q
				-10.*q*q*q - 9.*q
		true value = ?

		"""
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		p = x[0]
		q = x[1]
		y[0] = p*p*p*p*p - 10.*p*p*p*q*q + 5.*p*q*q*q*q\
				- 2.*p*p*p*p + 12.*p*p*q*q - 2.*q*q*q*q\
				+ 10.*p*p*p - 30.*p*q*q - 9.*p + 3.
		y[1] = q*q*q*q*q - 10.*p*p*q*q*q + 5.*p*p*p*p*q\
				- 8.*p*p*p*q + 8.*p*q*q*q + 30.*p*p*q\
				-10.*q*q*q - 9.*q
		if retI == True:
			#return np.matrix([[interval(-5.1, 5.)], [interval(-5., 5.1)]])
			return np.matrix([[interval(-100., 100.)], [interval(-100., 100.)]])
		return y


	def Shinohara2(self, x, retI = False):
		""" no = 13: Shinohara2

		{ y(0) = p*p*p*p*p - 10.*p*p*p*q*q + 5.*p*q*q*q*q
			- 3.*p*p*p*p + 18.*p*p*q*q - 3.*q*q*q*q
			- 2.*p*p*p + 6.*p*q*q + 3.*p*p*q - q*q*q
			+ 12.*p*p - 12.*q*q - 10.*p*q - 8.*p + 8.*q;
		{ y(1) = 5.*p*p*p*p*q - 10.*p*p*q*q*q + q*q*q*q*q
			- 12.*p*p*p*q + 12.*p*q*q*q - p*p*p + 3.*p*q*q
			- 6.*p*p*q + 2.*q*q*q + 5.*p*p - 5.*q*q
			+ 24.*p*q - 8.*p - 8.*q + 4.;
		true value = ?
		output:
		0 = [[[-2.09868411349,-2.09868411345]]
		    [[-0.455089860584,-0.455089860541]]]
		1 = [[[0.999999999995,1.0]]
		    [[-4.51311746098e-12,4.51285733701e-12]]]
		2 = [[[0.0986841134678,0.0986841134678]]
		    [[0.455089860562,0.455089860562]]]

		"""
		y = [0.0 for i in range(2)]
		x[0], x[1] = fd.oovars('x0', 'x1')
		p = x[0]
		q= x[1]
		y[0] = p*p*p*p*p - 10.*p*p*p*q*q + 5.*p*q*q*q*q\
			- 3.*p*p*p*p + 18.*p*p*q*q - 3.*q*q*q*q\
			- 2.*p*p*p + 6.*p*q*q + 3.*p*p*q - q*q*q\
			+ 12.*p*p - 12.*q*q - 10.*p*q - 8.*p + 8.*q
		y[1] = 5.*p*p*p*p*q - 10.*p*p*q*q*q + q*q*q*q*q\
			- 12.*p*p*p*q + 12.*p*q*q*q - p*p*p + 3.*p*q*q\
			- 6.*p*p*q + 2.*q*q*q + 5.*p*p - 5.*q*q\
			+ 24.*p*q - 8.*p - 8.*q + 4.
		if retI == True:
			#return np.matrix([[interval(-3., 3.)], [interval(-3., 3.)]])
			return np.matrix([[interval(-10., 10.)], [interval(-10., 10.)]])
		return y


	def Shinohara3(self, x, retI = False):
		""" no = 14: Shinohara3

		{ y(0) = p*p*p - 2.*p*q + r + 0.75*p + 1.
		{ y(1) = p*p*q - q*q - p*r +s + 0.75*q + 0.25
		{ y(2) = p*p*r - p*s - q*r + t + 0.75*r + 0.75
		{ y(3) = p*p*s - p*t - q*s + 0.75*s
		{ y(4) = p*p*t - q*t + 0.75*t - 0.25
		true value = ?

		"""
		y = [0.0 for i in range(5)]
		x[0], x[1], x[2], x[3], x[4] = fd.oovars('x0', 'x1', 'x2', 'x3', 'x4')
		p = x[0]
		q = x[1]
		r = x[2]
		s = x[3]
		t = x[4]
		y[0] = p*p*p - 2.*p*q + r + 0.75*p + 1.
		y[1] = p*p*q - q*q - p*r +s + 0.75*q + 0.25
		y[2] = p*p*r - p*s - q*r + t + 0.75*r + 0.75
		y[3] = p*p*s - p*t - q*s + 0.75*s
		y[4] = p*p*t - q*t + 0.75*t - 0.25
		if retI == True:
			'''
			return np.matrix([[interval(-1.501, 2.)],\
							  [interval(-0.6001, 3.)],\
							  [interval(-1.501, 2.5)],\
							  [interval(-0.501, 1.9)],\
							  [interval(-1.01, 1.002)]])
			'''
			return np.matrix([[interval(-3., 3.)],\
							  [interval(-3., 3.)],\
							  [interval(-3., 3.)],\
							  [interval(-3., 3.)],\
							  [interval(-3., 3.)]])
		return y


	def Cyclo(self, x, retI = False):
		""" no = 15: Cyclo

		true value
		(x1, x2, x3) = ?

		"""
		y = [0.0 for i in range(3)]
		x[0], x[1], x[2] = fd.oovars('x0', 'x1', 'x2')
		y[0] = -x[1]*x[1]*x[2]*x[2] - x[1]*x[1] + 24.*x[1]*x[2] - x[2]*x[2] -13.
		y[1] = -x[0]*x[0]*x[2]*x[2] - x[2]*x[2] + 24.*x[2]*x[0] - x[0]*x[0] -13.
		y[2] = -x[0]*x[0]*x[1]*x[1] - x[0]*x[0] + 24.*x[0]*x[1] - x[1]*x[1] -13.
		if retI == True:
			#return np.matrix([[interval(0., 1e5)], [interval(0., 1e5)], [interval(0., 1e5)]])
			return np.matrix([[interval(-1e4, 1e4)], [interval(-1e4, 1e4)], [interval(-1e4, 1e4)]])
		return y


	def Kinkox(self, x, retI = False):
		""" no = 16: Kinkox

		"""
		y = [0.0 for i in range(4)]
		x[0], x[1], x[2], x[3] = fd.oovars('x0', 'x1', 'x2', 'x3')
		c1 = x[0]
		c2 = x[1]
		s1 = x[2]
		s2 = x[3]
		y[0] = -1. + 6.*(c1*c2 - s1*s2) + 10.*c1
		y[1] = -4. + 6.*(c1*s2 + c2*s1) + 10.*s1
		y[2] = c1*c1 + s1*s1 - 1
		y[3] = c2*c2 + s2*s2 - 1
		if retI == True:
			return np.matrix([[interval(-10., 10.)], [interval(-10., 10.)], [interval(-10., 10.)], [interval(-10., 10.)]])
		return y

