import numpy as np


def _check_matrix_input(*args):
	if len(args) == 1:
		arg = args[0]
		if isinstance(arg, np.ndarray):
			if len(arg.shape) == 2:
				return arg.tolist()
			else:
				raise TypeError(f'{len(arg.shape)}-dimensional numpy array is not a matrix!')
		elif isinstance(arg, (list, tuple)):
			if all([isinstance(e, (list, tuple)) for e in arg]):
				return arg
			else:
				raise TypeError(f'Elements of the argument are not lists or tuples!')
		else:
			raise TypeError(f'Object of type {type(arg)} is not supported!')
	else:
		return _check_matrix_input(args)


class Matrix:
	def __init__(self, *args):
		self._rows = _check_matrix_input(*args)
		self._n_rows = len(self._rows)
		self._n_columns = len(self._rows[0])
		assert all([len(row) == self._n_columns for row in self.rows]), "Rows do not have the same length!"
		self._columns = None

	@property
	def rows(self):
		return self._rows

	@property
	def columns(self):
		if self._columns is None:
			columns = [[] for e in self.rows[0]]
			for row in self.rows:
				for i, element in enumerate(row):
					columns[i].append(element)
			self._columns = columns
		return self._columns

	@staticmethod
	def multiply_elements(x, y):
		if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
			return np.matmul(x, y)
		else:
			return x * y

	def __add__(self, other):
		if not isinstance(other, Matrix):
			raise TypeError(f'Adding an object of type {type(other)} to a Matrix is not supported!')
		rows = []
		for row1, row2 in zip(self.rows, other.rows):
			row = [x1 + x2 for x1, x2 in zip(row1, row2)]
			rows.append(row)
		return Matrix(rows)

	def __sub__(self, other):
		if not isinstance(other, Matrix):
			raise TypeError(f'Subtracting an object of type {type(other)} from a Matrix is not supported!')
		rows = []
		for row1, row2 in zip(self.rows, other.rows):
			row = [x1 - x2 for x1, x2 in zip(row1, row2)]
			rows.append(row)
		return Matrix(rows)

	def __neg__(self):
		return Matrix([[-x for x in row] for row in self.rows])

	def __mul__(self, other):
		if not isinstance(other, Matrix):
			raise TypeError(f'Multiplying a Matrix by an object of type {type(other)} is not supported!')
		rows = []
		for row in self.rows:
			new_row = []
			for column in other.columns:
				element = sum([self.multiply_elements(e1, e2) for e1, e2 in zip(row, column)])
				new_row.append(element)
			rows.append(new_row)
		return Matrix(rows)

	def __repr__(self):
		return repr(self.rows)
