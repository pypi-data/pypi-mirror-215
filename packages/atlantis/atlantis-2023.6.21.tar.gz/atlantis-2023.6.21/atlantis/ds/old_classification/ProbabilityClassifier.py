# probability classifier is a classifier that can use any linear and non linear classifier
# together with a linear regression
# the classifier is trained on the data first, then the regression model is trained on the probability
# then the classifier is built on top of the probability that the regression model predicts


from sklearn.ensemble import RandomForestClassifier as SklearnRandomForestClassifier
from sklearn.linear_model import LinearRegression as SklearnLinearRegression
from pyspark.ml.classification import RandomForestClassifier as SparkRandomForestClassifier
from pyspark.ml.regression import LinearRegression as SparkLinearRegression
from pandas import DataFrame as PandasDF
import pandas as pd
from sklearn.metrics import confusion_matrix
from copy import deepcopy
from ..evaluation._get_confusion_matrix_df import convert_confusion_matrix_to_df
from ..evaluation._evaluate_mutliclass_classification import _evaluate_multiclass_classification


class ProbabilityClassifier:
	def __init__(self, classifier, regressor, threshold=0.5):
		"""
		a classifier based on any other kind of classifier and a regressor that predicts probability
		:type classifier: SklearnRandomForestClassifier or SparkRandomForestClassifier
		:type regressor: SklearnLinearRegression or SparkLinearRegression
		:type threshold: float
		"""

		self._classifier = classifier
		self._regressor_first_copy = regressor
		self._regressors = None
		self._threshold = threshold

		self._classes = None
		self._x_columns = None
		self._y_dtype = None
		self._coefficients = None
		self._confusion_matrix = None

	def fit(self, X, y):
		self._x_columns = X.columns
		self._classifier.fit(X, y)
		self._y_dtype = y.dtype
		probabilities_array = self._classifier.predict_proba(X)
		probabilities = PandasDF(probabilities_array, columns=self.classes)
		self._regressors = {}

		if probabilities.shape[1] != len(self.classes):
			raise RuntimeError(f'There are {probabilities.shape[1]} probability columns and {len(self.classes)} classes!')

		for column, _class in zip(probabilities.columns, self.classes):
			if column != _class:
				raise RuntimeError(f'column {column} does not match class {_class}!')
			probability_y = probabilities[column]
			self._regressors[_class] = deepcopy(self._regressor_first_copy)
			self._regressors[_class].fit(X[self._x_columns], probability_y)

	def _predict_probabilities(self, X):
		"""
		:type X: PandasDF
		:rtype: dict[str, ndarray]
		"""
		return {
			_class: self._regressors[_class].predict(X[self._x_columns])
			for _class, model in self._regressors.items()
		}

	def predict_probabilities(
			self, X, append=False, infer_prediction=False,
			prediction_column='prediction', suffix='_prediction_probability'
	):
		probabilities = self._predict_probabilities(X=X)

		probabilities_df = PandasDF({
			f'{_class}{suffix}': probabilities[_class]
			for _class in self.classes
		})

		if infer_prediction:
			predictions = self._convert_probabilities_to_predictions(probabilities_df=probabilities_df)
			probabilities_df[prediction_column] = predictions

		if append:
			probabilities_df = pd.concat([X, probabilities_df], axis=1)

		return probabilities_df

	predict_proba = predict_probabilities

	def _convert_probabilities_to_predictions(self, probabilities_df, suffix='_prediction_probability'):

		label_to_class = {
			f'{_class}{suffix}': _class
			for _class in self.classes
		}
		return probabilities_df.idxmax(axis=1).apply(lambda x: label_to_class[x])

	def predict(self, X):
		probabilities_df = self.predict_probabilities(X=X, infer_prediction=True, prediction_column='prediction')
		return probabilities_df['prediction'].values

	@property
	def classes(self):
		"""
		:rtype: list[str]
		"""
		if self._classes is None:
			self._classes = list(self._classifier.classes_)
		return self._classes

	@property
	def coefficients(self):
		"""
		:rtype: dict[str, float]
		"""
		if self._coefficients is None:
			result = {}
			for _class, regressor in self._regressors.items():
				coef_values = list(regressor.coef_)
				if len(coef_values) != len(self._x_columns):
					raise RuntimeError(f'There are {len(self._x_columns)} features but {len(coef_values)} coefficients!')
				intercept = regressor.intercept_
				internal_dictionary = {col: value for col, value in zip(self._x_columns, coef_values)}
				internal_dictionary['intercept'] = intercept
				result[_class] = internal_dictionary
			self._coefficients = result
		return self._coefficients

	@property
	def coefficients_df(self):
		"""
		:rtype: DataFrame
		"""
		records = [
			{'class': _class, **dictionary}
			for _class, dictionary in self.coefficients.items()
		]
		return PandasDF.from_records(records)

	def get_confusion_matrix(self, X, y, actual_prefix='actual_', prediction_prefix='predicted_'):
		predictions = self.predict(X=X)
		self._confusion_matrix = confusion_matrix(y, predictions, labels=self.classes)
		return convert_confusion_matrix_to_df(
			confusion_matrix=self._confusion_matrix, classes=self.classes,
			actual_prefix=actual_prefix, prediction_prefix=prediction_prefix
		)

	def evaluate(self, X=None, y=None):
		if X is not None and y is not None:
			predictions = self.predict(X=X)
			self._confusion_matrix = confusion_matrix(y, predictions, labels=self.classes)
		elif X is None and y is not None:
			raise ValueError('y should be provided if X is provided!')
		elif X is not None and y is None:
			raise ValueError('X should be provided if y is provided!')
		elif self._confusion_matrix is None:
			raise RuntimeError('confusion matrix should exist when X and y are not provided!')

		return _evaluate_multiclass_classification(confusion_matrix=self._confusion_matrix, classes=self.classes)
