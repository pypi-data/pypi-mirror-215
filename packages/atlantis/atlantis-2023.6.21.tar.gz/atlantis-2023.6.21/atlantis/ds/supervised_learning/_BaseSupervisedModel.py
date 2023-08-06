ALIASES = {
	'input_variables': ['features', 'feature_columns', 'x_columns', 'independent_variables'],
	'output_variable': ['label_column', 'y_column', 'class_column', 'dependent_variable'],
	'prediction_column': [],
	'probability_column': []
}

TYPES = {
	'features': list,
	'label_column': str,
	'prediction_column': str,
	'probability_column': str
}


class BaseSupervisedModel:
	def __init__(self, input_variables, output_variable, prediction_column, probability_column, **kwargs):
		self._inital_kwargs = {
			'input_variables': input_variables, 'output_variable': output_variable,
			'prediction_column': prediction_column, 'probability_column': probability_column,
			**kwargs
		}

		self._untrained_model = None
		self._trained_model = None
		self._performance = None
		self._feature_importances = None
		self._initialize()

	def _initialize(self):
		for key, value in self._inital_kwargs.items():
			if key in TYPES:
				the_type = TYPES[key]

				if the_type is list and isinstance(value, str):
					value = [value]

				# noinspection PyTypeHints
				if not isinstance(value, the_type):
					raise TypeError(f'{key} should be of type {the_type.__name__}')

			setattr(self, f'_{key}', value)

	@property
	def input_variables(self):
		"""
		:rtype: list[str]
		"""
		return self._input_variables

	@property
	def output_variable(self):
		"""
		:rtype: str
		"""
		return self._output_variable

	@property
	def prediction_column(self):
		"""
		:rtype: str
		"""
		return self._prediction_column

	@property
	def X(self):
		raise RuntimeError('X is not implemented')

	@property
	def y(self):
		raise RuntimeError('y is not implemented')

	def _fit(self, data):
		raise NotImplementedError('fit is not implemented')

	def fit(self, data):
		if self._trained_model is not None:
			raise RuntimeError('model is already trained')
		return self._fit(data=data)

	def _predict(self, data):
		raise NotImplementedError('predict is not implemented')

	def predict(self, data):
		if self._trained_model is None:
			raise RuntimeError('model is not trained')
		return self._predict(data=data)

	def _transform(self, data):
		raise NotImplementedError('transform is not implemented!')

	def transform(self, data):
		if self._trained_model is None:
			raise RuntimeError('model is not trained')
		return self._transform(data=data)

	def fit_transform(self, data):
		self.fit(data=data)
		return self.transform(data=data)

	@property
	def performance(self):
		"""
		:rtype: pd.DataFrame
		"""
		return self._performance

	@property
	def feature_importances(self):
		"""
		:rtype: dict[str, float]
		"""
		return self._feature_importances
