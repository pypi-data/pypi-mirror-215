from pandas import DataFrame
from joblib import Parallel, delayed
from math import sqrt
import matplotlib.pyplot as plt

from ...time.progress import ProgressBar, iterate
from ...time import get_elapsed, get_now
from ...exceptions import ClusteringError

from .KMeans import KMeans


_CLUSTERING_OPTIMIZER_STATE = [
	'_min_k', '_max_k', '_n_jobs', '_models', '_kwargs', '_keep_models', '_distortions', '_inertias',
	'_silhouette_scores', '_timeout'
]


class ClusteringOptimizer:
	def __init__(
			self, min_k, max_k, n_jobs=-1, keep_models=False, timeout=None,
			**kwargs
	):
		self._min_k = min_k
		self._max_k = max_k
		self._n_jobs = n_jobs
		self._models = None
		self._kwargs = kwargs
		self._keep_models = keep_models
		self._distortions = None
		self._inertias = None
		self._silhouette_scores = None
		self._timeout = timeout

	def __getstate__(self):
		return {
			name: getattr(self, name)
			for name in _CLUSTERING_OPTIMIZER_STATE
		}

	def __setstate__(self, state):
		for name, value in state.items():
			setattr(self, name, value)

	def fit(self, X, echo=1, raise_timeout=True):
		if self._keep_models:
			self._models = {}

		self._distortions = {}
		self._inertias = {}
		self._silhouette_scores = {}

		def get_scores(k):
			kmeans = KMeans(
				n_clusters=k, timeout=self._timeout, raise_timeout=raise_timeout, **self._kwargs
			)
			kmeans.fit(X=X)
			if kmeans.timedout:
				return k, None, None, None

			if self._keep_models:
				return k, kmeans, kmeans.inertia, kmeans.distortion, kmeans.silhouette_score

			else:
				return k, None, kmeans.inertia, kmeans.distortion, kmeans.silhouette_score

		if self._n_jobs > 1:

			n_ks = self._max_k - self._min_k + 1
			n_jobs = min(n_ks, self._n_jobs)
			print(f'n_ks = {n_ks} n_jobs = {n_jobs}')

			processor = Parallel(n_jobs=n_jobs, backend='threading', require='sharedmem')
			result = processor(
				delayed(get_scores)(k=k)
				for k in iterate(iterable=range(self._max_k, self._min_k - 1, -1), echo_items=True, echo=echo)
			)

			for k, model, inertia, distortion, silhouette_score in result:
				if inertia is not None or distortion is not None or silhouette_score is not None:
					self._distortions[k] = distortion
					self._inertias[k] = inertia
					self._silhouette_scores[k] = silhouette_score
					if self._keep_models:
						self._models[k] = model
				else:
					raise ClusteringError(f'Both inertia and distortion are None for k: {k}')

		else:

			progress_bar = ProgressBar(total=self._max_k - self._min_k + 1, echo=echo)
			error = ''

			elapsed = 0
			for k in range(self._max_k, self._min_k - 1, -1):
				start_time = get_now()
				progress_bar.show(amount=self._max_k - k, text=f'j={self._n_jobs}, k={k}{error}, t={round(elapsed)}')
				k, model, inertia, distortion, silhouette_score = get_scores(k=k)
				if inertia is not None or distortion is not None or silhouette_score is not None:
					if self._keep_models:
						self._models[k] = model
					self._distortions[k] = distortion
					self._inertias[k] = inertia
					self._silhouette_scores[k] = silhouette_score
				else:
					raise ClusteringError(f'Both inertia and distortion are None for k: {k}')
				elapsed = max(elapsed, get_elapsed(start=start_time, unit='s'))

			progress_bar.show(amount=progress_bar.total)

	def get_scores(self, by='silhouette_score'):
		"""
		:rtype: dict
		"""
		if by.startswith('silhouette'):
			return self._silhouette_scores.copy()
		elif by.startswith('inertia'):
			return self._inertias.copy()
		elif by.startswith('distortion'):
			return self._distortions.copy()
		else:
			raise ValueError(f'Unsupported scoring method: "{by}"')

	def plot(self, by='silhouette_score', size=(16, 8), title=None):
		scores = self.get_scores(by=by)
		if title is None:
			if by.startswith('silhouette'):
				title = 'Finding the Optimal k with the Silhouette Method'
			else:
				title = 'Finding the Optimal k with the Elbow Method'

		plt.figure(figsize=size)
		plt.plot(list(scores.keys()), list(scores.values()), 'bx-')
		plt.xlabel('k')
		plt.ylabel(by.replace('_', ' ').capitalize())
		plt.title(title)
		plt.show()

	def get_optimal_number_of_clusters(self, by='silhouette'):
		"""
		:param str by: can be 'inertia' or 'distortion'
		:rtype: int
		"""
		x1, x2 = min(self._silhouette_scores.keys()), max(self._silhouette_scores.keys())

		if by.startswith('silhouette'):
			return max(self._silhouette_scores, key=self._silhouette_scores.get)

		elif by.startswith('inertia'):
			y_dictionary = self._inertias

		elif by.startswith('distort'):
			y_dictionary = self._distortions

		else:
			raise ValueError(f'Method "{by}" is not supported!')

		# Elbow method
		y1, y2 = y_dictionary[x1], y_dictionary[x2]
		distances = []
		for x in range(x1, x2 + 1):
			y = y_dictionary[x]

			numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
			denominator = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
			distances.append(numerator / denominator)

		return distances.index(max(distances)) + 2

	@property
	def optimal_number_of_clusters(self):
		"""
		:rtype: int
		"""

		scores = []
		for by in ['silhouette', 'inertia', 'distortion']:
			try:
				score = self.get_optimal_number_of_clusters(by=by)
				scores.append(score)
			except TypeError:
				continue

		return max(scores)

	@property
	def records(self):
		"""
		:rtype: list[dict]
		"""
		return [
			{
				'k': k, 'distortion': self._distortions[k], 'inertia': self._inertias[k],
				'silhouette_score': self._silhouette_scores[k]
			}
			for k in range(self._min_k, self._max_k + 1)
		]

	@property
	def data(self):
		"""
		:rtype: DataFrame
		"""
		return DataFrame.from_records(self.records)
