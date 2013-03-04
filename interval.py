# -*- coding: utf-8 -*-
#! path to your python
#
#
# This module is for interval arithmetic.
# And, modifying class extended arithmetic operator for it.
#
# Reccomended version of python is 2.7.x (or upper)
import math

class interval(object):
	""" 区間演算に関するクラス

	"""

	""" Attribute """
	# クラス内部で扱う数値の型チェック用
	inner_types = (float, int)

	# 区間のサイズは１とする(FuncDesigner 内で自動微分に使用)
	size = 1
	# 区間の次元は１とする(FuncDesigner 内で自動微分に使用)
	ndim = 1
	# scipy.sparse.cs(c\r)_matrix でのエラー回避
	Unsupport_scipy_sparse_cscmatrix = False
	Unsupport_scipy_sparse_csrmatrix = False


	""" Method """
	def __init__(self, *args):
		""" 初期化メソッド

		"""
		if len(args) == 0:
			self.inf = None
			self.sup = None
		elif len(args) == 1:
			self.inf = args[0]
			self.sup = args[0]
		elif len(args) == 2:
			self.inf = args[0]
			self.sup = args[1]
		else:
			raise TypeError


	def __str__(self):
		""" __str___(self)再定義

		組み込み関数str()やprint文によって呼び出される。

		"""
		#return "[" + str(self.inf) + "," + str(self.sup) + "]"
		return repr(self)


	def __repr__(self):
		""" __repr__(self)の再定義

		組み込み関数repr()や文字列のへの変換の際に呼び出される。

		"""
		return "[" + repr(self.inf) + "," + repr(self.sup) + "]"


	# 単項算術演算の多重定義
	#
	# 単項算術演算(-, +, abs() および ~) を実現するために呼び出される
	# 特殊メソッドの多重定義をします。

	def __neg__(self):
		r = interval()
		r.inf = - self.sup
		r.sup = - self.inf
		return r


	# 二項算術演算子の多重定義
	#
	# 二項算術演算 ( +, -, *, //, %, divmod(), pow(), **, «, », &, ^, |)
	# を実現するために呼び出される特殊メソッドの多重定義をします。

	def __add__(self, x):
		""" 加算

		"""
		if isinstance(x, interval):
			r = interval()
			r.inf = interval.pred(self.inf + x.inf)
			r.sup = interval.succ(self.sup + x.sup)
		elif isinstance(x, interval.inner_types):
			r = interval()
			r.inf = interval.pred(self.inf + x)
			r.sup = interval.succ(self.sup + x)
		elif isinstance(x, long):
			r = interval()
			r.inf = interval.pred(self.inf + x)
			r.sup = interval.succ(self.sup + x)
		else:
			return NotImplemented
		return r


	def __sub__(self, x):
		""" 減算

		"""
		if isinstance(x, interval):
			r = interval()
			r.inf = interval.pred(self.inf - x.sup)
			r.sup = interval.succ(self.sup - x.inf)
		elif isinstance(x, interval.inner_types):
			r = interval()
			r.inf = interval.pred(self.inf - x)
			r.sup = interval.succ(self.sup - x)
		elif isinstance(x, long):
			r = interval()
			r.inf = interval.pred(self.inf - x)
			r.sup = interval.succ(self.sup - x)
		else:
			return NotImplemented
		return r


	def __mul__(self, x):
		""" 乗算

		"""
		if isinstance(x, interval):
			r = interval()
			tmp = (self.inf * x.inf, self.inf * x.sup, self.sup * x.inf, self.sup * x.sup)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		elif isinstance(x, interval.inner_types):
			r = interval()
			tmp = (self.inf * x, self.sup * x)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		elif isinstance(x, long):
			r = interval()
			tmp = (self.inf * x, self.sup * x)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		else:
			return NotImplemented
		return r


	def __div__(self, x):
		""" 除算

		"""
		if isinstance(x, interval):
			if x.inf <= 0 and x.sup >= 0:
				raise ZeroDivisionError("division by interval which contains 0")
			r = interval()
			tmp = (self.inf / x.inf, self.inf / x.sup, self.sup / x.inf, self.sup / x.sup)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		elif isinstance(x, interval.inner_types):
			r = interval()
			tmp = (self.inf / x, self.sup / x)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		elif isinstance(x, long):
			r = interval()
			tmp = (self.inf / x, self.sup / x)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		else:
			return NotImplemented
		return r


	# 二項算術演算子の多重定義
	#
	# 二項算術演算 ( +, -, *, //, %, divmod(), pow(), **, «, », &, ^, |)
	# を実現するために呼び出される特殊メソッドの多重定義をします。
	# ただし、メソッド呼び出しが行われる被演算子が逆転しています。


	def __radd__(self, x):
		""" 加算

		"""
		if isinstance(x, interval.inner_types):
			r = interval()
			r.inf = interval.pred(x + self.inf)
			r.sup = interval.succ(x + self.sup)
		else:
			return NotImplemented
		return r


	def __rsub__(self, x):
		""" 減算

		"""
		if isinstance(x, interval.inner_types):
			r = interval()
			r.inf = interval.pred(x - self.sup)
			r.sup = interval.succ(x - self.inf)
		else:
			return NotImplemented
		return r


	def __rmul__(self, x):
		""" 乗算

		"""
		if isinstance(x, interval.inner_types):
			r = interval()
			tmp = (x * self.inf, x * self.sup)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		else:
			return NotImplemented
		return r


	def __rdiv__(self, x):
		""" 除算

		"""
		if isinstance(x, interval.inner_types):
			if self.inf <= 0 and self.sup >= 0:
				raise ZeroDivisionError("division by interval which contains 0")
			r = interval()
			tmp = (x / self.inf, x / self.sup)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		else:
			return NotImplemented
		return r


	def __len__(self):
		""" return length of interval-obj when called from len()

		"""
		return 1


	# 除算演算に関する追加
	#
	# __future__.division が有効である場合に使用される。

	__truediv__ = __div__
	__rtruediv__ = __rdiv__


	# 数学関数の追加
	#
	# 区間演算用の数学関数を定義

	def sqrt(self):
		""" 区間の平方根

		"""
		if self.inf < 0:
			raise ValueError("sqrt of negative interval")
		r = interval()
		r.inf = interval.pred(math.sqrt(self.inf))
		r.sup = interval.succ(math.sqrt(self.sup))
		return r


	@staticmethod
	def subset(x, y):
		""" ある区間との包含関係

		xが区間yに含まれるときに True

		"""
		if isinstance(y, interval):
			if (isinstance(x, interval)):
				return x.inf >=  y.inf and x.sup <= y.sup
			else:
				return x >=  y.inf and x <= y.sup
		else:
			raise ValueError


	@staticmethod
	def overlap(x, y):
		""" 

		"""
		if isinstance(x, interval):
			xinf = x.inf
			xsup = x.sup
		else:
			xinf = x
			xsup = x
		if isinstance(y, interval):
			yinf = y.inf
			ysup = y.sup
		else:
			yinf = y
			ysup = y
		return max(xinf, yinf) <= min(xsup, ysup)


	@staticmethod
	def isemptyset(x, y):
		""" whether empty set

		"""
		if isinstance(x, interval):
			if isinstance(y, interval):
				xinf = x.inf
				xsup = x.sup
				yinf = y.inf
				ysup = y.sup
				return xsup < yinf or ysup < xinf
		raise ValueError


	@staticmethod
	def issubset(x, y):
		""" whether subset

		"""
		if isinstance(x, interval):
			if isinstance(y, interval):
				xinf = x.inf
				xsup = x.sup
				yinf = y.inf
				ysup = y.sup
				return (xinf < yinf and yinf <= xsup and xsup < ysup) or (yinf < xinf and xinf <= ysup and ysup < xsup)
		raise ValueError


	@staticmethod
	def issuperset(x, y):
		""" whether superset

		"""
		if isinstance(x, interval):
			if isinstance(y, interval):
				xinf = x.inf
				xsup = x.sup
				yinf = y.inf
				ysup = y.sup
				return (xinf <= yinf and ysup <= xsup) or (yinf <= xinf and xsup <= ysup)
		raise ValueError


	@staticmethod
	def shape(self):
		""" return shaoe of interval-obj

		any interval-obj is defined 1*1
		ref: numpy.shape(matrix)

		"""
		if isinstance(self, interval):
			return (1, 1)
		else:
			raise TypeError


	#@staticmethod
	def item(self):
		""" return self-interval-obj

		ref: numpy.item(matrix)

		"""
		return interval(self.inf, self.sup)


	@staticmethod
	def abs(x):
		""" 区間の絶対値

		"""
		if not isinstance(x, interval):
			return abs(x)
		return max(abs(x.inf), abs(x.sup))


	@staticmethod
	def norm(x):
		""" ノルム

		"""
		# これだと間違い？予約abs()を呼び出してしまう？
		#return abs(x)
		return interval.abs(x)


	@staticmethod
	def mag(x):
		""" 絶対値

		"""
		return abs(x)


	@staticmethod
	def mig(x):
		""" 

		"""
		if not isinstance(x, interval):
			return abs(x)
		else:
			if x.inf <=0 and x.sup >=0:
				return 0
			else:
				return min(abs(x.inf), abs(x.sup))


	@staticmethod
	def mid(x):
		""" 区間の中間値

		"""
		if isinstance(x, interval):
			return (x.inf + x.sup) / 2
		else:
			return x


	@staticmethod
	def width(x):
		""" 区間幅

		"""
		if isinstance(x, interval):
			return interval.succ(x.sup - x.inf)
		else:
			return 0


	@staticmethod
	def rad(x):
		""" 区間の中間座標（丸めなし）

		"""
		if isinstance(x, interval):
			return (x.inf + x.sup) / 2
		else:
			return x


	@staticmethod
	def medsucc(x):
		""" 区間の中間座標（上方向丸め）

		"""
		if isinstance(x, interval):
			return interval.succ((x.sup + x.inf) / 2)
		else:
			return x


	@staticmethod
	def medpred(x):
		""" 区間の中間座標（下方向丸め）

		"""
		if isinstance(x, interval):
			return interval.pred((x.sup + x.inf) / 2)
		else:
			return x


	@staticmethod
	def succ(x):
		""" 区間丸め誤差

		上方向丸めの場合

		"""
		a = abs(x)
		if a >= 2**(-1022):
			return x + a * (2.**(-53)+2.**(-55))
		else:
			return x + 2.**(-1074)


	@staticmethod
	def pred(x):
		""" 区間丸め誤差

		下方向丸め

		"""
		a = abs(x)
		if a >= 2**(-1022):
			return x - a * (2.**(-53)+2.**(-55))
		else:
			return x - 2.**(-1074)


	# 数学関数のオーバーライド
	#
	# 区間演算用に定義
	# math_interval 等で呼び出される


	def float(self):
		""" convert inner-type to 'float'

		usage:
		>>> int1 = interval(-1, 1)
		>>> interval.float(int1)
		or
		>>> int1.float()

		"""
		from numpy import float as npfloat
		if isinstance(self, interval):
			self.inf = self.inf*1.
			self.sup = self.sup*1.
		else:
			return npfloat(self)
		return interval(self.inf, self.sup)


	def __asfarray__(self):
		""" override method-asfarray of numpy for interval

		return interval-instance as overwrapped by numpy.ndarray

		"""
		from numpy import array
		if isinstance(self, interval):
			return array(interval.float(self))
		else:
			raise TypeError('Input value is not interval-instance')


	def __isscalar__(self):
		""" extend numpy.isscalar for interval

		interval class is as scalar (return True).

		"""
		if isinstance(self, interval):
			return True
		else:
			return np.isscalar(self)


	def toarray(self):
		""" return self

		for FuncDesigner

		"""
		return self


	def __sin__(self):
		""" sine function for interval

		"""
		if not isinstance(self, interval):
			raise TypeError('Invalid type of object')
		else:
			# init
			width = interval.width(self)
			tmp = interval()
			loop = 100
			if self.inf < -loop*(math.pi) or loop*(math.pi) < self.sup:
				raise ValueError('Exceed dealing of interval-value')
			if width >= 2.*(math.pi):
				""" 1. """
				(tmp.inf, tmp.sup) = (-1., 1.)
			else:
				""" 2. """
				for n in range(-loop, loop):
					# self include extreme value of 1 and -1
					if (self.inf <= (2*n - 1)*(math.pi)/2.) and ((2*n + 1)*(math.pi)/2. <= self.sup):
						(tmp.inf, tmp.sup) = (-1., 1.)
						break
				else:
					for n in range(-loop, loop):
						# self include extreme value of 1 only
						if self.inf <= (4*n - 3)*(math.pi)/2. <= self.sup:
							(tmp.inf, tmp.sup) = (min(math.sin(self.inf), math.sin(self.sup)), 1.)
							break
						# self include extreme value of -1 only
						if self.inf <= (4*n - 1)*(math.pi)/2. <= self.sup:
							(tmp.inf, tmp.sup) = (-1., max(math.sin(self.inf), math.sin(self.sup)))
							break
					else:
						# self not include extreme value
						(tmp.inf, tmp.sup) = (min(math.sin(self.inf), math.sin(self.sup)), max(math.sin(self.inf), math.sin(self.sup)))
			if tmp.inf == None or tmp.sup == None:
				raise ValueError('Not decide value of sine')
			""" spreading width of interval """
			if not (tmp.inf == 1. or tmp.inf == -1.):
				tmp.inf = interval.pred(tmp.inf)
			if not (tmp.sup == 1. or tmp.sup == -1):
				tmp.sup = interval.succ(tmp.sup)
			return interval(tmp.inf, tmp.sup)


	def __cos__(self):
		""" cosine function for interval

		"""
		if not isinstance(self, interval):
			raise TypeError('Invalid type of object')
		else:
			# init
			width = interval.width(self)
			tmp = interval()
			loop = 100
			if self.inf < -loop*(math.pi) or loop*(math.pi) < self.sup:
				raise ValueError('Exceed dealing of interval-value')
			if width >= 2.*(math.pi):
				""" 1. """
				(tmp.inf, tmp.sup) = (-1., 1.)
			else:
				""" 2. """
				for n in range(-loop, loop):
					# self include extreme value of 1 and -1
					if (self.inf <= n*(math.pi)) and ((n + 1)*(math.pi) <= self.sup):
						(tmp.inf, tmp.sup) = (-1., 1.)
						break
				else:
					for n in range(-loop, loop):
						# self include extreme value of 1 only
						if self.inf <= 2*n*(math.pi) <= self.sup:
							(tmp.inf, tmp.sup) = (min(math.cos(self.inf), math.cos(self.sup)), 1.)
							break
						# self include extreme value of -1 only
						if self.inf <= (2*n + 1)*(math.pi) <= self.sup:
							(tmp.inf, tmp.sup) = (-1., max(math.cos(self.inf), math.cos(self.sup)))
							break
					else:
						# self not include extreme value
						(tmp.inf, tmp.sup) = (min(math.cos(self.inf), math.cos(self.sup)), max(math.cos(self.inf), math.cos(self.sup)))
			if tmp.inf == None or tmp.sup == None:
				raise ValueError('Not decide value of cosine')
			""" spreading width of interval """
			if not (tmp.inf == 1. or tmp.inf == -1.):
				tmp.inf = interval.pred(tmp.inf)
			if not (tmp.sup == 1. or tmp.sup == -1):
				tmp.sup = interval.succ(tmp.sup)
			return interval(tmp.inf, tmp.sup)


	def __pow__(x, y):
		""" 冪乗

		y: 正の整数のみ対応

		"""
		if isinstance(x, interval):
			if y == 0:
				if x.inf == 0 or x.sup == 0:
					raise ValueError('invalid value of 0 power to 0')
				return interval(1., 1.)
			elif y == 1:
				return x
			elif y > 1:
				if y % 2 == 0:
					r = interval()
					tmp = interval(1., 1.)
					r.inf = min(interval.abs(x.inf), interval.abs(x.sup))
					r.sup = max(interval.abs(x.inf), interval.abs(x.sup))
					for i in range(int(y)):
						tmp.inf = tmp.inf * r.inf
						tmp.sup = tmp.sup * r.sup
					if x.inf >= 0 or x.sup <= 0:
						return interval(min(tmp.inf, tmp.sup), max(tmp.inf, tmp.sup))
					else:
						return interval(0., max(tmp.inf, tmp.sup))
				elif y % 2 == 1:
					r = interval()
					tmp = interval(1., 1.)
					r.inf = min(x.inf, x.sup)
					r.sup = max(x.inf, x.sup)
					for i in range(int(y)):
						tmp.inf = tmp.inf * r.inf
						tmp.sup = tmp.sup * r.sup
					return interval(min(tmp.inf, tmp.sup), max(tmp.inf, tmp.sup))
				else:
					raise ValueError('unknown value')
			else:
				raise ValueError('Not yet')
		else:
			return pow(x, y)



	########## False method ###########
	def __cos_bac__(self):
		""" cosine function for interval

		"""
		if isinstance(self, interval):
			width = interval.width(self)
			tmp = interval()
			loop = 100
			if self.inf >= 0.:
				""" 1. """
				if width >= 2.*(math.pi):
					# 1.1
					tmp.inf = -1.
					tmp.sup = 1.
				elif math.pi <= width < 2.*(math.pi):
					# 1.2
					for n in range(1, loop):
						if self.inf <= n*(math.pi) and (n + 1)*(math.pi) <= self.sup:
							# 1.2.1
							tmp.inf = -1.
							tmp.sup = 1.
							break
						elif self.inf < (2*n - 1)*(math.pi) < self.sup:
							# 1.2.2
							tmp.inf = -1.
							tmp.sup = max(math.cos(self.inf), math.cos(self.sup))
							break
						elif self.inf < n*(math.pi) < self.sup:
							# 1.2.3
							tmp.inf = min(math.cos(self.inf), math.cos(self.sup))
							tmp.sup = 1.
							break
					else:
						# 1.2.0
						raise ValueError('Could not decide value of cosine: 1.2.0')
				elif 0. <= width < math.pi:
					# 1.3
					for n in range(1, loop):
						if self.inf < (2*n - 1)*(math.pi) < self.sup:
							# 1.3.1
							tmp.inf = -1.
							tmp.sup = max(math.cos(self.inf), math.cos(self.sup))
							break
						elif self.inf < n*(math.pi) < self.sup:
							# 1.3.2
							tmp.inf = min(math.cos(self.inf), math.cos(self.sup))
							tmp.sup = 1.
							break
						elif (n - 1)*(math.pi) <= self.inf and self.sup <= n*(math.pi):
							# 1.3.3
							tmp.inf = min(math.cos(self.inf), math.cos(self.sup))
							tmp.sup = max(math.cos(self.inf), math.cos(self.sup))
							break
					else:
						# 1.3.0
						raise ValueError('Could not decide value of cosine: 1.3.0')
			elif self.sup <= 0.:
				""" 2. """
				if width >= 2.*(math.pi):
					# 2.1
					tmp.inf = -1.
					tmp.sup = 1.
				elif math.pi <= width < 2.*(math.pi):
					# 2.2
					for n in range(1, loop):
						if self.inf <= -(n + 1)*(math.pi) and (-n)*(math.pi) <= self.sup:
							# 2.2.1
							tmp.inf = -1.
							tmp.sup = 1.
							break
						elif self.inf < -(2*n - 1)*(math.pi) < self.sup:
							# 2.2.2
							tmp.inf = -1.
							tmp.sup = max(math.cos(self.inf), math.cos(self.sup))
							break
						elif self.inf < (-n)*(math.pi) < self.sup:
							# 2.2.3
							tmp.inf = min(math.cos(self.inf), math.cos(self.sup))
							tmp.sup = 1.
							break
					else:
						# 2.2.0
						raise ValueError('Could not decide value of cosine: 2.2.0')
				elif 0. <= width < math.pi:
					# 2.3
					for n in range(1, loop):
						if self.inf < -(2*n - 1)*(math.pi) < self.sup:
							# 2.3.1
							tmp.inf = -1.
							tmp.sup = max(math.cos(self.inf), math.cos(self.sup))
							break
						elif self.inf < (-n)*(math.pi) < self.sup:
							# 2.3.2
							tmp.inf = min(math.cos(self.inf), math.cos(self.sup))
							tmp.sup = 1.
							break
						elif (-n)*(math.pi) <= self.inf and self.sup <= (-n + 1)*(math.pi):
							# 2.3.3
							tmp.inf = min(math.cos(self.inf), math.cos(self.sup))
							tmp.sup = max(math.cos(self.inf), math.cos(self.sup))
							break
					else:
						# 2.3.0
						raise ValueError('Could not decide value of cosine: 2.3.0')
			elif self.inf < 0. < self.sup:
				""" 3. """
				if width >= 2.*(math.pi):
					# 3.1
					tmp.inf = -1.
					tmp.sup = 1.
				elif 0. < width < 2.*(math.pi):
					# 3.2
					tmp.inf = min(math.cos(self.inf), math.cos(self.sup))
					tmp.sup = 1.
				else:
					# 3.0
					raise ValueError('Could not decide value of cosine: 3.0')
			else:
				# 0.
				raise ValueError('Could not decide value of cosine: 0.')
			""" spreading width of interval """
			if not (tmp.inf == 1. or tmp.inf == -1.):
				tmp.inf = interval.pred(tmp.inf)
			if not (tmp.sup == 1. or tmp.sup == -1.):
				tmp.sup = interval.succ(tmp.sup)
			return interval(tmp.inf, tmp.sup)
		else:
			raise TypeError('Invalid type of object')
