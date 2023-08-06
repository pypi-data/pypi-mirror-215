from pyspark.sql import DataFrame
from pyspark.sql import functions as f
import pandas as pd
from sparta.wrangling import union
from ..classification import Classifier
from ..slicing import get_random_split
from .validate_classifier import validate_classifier


class TrainTestData:
	def __init__(self, training_data, test_data, echo=0):
		assert isinstance(training_data, DataFrame)
		assert isinstance(test_data, DataFrame)
		self._training = training_data
		self._test = test_data
		self._echo = echo

	@property
	def training_data(self):
		"""
		:rtype: DataFrame
		"""
		return self._training

	@property
	def test_data(self):
		"""
		:rtype: DataFrame
		"""
		return self._test

	def train_and_test(self, classifier):
		"""
		:type classifier: Classifier
		:rtype: DataFrame
		"""
		classifier = classifier.copy(keep_trained=False).fit(data=self.training_data)
		if isinstance(classifier, Classifier):
			training_result = classifier.evaluate(self.training_data)
			test_result = classifier.evaluate(data=self.test_data)
		else:
			raise TypeError(f'classifier of type {type(classifier)} is not supported')

		training_result['set'] = 'training'
		test_result['set'] = 'test'

		return pd.concat([training_result, test_result])


class CrossValidationData(TrainTestData):
	@classmethod
	def from_folds(cls, folds, holdout_data):
		"""
		:type folds: list[DataFrame]
		:type holdout_data: DataFrame
		:rtype: CrossValidationData
		"""
		train_test_pairs = []
		for fold_number in range(len(folds)):
			test_df = folds[fold_number]
			training_dfs = folds[:fold_number] + folds[fold_number + 1:]
			training_df = union(*training_dfs, n_jobs=4)
			train_test_pairs.append({'training': training_df, 'test': test_df})

		training_data = union(folds, n_jobs=4)
		return cls(train_test_pairs=train_test_pairs, training_data=training_data, holdout_data=holdout_data)

	def get_data(self, _set_column='__set__', _fold_column='__fold__'):
		"""
		returns the data with identifiers
		:rtype: DataFrame
		"""
		result = []
		for i, fold in enumerate(self.folds):
			df = fold.withColumn(_set_column, f.lit('validation')).withColumn(_fold_column, f.lit(i))
			result.append(df)

		holdout = self.holdout_data.withColumn(_set_column, f.lit('holdout')).withColumn(_fold_column, f.lit(-1))
		result.append(holdout)

		return union(result, n_jobs=4)

	def save(self, path, partition_by=None, format='delta', _set_column='__set__', _fold_column='__fold__'):
		df = self.get_data(_set_column=_set_column, _fold_column=_fold_column).repartition(_fold_column)

		df_write = df.write.option('header', True).option('overwriteSchema', True)

		if partition_by is None:
			df_write = df_write.partitionBy(_set_column)
		elif isinstance(partition_by, str):
			df_write = df_write.partitionBy(_set_column, partition_by)
		elif isinstance(partition_by, (list, tuple)):
			df_write = df_write.partitionBy(_set_column, *partition_by)
		else:
			raise TypeError(f'partition_by of type {type(partition_by)} is not supported')

		return df_write.mode('overwrite').format(format).save(path)

	@classmethod
	def load(cls, path, format='delta', _set_column='__set__', _fold_column='__fold__'):
		from pyspark.sql.session import SparkSession
		spark = SparkSession.builder.getOrCreate()
		if format == 'csv':
			df = spark.read.format(format).option('header', True).load(path)
		else:
			df = spark.read.format(format).load(path)

		holdout = df.filter(f.col(_set_column) == 'holdout').drop(_set_column, _fold_column)

		validation = df.filter(f.col(_set_column) == 'validation').drop(_set_column)
		fold_values = validation.agg(f.collect_set(_fold_column)).collect()[0][0]
		folds = [
			validation.filter(f.col(_fold_column) == fold_value).drop(_fold_column)
			for fold_value in sorted(fold_values)
		]

		return cls.from_folds(folds=folds, holdout_data=holdout)

	def __init__(self, train_test_pairs, training_data, holdout_data):
		super().__init__(training_data=training_data, test_data=holdout_data)

		assert isinstance(train_test_pairs, (list, tuple))
		validation_pairs = []
		for training_test in train_test_pairs:
			if isinstance(training_test, dict):
				training_data = training_test['training']
				test_data = training_test['test']
				validation_pairs.append(TrainTestData(training_data=training_data, test_data=test_data))
			else:
				assert isinstance(training_test, TrainTestData)
				validation_pairs.append(training_test)

		self._validation_pairs = tuple(validation_pairs)
		self._folds = None

	@property
	def folds(self):
		"""
		:rtype: tuple[DataFrame]
		"""
		if self._folds is None:
			self._folds = tuple(validation_pair.test_data for validation_pair in self.validation_pairs)
		return self._folds

	@property
	def validation_pairs(self):
		"""
		:rtype: tuple[TrainTestData]
		"""
		return self._validation_pairs

	@property
	def holdout_data(self):
		"""
		:rtype: DataFrame
		"""
		return self.test_data

	@property
	def train_test_data(self):
		"""
		:rtype: TrainTestData
		"""
		return TrainTestData(training_data=self.training_data, test_data=self.holdout_data)

	def _validate_one_classifier(self, classifier, name):
		return validate_classifier(
			classifier=classifier, name=name, validation_pairs=self.validation_pairs, echo=self._echo
		)

	def validate(self, classifier=None, classifiers=None):
		if classifiers is None and classifier is not None:
			return self._validate_one_classifier(classifier=classifier, name=None)
		elif classifier is None and classifiers is not None:
			if not isinstance(classifiers, (list, tuple, dict)):
				return self._validate_one_classifier(classifier=classifiers, name=None)

			if isinstance(classifiers, dict):
				results = [
					self._validate_one_classifier(classifier=classifier, name=name)
					for name, classifier in classifiers.items()
				]
			else:
				results = [
					self._validate_one_classifier(classifier=classifier, name=str(i))
					for i, classifier in enumerate(classifiers)
				]

			return pd.concat(results)

	@staticmethod
	def find_best_model_name(validation_result, label, by='f1_score'):
		filtered = validation_result[(validation_result['label'] == label) & (validation_result['set'] == 'test')]
		if filtered.shape[0] == 0:
			filtered = validation_result[validation_result['label'] == str(label)]
			if filtered.shape[0] == 0:
				raise RuntimeError(f'Cannot find label {label} of type {type(label)}')
		return filtered.sort_values(by=by, ascending=False).iloc[0]['model_name']

	@property
	def validation_data(self):
		return self.training_data

	def find_best_classifier(self, classifiers, label, validation_result=None, by='f1_score'):
		"""
		:param label: the class label
		:type classifiers: list[Classifier] or dict[str, Classifier]
		:rtype: Classifier
		"""
		if validation_result is None:
			validation_result = self.validate(classifiers=classifiers)
		best_model_name = self.find_best_model_name(validation_result=validation_result, label=label, by=by)

		if isinstance(classifiers, dict):
			classifier = classifiers[best_model_name]
		elif isinstance(classifiers, (list, tuple)):
			classifier = classifiers[int(best_model_name)]
		else:
			classifier = classifiers[best_model_name]

		new_classifier = classifier.copy(only_model=best_model_name)
		new_classifier.fit(data=self.validation_data)
		return new_classifier


