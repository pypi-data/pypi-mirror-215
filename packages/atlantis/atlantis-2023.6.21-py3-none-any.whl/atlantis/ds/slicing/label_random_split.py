from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType
from pandas import DataFrame as PandasDF
from pyspark.sql import DataFrame
from pyspark.sql import functions as f
from .get_random_by_object import get_random_by_object


def label_random_split(data, weights, split_column='split', id_columns=None, seed=None, drop_temp_columns=False):
	"""
	:type data: DataFrame or PandasDF
	:type weights: list[float]
	:type id_columns: NoneType or str or list[str]
	:type seed: NoneType or int
	:rtype: DataFrame or PandasDF
	"""
	if isinstance(data, PandasDF):
		new_data = data.copy()
		if id_columns is None:
			new_data['_id_'] = range(new_data.shape[0])
			id_columns = ['_id_']
			if drop_temp_columns:
				columns_to_drop = ['_id_']
			else:
				columns_to_drop = None

		else:
			if isinstance(id_columns, str):
				id_columns = [id_columns]

			columns_to_drop = None

		missing_id_columns = [col for col in id_columns if col not in new_data.columns]
		if len(missing_id_columns) > 0:
			raise KeyError(f'missing id columns: {missing_id_columns}')

		def _get_split(row):
			obj = [row[id_col] for id_col in id_columns]
			result = get_random_by_object(obj=obj, weights=weights, seed=seed)
			return result

		new_data[split_column] = new_data.apply(_get_split,axis=1)

		if columns_to_drop is not None:
			new_data = new_data.drop(columns=columns_to_drop)

	elif isinstance(data, DataFrame):
		if id_columns is None:
			window = Window.orderBy(f.monotonically_increasing_id())
			new_data = data.withColumn('_id_', f.row_number().over(window))
			id_columns = ['_id_']
			if drop_temp_columns:
				columns_to_drop = id_columns
			else:
				columns_to_drop = None

		else:
			new_data = data
			if isinstance(id_columns, str):
				id_columns = [id_columns]

			columns_to_drop = None

		missing_id_columns = [col for col in id_columns if col not in new_data.columns]
		if len(missing_id_columns) > 0:
			raise KeyError(f'missing id columns: {missing_id_columns}')

		@f.udf(IntegerType())
		def _get_split(*args):
			return get_random_by_object(obj=args, weights=weights, seed=seed)

		new_data = new_data.withColumn(split_column, _get_split(*id_columns))

		if columns_to_drop is not None:
			new_data = new_data.drop(*columns_to_drop)

	else:
		raise TypeError(f'data of type {type(data)} is not supported')

	return new_data