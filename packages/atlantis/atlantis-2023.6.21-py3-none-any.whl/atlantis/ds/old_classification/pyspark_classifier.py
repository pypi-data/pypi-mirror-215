from pyspark.ml.classification import RandomForestClassifier, RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.types import ArrayType, FloatType
from pyspark.ml.linalg import DenseVector
from pyspark.sql import functions as f
from pyspark.sql import DataFrame as SparkDataFrame
import pandas as pd


class Classifier:
	def __init__(
			self, label_column,
			prediction_column='predicted', features_column='features',
			probability_column='probability',
			columns=None, classifier='random_forest', classifier_parameters=None, balanced=False,
			seed=42
	):
		self._balanced = balanced
		if self._balanced:
			self._weight_column = 'class_weight'
		else:
			self._weight_column = None

		self._label_column = label_column
		self._prediction_column = prediction_column
		self._features_column = features_column
		self._probability_column = probability_column

		self._classifier_type = classifier
		self._classifier_parameters = classifier_parameters or {}
		self._seed = seed

		if classifier is None:
			classifier = RandomForestClassifier(
				labelCol=self._label_column, weightCol=self._weight_column,
				featuresCol=self._features_column, predictionCol=self._prediction_column,
				probabilityCol=self._probability_column,
				seed=self._seed,
				**self._classifier_parameters
			)

		self._untrained_classifier = classifier
		self._trained_classifier = None
		self._performance = None
		self._feature_importances = None
		self._columns = columns

		self._assembler = VectorAssembler(inputCols=self._columns, outputCol='features')
		self._dense = False

		self._regressors = {}
		self._regressors_performances = {}
		self._coefficients = None
		self._regressors_evaluations = {}
		self._stop_training = False
		self._coefficients_data = None

	def _transform(self, data):
		"""
		:type data: SparkDataFrame
		:rtype: SparkDataFrame
		"""
		@f.udf(ArrayType(FloatType()))
		def to_dense(v):
			v = DenseVector(v)
			new_array = list([float(x) for x in v])

			return new_array

		transformed_data = self._assembler.transform(data)
		if self._dense:
			transformed_data = transformed_data.withColumn('features', to_dense('features'))
		return transformed_data

	def fit(self, data):
		transformed_data = self._transform(data=data)
		self._trained_classifier = self.untrained_classifier.fit(dataset=transformed_data)

	@property
	def untrained_classifier(self):
		return self._untrained_classifier

	@property
	def trained_classifier(self):
		if self._trained_classifier is None:
			raise RuntimeError('classifier is not fit yet!')
		return self._trained_classifier

	def predict(self, data, label):
		"""
		:type data: SparkDataFrame
		:rtype: SparkDataFrame
		"""
		transformed_data = self._transform(data=data.fillna(0))
		result = self.trained_classifier.transform(transformed_data)

		if self._label_column in result.columns:
			self.measure_performance(data=result, label=label)

		return result

	def measure_performance(self, data, label):
		result = data.select(f.col(self._label_column).alias('actual'), self._prediction_column).groupby(
			'actual', 'predicted'
		).agg(f.count(f.lit(1)).alias('count')).toPandas()

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
		self._performance = {
			'label': label,
			'true_negative': true_negative, 'false_positive': false_positive, 'false_negative': false_negative,
			'true_positive': true_positive, 'precision': precision, 'recall': recall
		}
		return self._performance

	@property
	def performance(self):
		"""
		:rtype: dict[str, float]
		"""
		if self._performance is None:
			raise RuntimeError('no performance!')
		return self._performance

	def _add_probability_column(self, data, index=0):
		"""
		:type data: SparkDataFrame
		:rtype: SparkDataFrame
		"""
		@f.udf(FloatType())
		def _get_probability_of_1(v):
			try:
				return 1 - float(v[index])
			except:
				return None

		return data.withColumn(
			f'{self._probability_column}_{index}',
			_get_probability_of_1(self._probability_column)
		)

	@property
	def feature_importances(self):
		"""
		:rtype: dict[str, float]
		"""
		if self._feature_importances is None:
			feature_importances = list(self.trained_classifier.featureImportances.toArray())
			self._feature_importances = {
				column: importance for column, importance in zip(self._columns, feature_importances)
			}
		return self._feature_importances

	@property
	def feature_importances_data(self):
		"""
		:rtype: pd.DataFrame
		"""
		df = pd.DataFrame(self.feature_importances.items(), columns=['feature', 'importance']).sort_values(
			by='importance', ascending=False
		)
		suffixes = ['_zscore', '_value', '_count']
		prefixes = ['mean_', 'max_']

		def _get_aggregate_type(x):
			if x.endswith('_count'):
				return 'count'
			elif x.startswith('mean_'):
				return 'mean'
			elif x.startswith('max_'):
				return 'max'
			else:
				return 'none'

		def _get_measurement_type(x):
			if x.endswith('_count'):
				return 'count'
			elif x.endswith('_zscore'):
				return 'zscore'
			elif x.endswith('_value'):
				return 'value'
			else:
				return 'unknown'

		def _get_measurement(x):
			for suffix in suffixes:
				if x.endswith(suffix):
					x = x[:-len(suffix)]
					break
			for prefix in prefixes:
				if x.startswith(prefix):
					x = x[len(prefix):]
					break
			return x

		df['aggregate_type'] = df['feature'].apply(_get_aggregate_type)
		df['measurement_type'] = df['feature'].apply(_get_measurement_type)
		df['measurement'] = df['feature'].apply(_get_measurement)
		return df
