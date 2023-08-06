import pandas as pd
from ._RegularizedLeastSquaresForNumpy import RegularizedLeastSquaresForNumpy, C


class RegularizedLeastSquaresForPandas:
	"""
	Generalized Ridge regularization with option for returning non-negative weights
	and inputting an arbitrary trial weight vector

	This version takes Pandas Dataframes as input

	inputs:
	C           regularization strength (default is near zero)
	x0          trial input weight vector (default = None)
	non_neg     bool to set non-negative constraint (default = False)
	add_const   bool to add column of 1's (default = False)

	returns:
	res         result object storing values for:
				params - fitted weights
				mse    - mean square error
				bse    - vector of std err in the weights

	typical usage:
	model = RegularizedLS(C=1)
	res = model.fit(X, y)
	"""

	def __init__(self, c=C, x0=None, add_constant=False, non_negative=False):
		self._gr_numpy = RegularizedLeastSquaresForNumpy(c=c, x0=x0, add_constant=add_constant, non_negative=non_negative)
		self._x_columns = None

	@property
	def parameters(self):
		return self._gr_numpy.parameters

	def copy(self):
		return self.__class__(
			c=self._gr_numpy._c, x0=self._gr_numpy._x0, add_constant=self._gr_numpy._add_constant,
			non_negative=self._gr_numpy._non_negative
		)

	def predict(self, X):
		"""
		:type X: pd.DataFrame
		"""
		X = X[self._x_columns]
		return self._gr_numpy.predict(X.to_numpy())

	def fit(self, X, y):
		"""
		:type X: pd.DataFrame
		:type y: pd.Series or list
		"""
		self._x_columns = list(X.columns)
		if 'intercept' in self._x_columns:
			raise ValueError('A column named "intercept" is not allowed!')
		self._gr_numpy.fit(X, y)

		return self

	@property
	def coefficients(self):
		coefficient_values = self._gr_numpy.coefficients
		if len(self._x_columns) != len(coefficient_values):
			raise RuntimeError(f'There are {len(self._x_columns)} columns but {len(coefficient_values)} coefficients!')
		result = {col: val for col, val in zip(self._x_columns, coefficient_values)}
		if self._gr_numpy._add_constant:
			result['intercept'] = self.intercept
		return result

	@property
	def intercept(self):
		return self._gr_numpy.intercept

	@property
	def mse(self):
		return self._gr_numpy.mse
