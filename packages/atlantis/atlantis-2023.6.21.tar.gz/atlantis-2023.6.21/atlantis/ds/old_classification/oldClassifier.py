from pyspark.ml.feature import VectorAssembler
from pandas import DataFrame as PandasDF
from pyspark.sql import DataFrame as SparkDF

class Classifier:
	def __init__(
			self, model_class, model_kwargs, input_variables, output_variable,
			assembler_features_column = 'asssembler_features'
	):
		self._model_class = model_class
		self._model_kwargs = model_kwargs

		self._input_variables = input_variables
		self._output_variable = output_variable
		self._assembler_placeholder = None
		self._classes = None
		self._assembler_features_column = assembler_features_column

		self._trained_model = None
		self._model_type = None

	@property
	def untrained_model(self):
		return self._model_class(**self._model_kwargs)

	@property
	def _assembler(self):
		if self._assembler_placeholder is None:
			self._assembler_placeholder = VectorAssembler(
				inputCols=self._input_variables, outputCol=self._assembler_features_column
			)
		return self._assembler_placeholder

	def _assemble(self, data):
		return self._assembler.transform(data)

	def _set_classes(self, data):
		if isinstance(data, SparkDF):
			self._classes = data.select(self._output_variable).distinct().rdd.flatMap(lambda x: x).collect()
		else:
			self._classes = list(data[self._output_variable].drop_duplicates().values)

	def fit(self, data):
		untrained_model = self.untrained_model
		if isinstance(data, SparkDF):
			data = self._assemble(data=data)
			self._trained_model = untrained_model.fit(data)
		elif isinstance(data, PandasDF):
			X = data[self._input_variables]
			y = data[self._output_variable]
			self._trained_model = untrained_model.fit(X, y)

		return self

	def transform(self, data):
		pass

	predict = transform




