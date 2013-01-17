# -*- coding: utf-8 -*-
#! path to your python

##################################################################################
#
# This module is for checking existance region of solutions.
# With mean-value-form and krawczyk method.
#
# Reccomended version of python is 2.7.x (or upper)
#
##################################################################################

# import modules
from interval import *
# import module of expanding operator
import operator as op
# import numpy
import numpy as np
# importing FuncDesigner for automatic-differentiation
import FuncDesigner as fd
# importing target function
import fdFunc as func
# importing krawczyk module
import krawczyk as kraw


def fdFunc(no):
	""" define target function from fdFunc-module

	"""
	funcObj = func.fdFunc(no)
	global x
	x = funcObj.x
	y = funcObj.getFunc()
	return y


def checkSomeSolExsist(no, obj, method = 0):
	""" execute checking solutions exist in the region.

	If the region has some solutions, return True.
	But, this bool-value is untrust.

	"""
	selectedMethod = selectMethod(no, obj, method)
	return selectedMethod(no, obj)


def checkOnlySolExist(no, obj, method = 4):
	""" execute checking only solution exist in the region.

	If the region has only-one-solution, return True.

	"""
	selectedMethod = selectMethod(obj, method)
	return selectedMethod(no, obj)


def checkNoSolExist(no, obj, method = 0):
	""" execute checking of non-existence region

	If interval-region does not have solution (No-solution), return True.
	If ruurn False, region has some solutions or unknown whether does.

	"""
	selectedMethod = selectMethod(obj, method)
	return op.not_(selectedMethod(no, obj))


def selectMethod(obj, method = 0):
	""" select method of deciding non-existence region

	"""
	# selected-method
	if method == 1:
		return useFuncIntVal
	elif method == 2:
		return useKrawczyk
	elif method == 3:
		return useMeanValForm
	elif method == 4:
		return onlySolKrawczyk
	# unselect-method
	if isinstance(obj, np.matrixlib.defmatrix.matrix):
		return useFuncIntVal
	elif isinstance(obj, kraw.data):
		#if obj.detI == 0:
		if obj.KI is False:
			return useMeanValForm
		else:
			return useKrawczyk
	else:
		raise TypeError('obj is invalid-type')


#########################################################################################
#
# Methods of deciding Non-existence region about solutions.
#	1: substituting interval-I for the assigned equation
#	2: using the method of Krawczyk
#	3: using the method of Mean Value Form in place of Krawczyk, if singular-matrix
#
#########################################################################################


def useFuncIntVal(no, I):
	""" method-1:

	if F(I) not including 0, I is non-existence region.
	by using interval operation.

	"""
	intVal = fdFuncIntervalVal(no, I)
	for i in range(len(intVal)):
		if interval.subset(0, intVal.item(i)) == False:
			return False
	return True


def useKrawczyk(no, obj):
	""" method-2:

	if subset of K(I) and I is empty-set, I is non-existence region.
	by using Krawczyk.

	"""
	I = obj.I
	KI = obj.KI
	return checkCap(I, KI)


def useMeanValForm(no, obj):
	""" method-3:

	if the mean value form of I not including, I is non-existence region.
	by using mean value form.

	"""
	if isinstance(obj, np.matrixlib.defmatrix.matrix):
		I = obj
	elif isinstance(obj, kraw.data):
		I = obj.I
	MIList = meanValueForm(no, I)
	for i in range(len(MIList)):
		if interval.subset(0, MIList.item(i)) == False:
			return False
	return True


################################################################################
#
# Method of deciding Only-solution-existence region.
#	4: using the method of Krawczyk
#
################################################################################


def onlySolKrawczyk(no, obj):
	""" method-4:

	if the krawczyk include only one solution, return True.

	"""
	I = obj.I
	KI = obj.KI
	for i in range(len(KI)):
		if interval.subset(KI.item(i), I.item(i)) == False:
			return False
	return True


#####################################################################
#
# Extra functions for aboves.
#
#####################################################################


def fdFuncIntervalVal(no, I):
	""" return fd_func(I)

	"""
	y = fdFunc(no)
	mtrx_int = []
	point = {}
	if len(I) == len(x) == len(y):
		for i in range(len(I)):
			point[x[i]] = I.item(i)
		for j in range(len(x)):
			mtrx_int.append(y[j](point))
	else:
		raise ValueError('Unsupported different dimension of x, y and I')
	return np.reshape(mtrx_int, (len(mtrx_int), 1))



def checkCap(I1, I2):
	""" check cap of two intervals

	if each intarvals have common set, this returns true.

	"""
	for i in range(len(I1)):
		if interval.isemptyset(I1.item(i), I2.item(i)) == True:
			return False
	return True


def meanValueForm(no, I):
	""" return value of mean value form list

	dimention of list is dim-x * dim-y

	"""
	y = fdFunc(no)
	point_c = {}
	fc = []
	Ic = []
	# auto-differentiation with FuncDesigner
	dF = kraw.fd_autoDif(no, I)
	y = fdFunc(no)
	for i in range(len(x)):
		point_c[x[i]] = interval.mid(I.item(i))
	for j in range(len(x)):
		fc.append(y[j](point_c))
		Ic.append(I.item(j) - point_c[x[j]])
	# reshape to square-matrix
	dF_mtrx = np.matrix(np.reshape(dF, (len(x), len(x))))
	fc_mtrx = np.matrix(np.reshape(fc, (len(x), 1)))
	Ic_mtrx = np.matrix(np.reshape(Ic, (len(x), 1)))
	return fc_mtrx + dF_mtrx*Ic_mtrx


'''
print "------------------------------------------"
#I = np.matrix([[interval(-1., 1.)], [interval(-1., 1.1)]])
#I = np.matrix([[interval(0.71, 0.81)], [interval(0.8, 0.81)]])
#I = np.matrix([[interval(0.707, 0.708)], [interval(0.707, 0.7081)]])
I = np.matrix([[interval(-0.001, 0.001)], [interval(-0.001, 0.0011)]])
print "Input: "
print I
kobj = kraw.data(I)
print "----------------------------"

print "FuncVal: ", checkNonExistece(I, 1)
#print "FuncVal: ", checkNonExistece(I)
#print "Kraw: ", checkNonExistece(kobj, 2)
#print "Kraw: ", checkNonExistece(kobj)
print "MI: ", checkNonExistece(I, 3)
print "MI: ", checkNonExistece(kobj, 3)
#print "Only: ", checkOnlySolExist(kobj)
print "------------------------------------------"
'''
