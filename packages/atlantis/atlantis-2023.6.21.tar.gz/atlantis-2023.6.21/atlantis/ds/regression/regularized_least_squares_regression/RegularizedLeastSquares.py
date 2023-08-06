import pandas as pd
import numpy as np
from ._RegularizedLeastSquaresForPandas import RegularizedLeastSquaresForPandas
from ._RegularizedLeastSquaresForNumpy import RegularizedLeastSquaresForNumpy, C


class RegularizedLeastSquares:
	def __init__(self, c=C, x0=None, add_constant=False, non_negative=False):
		self._c = c
		self._x0 = x0
		self._add_constant = add_constant
		self._non_negative = non_negative
		self._model = None

	def fit(self, X, y):
		"""
		:type X: pd.DataFrame or np.ndarray
		:type y: list or np.ndarray
		"""
		if isinstance(X, pd.DataFrame):
			self._model = RegularizedLeastSquaresForPandas(
				c=self._c, x0=self._x0, add_constant=self._add_constant, non_negative=self._non_negative
			)
		else:
			self._model = RegularizedLeastSquaresForNumpy(
				c=self._c, x0=self._x0, add_constant=self._add_constant, non_negative=self._non_negative
			)

		self._model.fit(X, y)
		return self

	def predict(self, X):
		return self._model.predict(X)

	@property
	def coefficients(self):
		return self._model.coefficients

	@property
	def intercept(self):
		return self._model.intercept

	@property
	def mse(self):
		return self._model.mse
