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
	x = funcObj.x
	y = funcObj.getFunc()
	return x, y


def initList(I):
	""" initialize List by I

	"""
	List = []
	List.append(I)
	return List


def allSolution(no, I, x=None, y=None):
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
	flag = None
	# 対象funcの設定
	if x is None or y is None:
		x, y = fdFunc(no)

	""" step-2 """
	#print "step-2"
	#print "=========================== START ============================="
	#print "List of intervals: ",
	while List != []:
		if numSplit%50 == 0:
			#print numSplit, ": ", str(len(List))
			pass
		#print List
		# リストList の先頭要素を取り出しI とする
		I = List.pop(0)

		""" step-3 """
		#print "step-3:"
		# F(I) によりI に解が存在するか判定(弱い非存在判定)
		if solex.checkNoSolExist(no, I, x, y, method = 1) == True:
			# I を初期化してstep 2 へ戻る
			#I = []
			#continue
			flag = 3
			break
		else:
			pass

		""" step-4 """
		#print "step-4:"
		# Krawczyk 法による唯一解の判定
		krawObj = kraw.data(no, I)
		if not krawObj.KI is False:
			if solex.checkOnlySolExist(no, krawObj, x, y, method = 4) == True:
				#print I
				solI.append(I)
				#continue
				flag = 4
				break
		else:
			pass

		""" step-5 """
		#print "step-5:"
		# 区間I, K(I) が空集合であればI に解は存在しない(強い非存在判定)
		if not krawObj.KI is False:
			# the krawczyk-method
			if solex.checkNoSolExist(no, krawObj, x, y, method = 2) == True:
				#I = []
				#continue
				flag = 5
				break
		else:
			# the mean-value-form
			if solex.checkNoSolExist(no, I, x, y, method = 3) == True:
				#I = []
				#continue
				flag = 5
				break

		""" step-6 """
		#print "step-6:"
		# 区間の分割
		splitI = []
		for i in range(len(split(I))):
			#List.append(split(I)[i])
			splitI.append(split(I)[i])
		numSplit += 1
		#continue
		flag = 6
		return (no, flag, splitI)

	# 唯一解を持つ区間を返す
	# 分割回数の表示
	#print '\n\r'
	#print "The number of split-I: "+str(numSplit)
	#return solI
	return (no, flag, [I])


#def improveVerification(no, solIList):
def improveVerification(no, solI, x=None, y=None):
	""" higher numerical verification

	"""
	if x is None or y is None:
		x, y = fdFunc(no)
	# number counting improved-solI
	countImprovedSolI = 0
	# max-loop of improve soilI
	maxLoop = 100
	#if len(solIList) == 0:
	if len(solI) == 0:
		msg = 'Assigned equation has no-solution in the interval-list.'
		print "============================ END =============================="
		return msg
	#improvedSolIList = []
	#countImprovedSolI += 1
	#solI = solIList.pop(0)
	# 区間反復法
	#solIList.append(kraw.krawczyk(no, solI))
	flag = None
	if evaluateImproveVerification(solI) == True:
		flag = True
	else:
		flag = False
	return (no, flag, [kraw.krawczyk(no, solI, x, y)])
	#print "The number of improving verification: "+str(countImprovedSolI)
	#print "============================ END =============================="
	#return improvedSolIList


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
	#allowableError = 1e-7
	allowableError = 1e-1
	for i in range(len(solI)):
		# calcurate width-error of interval
		widthError = interval.width(solI.item(i))
		if widthError >= allowableError:
			return False
	return True


def convertJson(no, flag, IList):
	"""

	"""
	import json
	data = {}
	list = {}
	cnt = 0
	data['no'] = no
	data['flag'] = flag
	for I in IList:
		val = []
		for i in xrange(len(I)):
			val.append((I.item(i).inf, I.item(i).sup))
		#list.append(val)
		list[cnt] = val
		cnt = cnt + 1
	data['I'] = list
	#return json.dumps(data, indent=4)
	return json.dumps(data)




# 入力する解区間
#I = func.initI()
#print_r(improveVerification(allSolution(I)))
