from pyspark.sql import DataFrame
from pyspark.sql import functions as f
from pandas import DataFrame as PandasDF
from .label_random_split import label_random_split
from ._get_random_split_without_hashing import _get_random_split_without_hashing


def get_random_split(data, weights, id_columns=None, seed=None, broadcast=False, use_hashing=True):
	if use_hashing:
		labelled = label_random_split(
			data=data, weights=weights, id_columns=id_columns, seed=seed, drop_temp_columns=True,
			split_column='_split_'
		)

		if isinstance(data, PandasDF):
			def _filter_data(data, i):
				return data[data['_split_'] == i].drop(columns=['_split_'])

		elif isinstance(data, DataFrame):
			def _filter_data(data, i):
				return data.filter(f.col('_split_') == i).drop('_split_')

		else:
			raise TypeError(f'data of type {type(data)} is not supported')

		return [_filter_data(data=labelled, i=i) for i in range(len(weights))]

	else:
		return _get_random_split_without_hashing(
			data=data, weights=weights, broadcast=broadcast, id_columns=id_columns, seed=seed
		)
