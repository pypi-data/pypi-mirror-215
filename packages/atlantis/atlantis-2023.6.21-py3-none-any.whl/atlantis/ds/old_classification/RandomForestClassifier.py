from pandas import DataFrame as PandasDF
from pyspark.sql import DataFrame as PySparkDF
from ..supervised_learning import PySparkRandomForestClassifier, BaseSupervisedModel


class RandomForestClassifier(BaseSupervisedModel):
	def __init__(
			self, input_variables, output_variable, prediction_column='predicted', probability_column='probability',
			seed=42,
			**kwargs
	):
		super().__init__(
			input_variables=input_variables, output_variable=output_variable, prediction_column=prediction_column,
			probability_column=probability_column, seed=seed, **kwargs
		)

	def _fit(self, data):
		"""
		:type data: PandasDF or PySparkDF
		"""
		if isinstance(data, PandasDF):
			raise NotImplementedError('pandas model not implemented')
		elif isinstance(data, PySparkDF):
			self._untrained_model = PySparkRandomForestClassifier

