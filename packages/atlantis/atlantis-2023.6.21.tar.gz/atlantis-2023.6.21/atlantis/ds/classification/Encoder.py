from pyspark.sql.session import SparkSession
from pyspark.sql import functions as f
from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, IntegerType, FloatType
from amazonian import S3
# from ..helpers.save_dictionary_as_dataframe import save_dictionary_as_dataframe, load_dictionary_as_dataframe


class Encoder:
	def __init__(self, column, negative_label=None, encoded_column=None, spark=None, s3=None):
		if spark is None:
			spark = SparkSession.builder.getOrCreate()
		if s3 is None:
			s3 = S3()

		self._spark = spark
		self._s3 = s3

		self._column = column
		if encoded_column is None:
			encoded_column = f'{column}_encoded'
		self._encoded_column = encoded_column

		self._negative_label = negative_label
		self._labels = None
		self._labels_df = None
		self._mapping_dictionary = {}

	def __repr__(self):
		return f'<Encoder: {self.column} -> {self.encoded_column}>'

	def copy(self):
		encoder_copy = self.__class__(
			column=self._column, encoded_column=self._encoded_column, negative_label=self._negative_label, spark=self._spark
		)
		if self._labels is not None:
			encoder_copy._labels = self._labels.copy()
		encoder_copy._mapping_dictionary = self._mapping_dictionary.copy()
		return encoder_copy

	def save(self, path, mode='overwrite'):
		dictionary = {
			'column': self._column,
			'encoded_column': self._encoded_column,
			'negative_label': self._negative_label
		}
		self._s3.save_pickle(obj=dictionary, path=f'{path}/parameters.pickle', mode=mode)
		if self._labels_df is not None:
			self._labels_df.write.mode(mode).csv(f'{path}/labels_data.csv')

		# save_dictionary_as_dataframe(dictionary=dictionary, path=f'{path}/parameters.csv', spark=self._spark)
		if len(self._mapping_dictionary) > 0:
			self._s3.save_pickle(obj=self._mapping_dictionary, path=f'{path}/mapping.pickle', mode=mode)
			#save_dictionary_as_dataframe(dictionary=self._mapping_dictionary, path=f'{path}/mapping.csv', spark=self._spark)

	@classmethod
	def load(cls, path, spark=None, s3=None):
		if spark is None:
			spark = SparkSession.builder.getOrCreate()
		if s3 is None:
			s3 = S3()

		# parameters = load_dictionary_as_dataframe(path=f'{path}/parameters.csv', spark=spark)
		parameters = s3.load_pickle(path=f'{path}/parameters.pickle')
		encoder = cls(spark=spark, **parameters)
		try:
			encoder._labels_df = spark.read.csv(f'{path}/labels_data.csv')
			encoder._labels = encoder._labels_df.rdd.flatMap(lambda x: x).collect()
			encoder._set_mapping_dictionary()
		except:
			try:
				# mapping_dictionary = load_dictionary_as_dataframe(path=f'{path}/mapping.csv', spark=spark)
				mapping_dictionary = s3.load_pickle(path=f'{path}/mapping.pickle')
				encoder._mapping_dictionary = mapping_dictionary
				encoder._labels = list(encoder._mapping_dictionary.keys())
			except:
				pass
		return encoder

	@property
	def column(self):
		return self._column

	@property
	def encoded_column(self):
		return self._encoded_column

	def _set_mapping_dictionary(self):
		first_type = type(self._labels[0])
		if not all(isinstance(item, first_type) for item in self._labels):
			raise TypeError(f'labels are of different types: {[type(x) for x in self._labels]}')
		if self._negative_label is not None:
			if not isinstance(self._negative_label, first_type):
				if isinstance(first_type, str):
					self._negative_label = str(self._negative_label)
				elif isinstance(first_type, int):
					self._negative_label = int(self._negative_label)
				else:
					raise TypeError(f'negative label of type {type(self._negative_label)} does not match the labels: {first_type}')

			if self._negative_label not in self._labels:
				raise ValueError(f'negative label {self._negative_label} does not exist among the labels: {self._labels}')

		if self._negative_label is not None:
			self._mapping_dictionary[self._negative_label] = 0

			new_label = 1
			for label in self._labels:
				if label != self._negative_label:
					self._mapping_dictionary[label] = new_label
					new_label += 1
		else:
			new_label = 0
			for label in self._labels:
				self._mapping_dictionary[label] = new_label
				if new_label == 0:
					self._negative_label = label
				new_label += 1

	def fit(self, data):
		"""
		:type data: DataFrame
		:rtype: Encoder
		"""
		self._labels_df = data.select(self._column).distinct()
		self._labels = self._labels_df.rdd.flatMap(lambda x: x).collect()
		self._set_mapping_dictionary()

		return self

	def transform(self, data):
		"""
		:type data: DataFrame
		:rtype: DataFrame
		"""

		mapping_dictionary = self._mapping_dictionary.copy()

		@f.udf(IntegerType())
		def _map_column(x):
			try:
				return mapping_dictionary[x]
			except KeyError:
				return None

		return data.withColumn(self._encoded_column, _map_column(self._column))

	def fit_transform(self, data):
		self.fit(data=data)
		return self.transform(data=data)


class Decoder:
	def __init__(self, encoder, column, decoded_column=None):
		"""
		:type encoder: Encoder
		:type column: str
		:type decoded_column: str
		"""
		self._encoder = encoder
		self._column = column
		if decoded_column is None:
			decoded_column = f'{column}_decoded'
		self._decoded_column = decoded_column

		if all([isinstance(label, int) for label in encoder._labels]):
			self._original_type = 'integer'
		elif all([isinstance(label, float) for label in encoder._labels]):
			self._original_type = 'float'
		elif all([isinstance(label, str) for label in encoder._labels]):
			self._original_type = 'string'
		else:
			raise TypeError(f'Unsupported types: {type(encoder._labels[0])}')

		self._mapping_dictionary = {v: k for k, v in self._encoder._mapping_dictionary.items()}

	def __repr__(self):
		return f'<Decoder: {self.column} -> {self.decoded_column}>'

	def copy(self):
		return self.__class__(encoder=self._encoder.copy(), column=self.column, decoded_column=self.decoded_column)

	@property
	def column(self):
		return self._column

	@property
	def encoded_column(self):
		return self.column

	@property
	def labels(self):
		return self._encoder._labels

	@property
	def decoded_column(self):
		return self._decoded_column

	def transform(self, data):
		"""
		:type data: DataFrame
		:rtype: DataFrame
		"""
		if self._original_type == 'integer':
			the_type = IntegerType()
		elif self._original_type == 'float':
			the_type = FloatType()
		elif self._original_type == 'string':
			the_type = StringType()
		else:
			raise TypeError(f'Unsupported type for labels: {self._original_type}')

		mapping_dictionary = self._mapping_dictionary.copy()

		@f.udf(the_type)
		def _map_column_back(x):
			return mapping_dictionary[x]

		return data.withColumn(self._decoded_column, _map_column_back(self._column))
