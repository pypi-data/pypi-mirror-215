from pyspark.sql import functions as f


def _get_random_split_without_hashing(data, weights, broadcast=False, id_columns=None, seed=None):
	"""
	:type data: DataFrame
	:type weights: list[float]
	:type id_columns: str or list[str]
	:type seed: int
	:rtype: list[DataFrame]
	"""
	if id_columns is None:
		result = data.randomSplit(weights=weights, seed=seed)
	else:
		if isinstance(id_columns, str):
			id_columns = [id_columns]

		missing_cols = [col for col in id_columns if col not in data.columns]
		if len(missing_cols) > 0:
			raise KeyError(f'columns are missing: {missing_cols}')

		id_data = data.select(*id_columns).distinct()

		id_split = id_data.randomSplit(weights=weights, seed=seed)
		if broadcast:
			result = [f.broadcast(id_subdata).join(data, on=id_columns, how='inner') for id_subdata in id_split]
		else:
			result = [id_subdata.join(data, on=id_columns, how='inner') for id_subdata in id_split]

	return result
