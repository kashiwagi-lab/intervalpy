# -*- coding: utf-8 -*-
#! path to your python

######################################################################
#
# Benchmark for all-solution.
#	- calcurate time
#	- calcurate memory of cpu
#
######################################################################

# import modules
import all_solution as allsol
from interval import *
import fdFunc as func
import time
from print_r import print_r
import resource as rc


######################################################################
#
# Initialize function.
#
######################################################################

def fdFunc(no):
	""" define target function from fdFunc-module

	"""
	funcObj = func.fdFunc(no)
	x = funcObj.x
	y = funcObj.getFunc()
	return x, y



######################################################################
#
# Calculate time executing all-solution.
#
######################################################################

def executeTime(no, I = None, loop = 1):
	""" execute calcurating time of all-solution

	"""
	x, y = fdFunc(no)
	if I == None:
		funcObj = func.fdFunc(no)
		I = funcObj.initI()
	time_str = time.time()
	for i in range(loop):
		solI = allsol.improveVerification(no, allsol.allSolution(no, I, x, y), x, y)
	time_end = time.time()
	printTime(I, solI, calcurateTime(time_str, time_end))


def calcurateTime(time_str, time_end):
	""" calcurate time

	"""
	return (time_end - time_str)


def printTime(I, solI, time):
	""" print time and result

	"""
	print '--------------------------------------------------'
	print 'Input: '
	print I
	print 'Output: '
	print_r(solI)
	print '--------------------------------------------------'
	print 'Time:', time, 'sec'


######################################################################
#
# Calculate all resource-usage of executing all-solution.
#
######################################################################

def executeRUsage(no, I = None, loop = 1):
	""" execute calcurating all resource-usage of all-solution

	"""
	x, y = fdFunc(no)
	if I == None:
		funcObj = func.fdFunc(no)
		I = funcObj.initI()
	str = time.time()
	for i in range(loop):
		solI = allsol.improveVerification(no, allsol.allSolution(no, I, x, y), x, y)
	end = time.time()
	rUsage= rc.getrusage(rc.RUSAGE_SELF)
	pageSize = rc.getpagesize()
	printRUsage(no, I, solI, rUsage, pageSize)
	return (I, solI, (end-str), rUsage)


def printRUsage(no, I, solI, rUsage, pageSize):
	""" print all resource-usage and result

	"""
	print '--------------------------------------------------'
	print 'Input: '
	print I
	print 'Output: '
	if solI is None:
		print solI
	else:
		print_r(solI)
	print '--------------------------------------------------'
	print 'All resource-usage: '
	print_r(rUsage)
	print 'Page-size: '
	print pageSize
	print 'Max-usage memory size of RAM [MB]: '
	#print float(((rUsage[2]*pageSize)/1024.)/1024.)
	print float((rUsage[2]/1024.)/1024.)
	#proveSolution(no, solI)


######################################################################
#
# Prove solutions returned all-solution.
#
######################################################################

def proveSolution(no, solI):
	""" prove solutions returned all-solution

	"""
	import sol_existence as solex
	for i in xrange(len(solI)):
		print solex.fdFuncIntervalVal(no, solI.pop(0))




funcNo = 13
#executeTime(funcNo)
calctime = executeRUsage(funcNo)[2]
print "//////////////////////////////////////////////"
print "Time: ", calctime, " sec."
