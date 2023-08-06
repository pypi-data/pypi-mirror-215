from .Classifier import Classifier


def get_renames(strings, sep='_'):
	"""
	Get renames for strings based on their counts.

	:param strings: List of strings.
	:type strings: list
	:param sep: Separator to be used between string and index. Defaults to '_'.
	:type sep: str, optional
	:return: List of tuples containing the original string and its rename.
	:rtype: list
	:example:

	>>> strings = ['a', 'b', 'a', 'c']
	>>> result = get_renames(strings)
	>>> print(result)
	[('a', 'a_1'), ('b', 'b_1'), ('a', 'a_2'), ('c', 'c_1')]
	"""
	counts = {}
	for s in strings:
		if s in counts:
			counts[s] += 1
		else:
			counts[s] = 1

	result = []

	indices = {}

	for s in strings:
		if counts[s] == 1:
			result.append((s, s))
		else:
			if s not in indices:
				result.append((s, f'{s}{sep}1'))
				indices[s] = 2
			else:
				index = indices[s]
				result.append((s, f'{s}{sep}{index}'))
				indices[s] += 1

	return result


class EnsembleClassifier(Classifier):
	def __init__(self, children, target_column, negative_label, model, prediction_column=None,
            probability_column=None, probability_prefix=None, vectorized_features_column=None,
            encoded_prediction_column=None, raw_prediction_column=None,
            model_name=None,
            spark=None, s3=None
	    ):
		"""
		:type children: list[Classifier]
		"""
		prediction_renames = get_renames([classifier.prediction_column for classifier in children])
		prob_prefix_renames = get_renames([classifier.probability_prefix for classifier in children])

		new_features = []
		self._children = []

		for pred_rename, prob_prefix_rename, classifier in zip(prediction_renames, prob_prefix_renames, children):

			new_classifier = classifier.copy(keep_trained=True)
			old_pred, new_pred = pred_rename
			assert new_classifier.prediction_column == old_pred
			if old_pred != new_pred:
				new_classifier.prediction_column = new_pred

			old_prob_prefix, new_prob_prefix = prob_prefix_rename
			assert new_classifier.probability_prefix == old_prob_prefix
			if old_prob_prefix != new_prob_prefix:
				new_classifier.probability_prefix = new_prob_prefix

			new_features.append(new_prob_prefix)
			self._children.append(new_classifier)

		super().__init__(
			model=model,
			feature_columns=new_features, target_column=target_column, negative_label=negative_label,
			prediction_column=prediction_column, probability_column=probability_column,
			probability_prefix=probability_prefix, vectorized_features_column=vectorized_features_column,
			model_name=model_name, spark=spark, s3=s3
		)

	def copy(self, keep_trained=False):
		"""
		:rtype: EnsembleClassifier
		"""
		model = self._model.copy()
		classifier_copy = self.__class__(
			children=self._children,
			spark=self._spark, s3=self._s3, model=model, **self._parameters
		)
		if keep_trained:
			if self._trained_model is not None and keep_trained:
				classifier_copy._trained_model = self._trained_model.copy()
			classifier_copy._encoder = self._encoder.copy()
			if self._decoder is not None:
				classifier_copy._decoder = self._decoder.copy()
			classifier_copy._is_fit = self._is_fit
		return classifier_copy

	def transform_by_children(self, data):
		original_columns = list(data.columns)

		transformed_by_children = data
		for child in self._children:
			transformed_by_children = child.transform(data=transformed_by_children)
			transformed_by_children = (
				transformed_by_children
				.select(*original_columns, child.prediction_column, child.probability_column)
			)

		missing_columns = [col for col in self.feature_columns if col not in data.columns]
		if len(missing_columns) > 0:
			raise RuntimeError(f'columns missing: {missing_columns}')

		return data

	def fit(self, data):
		transformed_by_children = self.transform_by_children(data=data)
		return super().fit(data=transformed_by_children)

	def _transform_and_evaluate(self, data, evaluate):
		transformed_by_children = self.transform_by_children(data=data)
		return super()._transform_and_evaluate(data=transformed_by_children, evaluate=evaluate)

