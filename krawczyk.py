# -*- coding: utf-8 -*-
#! path to your python

from __future__ import division
# importing numpy
import numpy as np
# importing scipy
import scipy as sp
# importing interval library
from interval import *
# importing FuncDesigner for automatic-differentiation
import FuncDesigner as fd
# importing target function
import fdFunc as func


########################################################################
#
# Data hold class
#
########################################################################


class data(object):
	""" Class holding data

	data: I, det(I), K(I)

	"""


	""" Attribute """

	I = None

	detI = None

	KI = None


	""" Method """

	def __init__(self, no, I, x=None, y=None):
		""" initialize data class

		"""
		self.no = no
		self.I = I
		if x is None or y is None:
			self.x, self.y = fdFunc(self.no)
		else:
			self.x = x
			self.y = y
		self.KI = krawczyk(self.no, self.I, self.x, self.y)

	def setDeterminant(self):
		""" setting determinant of I: self.detI

		"""
		self.detI = getDetKrawczykL(self.no, self.I, self.x, self.y)

	def setKrawczyk(self):
		""" setting krawczyk of I: self.KI

		"""
		self.KI = krawczyk(self.no, self.I, self.x, self.y)



########################################################################
#
# The krawczyk method
#
########################################################################


def fdFunc(no):
	""" define target function from fdFunc-module

	"""
	funcObj = func.fdFunc(no)
	x = funcObj.x
	y = funcObj.getFunc()
	return x, y


def getDetKrawczykL(no, I, x, y):
	""" getting determinant of L in krawczyk

	"""
	if x is None or y is None:
		x, y = fdFunc(no)
	# �����c�ν����
	c = [0.0 for k in range(len(I))]
	# ����ͤ�����
	for i in range(len(I)):
		# ��ֹ���I�����Ǥ��˼��Ф�
		intI = I.item(i)
		# ���intI�������
		c[i] = interval.mid(intI)
	# func�Σ�����ʬ: f'(c)
	df = fd_autoDif(no, c, x, y)
	# f'(c)����ʬ��̤����
	if len(x) == len(y):
		df_mtrx = np.matrix(np.reshape(df, (len(x), len(x))))
	else:
		raise ValueError('Unsupported not square-matrix')
	return np.linalg.det(df_mtrx)


def krawczyk(no, I, x=None, y=None):
	""" verify approx by krawczyk method

	"""
	if x is None or y is None:
		x, y = fdFunc(no)
	# �����c�ν����
	c = [0.0 for k in range(len(I))]
	# ����ͤ�����
	for i in range(len(I)):
		# ��ֹ���I�����Ǥ��˼��Ф�
		intI = I.item(i)
		# ���intI�������
		c[i] = interval.mid(intI)
	# func�Σ�����ʬ: f'(c)
	df = fd_autoDif(no, c, x, y)
	# f'(c)����ʬ��̤����
	if len(x) == len(y):
		df_mtrx = np.matrix(np.reshape(df, (len(x), len(x))))
	else:
		raise ValueError('Unsupported not square-matrix')
	if np.linalg.det(df_mtrx) == 0:
		#print "Notice: L is singular-matrix!"
		return False
	# numpy�ˤ��չ��������
	iL = np.linalg.inv(df_mtrx)
	# f'�ζ�����F'(I)
	dF = fd_autoDif(no, I, x, y)
	# F'(I)����ʬ��̤����
	dF_mtrx = np.matrix(np.reshape(dF, (len(x), len(x))))
	# ñ�̹���
	E = np.matrix(np.identity(len(x)))
	# �̾����γ�ǧ
	dis = E - (iL * dF_mtrx)
	# �Υ��η׻�
	norm = getNorm(dis, x)
	# �̾�����Ƚ��
	if norm >= 1.0:
		#raise ValueError('not contractibility')
		#print "Notice: not contractibility!"
		#print 'C'
		pass
	# ����ݾ�
	fc = fdFunc_val(no, c, x, y)
	fc_mtrx = np.matrix(np.reshape(fc, (len(fc), 1)))
	c_mtrx = np.matrix(np.reshape(c, (len(c), 1)))
	K = c_mtrx - iL * fc_mtrx + dis * (I - c_mtrx)
	return K


def fdFunc_val(no, c, x, y):
	""" return fdFunc(a)

	"""
	#if x is None or y is None:
	#	x, y = fdFunc(no)
	point = {}
	fc = []
	for i in range(len(c)):
		if isinstance(c, np.matrix):
			point[x[i]] = c.item(i)
		else:
			point[x[i]] = c[i]
	for i in range(len(x)):
		fc.append(y[i](point))
	return fc


def fd_autoDif(no, c, x, y):
	""" auto-differentiation with FuncDesigner

	"""
	# fd�ˤ��ؿ��μ���
	#if x is None or y is None:
	#	x, y = fdFunc(no)
	# ��ʬ��
	point = {}
	for k in range(len(c)):
		if isinstance(c, np.matrix):
			point[x[k]] = c.item(k)
		else:
			point[x[k]] = c[k]
	# ��ʬ�ؿ��ν����
	df = []
	for i in range(len(y)):
		dfList = None
		dfList = y[i].D(point)
		for j in range(len(x)):
			if dfList.has_key(x[j]):
				df.append(dfList[x[j]])
			else:
				df.append(0.)
	#for i in range(len(y)):
	#	for j in range(len(x)):
	#		df.append(y[i].D(point, x[j]))
	return df


def getNorm(mtrx, x):
	""" return norm of matrix including interval

	"""
	val = []
	for i in range(len(mtrx) * len(mtrx)):
		if isinstance(mtrx.item(i), interval):
			intVal = mtrx.item(i)
			val.append(interval.norm(intVal))
		elif isinstance(mtrx.item(i), int):
			val.append(mtrx.item(i))
		elif isinstance(mtrx.item(i), float):
			val.append(mtrx.item(i))
		else:
			raise ValueError
	abs_mtrx = np.matrix(np.reshape(val, (len(x), len(x))))
	norm = np.linalg.det(abs_mtrx)
	return norm



def trigger():
	""" trigger func for calcurating time

	"""
	no = 0
	I = np.matrix([[interval(-0.11, 0.1)], [interval(-0.1, 0.1)]])
	krawczyk(no, I)


'''
print "------------------------------------------------------------"
# ���Ϥ������
I = np.matrix([[interval(0.7, 0.8)], [interval(0.7, 0.8)]])
print "Input: "
print I
# Krawczykˡ�ˤ�������ݾ�
print "Output: "
print krawczyk(I)
print "------------------------------------------------------------"
'''
