from pyspark.ml.feature import VectorAssembler
from pyspark.sql import DataFrame
from pyspark.sql import functions as f
import pandas as pd
from ._BaseSupervisedModel import BaseSupervisedModel


class PySparkModel(BaseSupervisedModel):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._assembler = VectorAssembler(inputCols=self.input_variables, outputCol='assembler_features')

	def _fit(self, data):
		transformed_data = self._assembler.transform(data)
		self._trained_model = self._untrained_model.fit(transformed_data)
		raw_feature_importances = list(self._trained_model.featureImportances.toArray())
		self._feature_importances = {
			feature: importance for feature, importance in zip(self.input_variables, raw_feature_importances)
		}

		return self

class PySparkClassifier(PySparkModel):
	@property
	def probability_column(self):
		"""
		:rtype: str
		"""
		return self._probability_column

	def _fit(self, data):
		"""
		:type data: DataFrame
		"""
		self._classes = data.select(self.output_variable).distinct().rdd.flatMap(lambda x: x).collect()
		return super()._fit(data=data)

	def _predict(self, data):
		"""
		:type data: DataFrame
		:rtype: DataFrame
		"""
		transformed_data = self._assembler.transform(data)
		prediction_data = self._trained_model.transform(transformed_data)
		if self.output_variable in prediction_data.columns:
			self.measure_performance(data=prediction_data)
		return prediction_data

	def _measure_performance_of_counts(self, data, label):
		"""
		:type data: pd.DataFrame
		"""
		result = data.copy()
		result['actual'] = (result['actual'] == label).astype('int')
		result['predicted'] = (result['predicted'] == label).astype('int')

		dictionary = result[['actual', 'predicted', 'count']].set_index(
			['actual', 'predicted']
		).to_dict()['count']
		true_positive = dictionary[(1, 1)]
		true_negative = dictionary[(0, 0)]
		false_positive = dictionary[(0, 1)]
		false_negative = dictionary[(1, 0)]
		precision = true_positive / (true_positive + false_positive)
		recall = true_positive / (true_positive + false_negative)
		return {
			'label': label,
			'true_negative': true_negative, 'false_positive': false_positive, 'false_negative': false_negative,
			'true_positive': true_positive, 'precision': precision, 'recall': recall
		}

	def measure_performance(self, data):
		"""
		:type data: pd.DataFrame
		"""
		result = data.select(
			f.col(self.output_variable).alias('actual'), f.col(self.prediction_column).alias('predicted')
		).groupby('actual', 'predicted').agg(
			f.count(f.lit(1).alias('count'))
		).toPandas()

		self._performance = pd.DataFrame.from_records(
			[self._measure_performance_of_counts(data=result, label=label) for label in self._classes]
		)
		return result
