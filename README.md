intervalpy
==========

Python による区間演算を用いた精度保証付き数値計算を実現する.

1. 要件:
  1-1. 必須：
		Python-2.7 (recommend: GCC-4.4.6 build)
		numpy-1.6.2 (or later)
		scipy-0.10.1 (or later)
		FuncDesigner-0.43
	
  1-2. 推奨:
		ARPACK
		BLAS
		ATLAS
		LAPACK

2. 機能群
  2-1. 区間演算
		interval.py
  2-2. Krawczyk法
		krawczyk.py
  2-3. 全解探索
		all_solution.py

3. パッチ
  3-1. FuncDesigner
		区間演算用に拡張した. ライブラリ導入後にファイルを差し替えれば良い.
