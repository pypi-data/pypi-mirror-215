from func_timeout import func_timeout, FunctionTimedOut

from pandas import DataFrame as PandasDF, Series as PandasSeries, concat
from sklearn.cluster import KMeans as SklearnKMeans
from sklearn.metrics import silhouette_score

from pyspark.sql import functions as f
from pyspark.sql.types import DoubleType, StringType
from pyspark.sql import DataFrame as SparkDF, Column as SparkColumn
from pyspark.ml.clustering import KMeans as SparkKMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.linalg import Vectors

from scipy.spatial.distance import cdist
import numpy as np


def get_distortion(X, kmeans_model):
	return sum(np.min(cdist(X, kmeans_model.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0]


class TimedOutKMeans:
	pass


_KMEANS_STATE = [
	'_n_clusters', '_n_jobs', '_kwargs', '_model_dict', '_env', '_features', '_evaluator', '_raise_timeout',
	'_timeout', '_timed_out'
]


class KMeans:
	def __init__(
			self, n_clusters, timeout=None, evaluator=None, raise_timeout=True, **kwargs
	):
		"""
		:type n_clusters: int
		:type n_jobs: int
		:type env: str
		:type features: list[str]
		:type X: SparkDF or PandasDF
		:type raise_timeout: bool
		:type evaluator: ClusteringEvaluator
		"""
		self._n_clusters = n_clusters
		self._kwargs = kwargs

		self._model_dict = None
		self._env = None
		self._features = None

		self._evaluator = evaluator
		self._raise_timeout = raise_timeout

		self._timeout = timeout
		self._timed_out = False

	def __getstate__(self):
		return {
			name: getattr(self, name)
			for name in _KMEANS_STATE
		}

	def __setstate__(self, state):
		for name, value in state.items():
			setattr(self, name, value)

	#  PYTHON #

	def _fit_python(self, X):
		"""
		:type X: PandasDF
		"""
		self._features = list(X.columns)
		model = SklearnKMeans(
			n_clusters=self.n_clusters, **self._kwargs
		)
		if self._timeout:
			try:
				func_timeout(timeout=self._timeout, func=model.fit, kwargs={'X': X})
				distortion = get_distortion(X=X, kmeans_model=model)
				inertia = model.inertia_
				predictions = model.predict(X=X)
				score = silhouette_score(X, predictions, metric='euclidean')

			except FunctionTimedOut as e:
				self._timed_out = True
				if self._raise_timeout:
					raise e
				else:
					model = TimedOutKMeans()
				distortion = None
				inertia = None
				score = None
		else:
			model.fit(X=X)
			distortion = get_distortion(X=X, kmeans_model=model)
			inertia = model.inertia_
			predictions = model.predict(X=X)
			score = silhouette_score(X, predictions, metric='euclidean')

		self._model_dict = {
			'kmeans': model,
			'distortion': distortion,
			'inertia': inertia,
			'silhouette_score': score
		}
		return self

	@property
	def _python_model(self):
		"""
		:rtype: SklearnKMeans
		"""
		return self._model_dict['kmeans']

	@property
	def _python_cluster_centers(self):
		"""
		:rtype: list[np_array]
		"""
		return list(self._python_model.cluster_centers_)

	def _transform_python(self, X, prefix='distance_', keep_columns=False):
		"""
		:type X: PandasDF
		:type prefix: str
		:rtype: PandasDF
		"""
		result = PandasDF(
			self._python_model.transform(X=X[self._features]),
			columns=[f'{prefix}{x + 1}' for x in range(self._n_clusters)]
		)
		if isinstance(X, PandasDF):
			result.index = X.index

		if not keep_columns:
			return result

		elif isinstance(keep_columns, (list, str)):
			if isinstance(keep_columns, str):
				keep_columns = [keep_columns]
		else:
			keep_columns = list(X.columns)

		return concat([X[keep_columns], result], axis=1)

	def _predict_python(self, X, prefix='cluster_', keep_columns=False, return_dataframe=False):
		"""
		:type X: PandasDF
		:type prefix: str
		:type keep_columns: bool or str or list[str]
		:type return_dataframe: bool
		:rtype: PandasSeries or PandasDF
		"""
		ndarray = self._python_model.predict(X=X[self._features])
		series = PandasSeries(ndarray, name='prediction')
		predictions = series.apply(lambda x: f'{prefix}{x + 1}')
		if keep_columns:
			if isinstance(keep_columns, str):
				keep_columns = [keep_columns]

			result = X.copy()
			if isinstance(keep_columns, list):
				result = result[keep_columns]

			result['prediction'] = predictions
			return result

		elif return_dataframe:
			return predictions.to_frame(name='prediction')

		else:
			return predictions

	# SPARK #

	def _fit_spark(self, X):
		"""
		:type X: SparkDF
		"""
		self._features = X.columns
		assembler = VectorAssembler(inputCols=self._features, outputCol="features")
		assembled = assembler.transform(X)
		kmeans = SparkKMeans(k=self.n_clusters).fit(assembled.select('features'))
		if self._evaluator is not None:
			clustered = kmeans.transform(assembled)
			score = self._evaluator.evaluate(clustered)
			inertia = kmeans.summary.trainingCost

		else:
			score = None
			inertia = None

		self._model_dict = {
			'assembler': assembler,
			'kmeans': kmeans,
			'silhouette_score': score,
			'inertia': inertia
		}
		return self

	@property
	def _spark_model(self):
		"""
		:rtype: SparkKMeans
		"""
		return self._model_dict['kmeans']

	@property
	def _spark_assembler(self):
		"""
		:rtype: VectorAssembler
		"""
		return self._model_dict['assembler']

	@property
	def _spark_cluster_centers(self):
		"""
		:rtype: list[np_array]
		"""
		return self._spark_model.clusterCenters()

	@staticmethod
	def _get_keep_columns(X, keep_columns):
		if isinstance(keep_columns, str):
			keep_columns = [keep_columns]
		elif isinstance(keep_columns, list):
			pass
		elif keep_columns == True:
			keep_columns = list(X.columns)
		elif keep_columns == False or keep_columns is None:
			keep_columns = []
		else:
			raise TypeError(f'keep_columns of type {type(keep_columns)} is not supported!')
		return keep_columns

	def _transform_and_predict_spark(self, X, add_distances, keep_prediction, distance_prefix, cluster_prefix, keep_columns):
		assembled = self._spark_assembler.transform(X)
		transformed = self._spark_model.transform(assembled)

		keep_columns = self._get_keep_columns(X=X, keep_columns=keep_columns)
		transformed = transformed.select(*[
			col for col in transformed.columns
			if (col in transformed.columns and col not in X.columns) or col in keep_columns
		])

		if add_distances:
			centers = self.cluster_centers

			@f.udf(DoubleType())
			def _get_distance(features, cluster):
				"""
				:type features: np_array
				:rtype: SparkColumn
				"""
				center = centers[cluster]
				return float(Vectors.squared_distance(features, center) ** 0.5)

			transformed = (
				transformed
				.select(*transformed.columns, *[
					_get_distance('features', f.lit(cluster)).alias(f'{distance_prefix}{cluster + 1}')
					for cluster in range(len(centers))
				])
			)

		transformed = transformed.drop('features')

		if not keep_prediction:
			transformed = transformed.drop('prediction')
		else:
			@f.udf(StringType())
			def _convert_prediction_to_string(x):
				return f'{cluster_prefix}{x + 1}'

			transformed = transformed.withColumn('prediction', _convert_prediction_to_string('prediction'))

		return transformed

	def _predict_spark(self, X, prefix='cluster_', keep_columns=False, add_distance=False, distance_prefix='distance_'):
		"""
		:type X: SparkDF
		:type prefix: str
		:type keep_columns: bool or NoneType or list[str] or str
		:type add_distance: bool
		:type distance_prefix: str
		:rtype: SparkDF
		"""
		return self._transform_and_predict_spark(
			X=X, cluster_prefix=prefix, keep_columns=keep_columns, keep_prediction=True,
			add_distances=add_distance, distance_prefix=distance_prefix
		)

	def _transform_spark(
			self, X, prefix='distance_', keep_columns=False, add_prediction=False, cluster_prefix='cluster_'
	):
		"""
		:type X: SparkDF
		:type prefix: str
		:type keep_columns: bool or NoneType or list[str] or str
		:type add_prediction: bool
		:type cluster_prefix: str
		:rtype: SparkDF
		"""
		return self._transform_and_predict_spark(
			X=X, distance_prefix=prefix, keep_columns=keep_columns, add_distances=True,
			keep_prediction=add_prediction, cluster_prefix=cluster_prefix
		)

	# GENERAL METHODS #

	def fit(self, X):
		"""
		:type X: SparkDF or PandasDF
		"""
		if isinstance(X, SparkDF):
			self._env = 'spark'
		elif isinstance(X, PandasDF):
			self._env = 'python'
		else:
			raise RuntimeError(f'unknown data type: {type(X)}')

		if self._evaluator is None:
			self._evaluator = ClusteringEvaluator()

		if self._env == 'spark':
			return self._fit_spark(X=X)

		elif self._env == 'python':
			return self._fit_python(X=X)

		else:
			raise RuntimeError(f'unknown environment {self._env}')

	@property
	def cluster_centers(self):
		"""
		:rtype: list[np_array]
		"""
		if self._env == 'spark':
			return self._spark_cluster_centers
		else:
			return self._python_cluster_centers

	def transform(self, X, keep_columns=False):
		"""
		:type X: SparkDF or PandasDF
		:type keep_columns: bool or list[str] or str
		"""
		if self._env == 'spark':
			return self._transform_spark(X=X, keep_columns=keep_columns)

		elif self._env == 'python':
			return self._transform_python(X=X, keep_columns=keep_columns)

		else:
			raise RuntimeError(f'unknown environment {self._env}')

	def fit_transform(self, X, keep_columns=False):
		"""
		:type X: SparkDF or PandasDF
		:type keep_columns: bool
		"""
		self.fit(X=X)
		return self.transform(X=X, keep_columns=keep_columns)

	def predict(self, X, prefix='cluster_', keep_columns=False, return_dataframe=None):
		"""
		:type X: SparkDF or PandasDF or PandasSeries
		:type prefix: str
		:type keep_columns: bool or str or list[str]
		:type return_dataframe: bool
		"""
		if self._env == 'spark':
			return self._predict_spark(X=X, prefix=prefix, keep_columns=keep_columns)

		elif self._env == 'python':
			return self._predict_python(
				X=X, prefix=prefix, keep_columns=keep_columns, return_dataframe=return_dataframe
			)

		else:
			raise RuntimeError(f'unknown environment {self._env}')

	def fit_predict(self, X, prefix='cluster_', keep_columns=False):
		self.fit(X=X)
		predictions = self.predict(X=X, prefix=prefix, keep_columns=keep_columns)
		return predictions

	def transform_and_predict(self, X, keep_columns=False):
		"""
		:type X: PandasDF or SparkDF
		:type keep_columns: bool or str or list[str]
		:rtype: PandasDF
		"""

		if isinstance(X, SparkDF):
			return self._transform_and_predict_spark(
				X=X, add_distances=True, keep_prediction=True, distance_prefix='distance_', cluster_prefix='cluster_',
				keep_columns=keep_columns
			)

		else:
			transformed = self._transform_python(X=X, keep_columns=True, prefix='distance_')
			keep_columns = self._get_keep_columns(X=X, keep_columns=keep_columns)
			keep_columns = keep_columns + [col for col in transformed.columns if col not in X.columns]
			return self._predict_python(X=transformed, return_dataframe=True, keep_columns=keep_columns)

	@property
	def n_clusters(self):
		"""
		:rtype: int
		"""
		return self._n_clusters

	@property
	def timedout(self):
		return self._timed_out

	@property
	def distortion(self):
		return self._model_dict.get('distortion', None)

	@property
	def inertia(self):
		return self._model_dict.get('inertia', None)

	@property
	def silhouette_score(self):
		return self._model_dict.get('silhouette_score', None)
