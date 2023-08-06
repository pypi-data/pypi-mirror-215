import numpy as np
from scipy.optimize import nnls
C = 1e-10


class RegularizedLeastSquaresForNumpy:
	"""
	Generalized Ridge regularization with option for returning non-negative weights
	and inputting an arbitrary trial weight vector

	This version takes numpy arrays as input

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
	res = model.fit(A, y)
	"""

	def __init__(self, c=C, x0=None, add_constant=False, non_negative=False):
		self._c = c
		self._x0 = x0
		self._add_constant = add_constant
		self._non_negative = non_negative
		self._x = None
		self._mse = None
		self._mse2 = None
		self._bse = None
		assert isinstance(x0, np.ndarray) or x0 is None, 'x0 is invalid type. Must be list or ndarray.'

	@property
	def parameters(self):
		return {
			'c': self._c, 'x0': self._x0, 'add_constant': self._add_constant,
			'non_negative': self._non_negative, 'x': self._x, 'mse': self._mse,
			'bse': self._bse
		}

	def copy(self):
		return self.__class__(c=self._c, x0=self._x0, add_constant=self._add_constant, non_negative=self._non_negative)

	@property
	def coefficients(self):
		x_list = list(self._x.flatten())
		if self._add_constant:
			x_list = x_list[1:]
		return x_list

	@property
	def intercept(self):
		if self._add_constant:
			return self._x[0]
		else:
			return 0

	@property
	def mse(self):
		return self._mse

	def predict(self, A):
		"""
		:type A: np.ndarray
		"""
		if self._add_constant:
			A = np.hstack((np.ones(A.shape[0]).reshape(-1, 1), A))
		return np.matmul(A, self._x)

	def fit(self, A, y):
		if not isinstance(y, np.ndarray):
			try:
				y = y.to_numpy()
			except AttributeError:
				y = np.array(y)

		if not isinstance(A, np.ndarray):
			try:
				A = A.to_numpy()
			except AttributeError:
				A = np.array(A)

		if self._add_constant is True:
			A = np.hstack((np.ones(A.shape[0]).reshape(-1, 1), A))

		nrows, self.n_columns = A.shape

		if self._x0 is None:
			x0 = np.zeros((self.n_columns, 1))
		else:
			x0 = np.array(self._x0).reshape(-1, 1)

		## build augmented A matrix
		A_augmented = np.vstack((A, self._c * np.eye(self.n_columns)))

		## build augmented y vector
		y_augmented = np.vstack((y.reshape(nrows, 1), self._c * x0))

		## build covariance matrix and its inverse (using augmented A matrix)
		ATA_augmented = np.matmul(A_augmented.transpose(), A_augmented)
		ATA_augmented_inverse = np.linalg.inv(ATA_augmented)

		if self._non_negative is True:
			self._x, err = nnls(A_augmented, y_augmented.reshape(-1, ))
			self._mse = err / np.sqrt(len(y))

		else:
			self._x = np.matmul(ATA_augmented_inverse, np.matmul(A_augmented.transpose(), y_augmented)).flatten()

			## calculate mean square error
			yf = np.matmul(A, self._x)
			self.yf = yf
			self._mse = np.sqrt(((y.reshape(-1, 1) - yf) ** 2).sum() / y.shape[0])

		yf = np.matmul(A, self._x)
		self._mse2 = np.sqrt(((y.flatten() - yf.flatten()) ** 2).sum() / yf.shape[0])

		## calculate mean square error for params
		self._bse = self._mse * np.sqrt(ATA_augmented_inverse.diagonal())

		return self