class CrossValidation:
	def __init__(self, n_folds, holdout_ratio, random_seed, broadcast=False, id_columns=None):
		self._n_folds = n_folds
		self._holdout_ratio = holdout_ratio
		self._random_seed = random_seed
		self._id_columns = id_columns
		self._broadcast = broadcast
		self._split_data = self.build_data_splitter()

	def split_data(self, data):
		"""
		:type data: DataFrame
		:rtype: CrossValidationData
		"""
		assert isinstance(data, DataFrame)
		result = self._split_data(data=data)
		assert isinstance(result, CrossValidationData)
		return result

	def build_data_splitter(self):
		"""
		returns a function that splits dataframes
		:rtype: callable
		"""
		holdout_ratio = self._holdout_ratio
		validation_ratio = 1 - holdout_ratio
		random_seed = self._random_seed
		n_cross_validation_folds = self._n_folds
		id_columns = self._id_columns
		broadcast = self._broadcast

		def _data_splitter(data):
			"""
			:type data: DataFrame
			:rtype: CrossValidationData
			"""
			validation_data, holdout_data = get_random_split(
				data=data, weights=[validation_ratio, holdout_ratio], id_columns=id_columns, seed=random_seed,
				broadcast=broadcast
			)
			fold_ratios = [1 / n_cross_validation_folds] * n_cross_validation_folds

			folds = get_random_split(
				data=validation_data, weights=fold_ratios, id_columns=id_columns, seed=random_seed,
				broadcast=broadcast
			)
			train_test_pairs = []
			for fold_number in range(n_cross_validation_folds):
				test_df = folds[fold_number]
				training_dfs = folds[:fold_number] + folds[fold_number + 1:]
				training_df = union(*training_dfs, n_jobs=4)
				train_test_pairs.append({'training': training_df, 'test': test_df})

			return CrossValidationData(
				train_test_pairs=train_test_pairs, training_data=validation_data, holdout_data=holdout_data
			)
			# return {'validation': train_test_pairs, 'holdout': holdout_data}

		return _data_splitter
