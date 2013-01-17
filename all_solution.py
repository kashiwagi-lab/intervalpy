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
# importing krawczyk module
import krawczyk as kraw
# importing module of checking solution-existing
import sol_existence as solex

# for debugging
from print_r import print_r
from time import time


def fdFunc(no):
	""" define target function from fdFunc-module

	"""
	funcObj = func.fdFunc(no)
	global x
	x = funcObj.x
	y = funcObj.getFunc()
	return y


def initList(I):
	""" initialize List by I

	"""
	List = []
	List.append(I)
	return List


def allSolution(no, I):
	""" function of all solution

	"""

	""" step-1 """
	#print "step-1:"
	# リストList の初期化
	List = initList(I)
	# 唯一解を持つリスト
	solI = []
	# 分割回数の保持
	numSplit = 0

	""" step-2 """
	#print "step-2"
	print "=========================== START ============================="
	print "List of intervals: ",
	while List != []:
		if numSplit%50 == 0:
			print numSplit, ": ", str(len(List))
		#print List
		# リストList の先頭要素を取り出しI とする
		I = List.pop(0)

		""" step-3 """
		#print "step-3:"
		# F(I) によりI に解が存在するか判定(弱い非存在判定)
		if solex.checkNoSolExist(no, I, method = 1) == True:
			# I を初期化してstep 2 へ戻る
			I = []
			continue
		else:
			pass

		""" step-4 """
		#print "step-4:"
		# Krawczyk 法による唯一解の判定
		krawObj = kraw.data(no, I)
		if not krawObj.KI is False:
			if solex.checkOnlySolExist(no, krawObj, method = 4) == True:
				print I
				solI.append(I)
				continue
		else:
			pass

		""" step-5 """
		#print "step-5:"
		# 区間I, K(I) が空集合であればI に解は存在しない(強い非存在判定)
		if not krawObj.KI is False:
			# the krawczyk-method
			if solex.checkNoSolExist(no, krawObj, method = 2) == True:
				I = []
				continue
		else:
			# the mean-value-form
			if solex.checkNoSolExist(no, I, method = 3) == True:
				I = []
				continue

		""" step-6 """
		#print "step-6:"
		# 区間の分割
		for i in range(len(split(I))):
			List.append(split(I)[i])
		numSplit += 1
		continue

	# 唯一解を持つ区間を返す
	# 分割回数の表示
	#print '\n\r'
	print "The number of split-I: "+str(numSplit)
	return solI


def improveVerification(no, solIList):
	""" higher numerical verification

	"""
	# number counting improved-solI
	countImprovedSolI = 0
	# max-loop of improve soilI
	maxLoop = 100
	if len(solIList) == 0:
		msg = 'Assigned equation has no-solution in the interval-list.'
		print "============================ END =============================="
		return msg
	improvedSolIList = []
	for i in range(maxLoop):
		countImprovedSolI += 1
		if len(solIList) != 0:
			solI = solIList.pop(0)
			if evaluateImproveVerification(solI) == True:
				improvedSolIList.append(solI)
			else:
				# 区間反復法
				solIList.append(kraw.krawczyk(no, solI))
		else:
			break
	print "The number of improving verification: "+str(countImprovedSolI)
	print "============================ END =============================="
	return improvedSolIList


def split(I):
	""" splitting List

	"""
	# Deep-copy による区間の複製
	Isucc = np.mat(I.copy())
	Ipred = np.mat(I.copy())
	# 区間幅の最も大きいものを分割
	Isucc[maxElementInMatrix(I)] = interval(I.item(maxElementInMatrix(I)).inf, interval.medsucc(I.item(maxElementInMatrix(I))))
	Ipred[maxElementInMatrix(I)] = interval(interval.medpred(I.item(maxElementInMatrix(I))), I.item(maxElementInMatrix(I)).sup)
	return [Ipred, Isucc]


def maxElementInMatrix(I):
	""" return list-index of max element in one matrix

	"""
	width = []
	for i in range(len(I)):
		width.append(interval.width(I.item(i)))
	return width.index(max(width))


def evaluateImproveVerification(solI):
	""" evaluate calcurating-error and check whether its allowable-value

	If error is under allowable-value, return True.

	"""
	# criteria of allowable-error
	allowableError = 1e-7
	for i in range(len(solI)):
		# calcurate width-error of interval
		widthError = interval.width(solI.item(i))
		if widthError >= allowableError:
			return False
	return True





# 入力する解区間
#I = func.initI()
#print_r(improveVerification(allSolution(I)))
