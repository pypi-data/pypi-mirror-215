from pyspark.ml.classification import RandomForestClassifier
from ._PySparkModel import PySparkClassifier


PARAM_ALIASES = {
	'n_trees': 'numTrees',
	'max_depth': 'maxDepth'
}

class PySparkRandomForestClassifier(PySparkClassifier):
	def __init__(
			self, input_variables, output_variable, prediction_column='predicted', probability_column='probability',
			seed=42,
			**kwargs
	):
		super().__init__(
			input_variables=input_variables, output_variable=output_variable,
			prediction_column=prediction_column, probability_column=probability_column, **kwargs
		)

		kwargs = {}
		for key, value in self._inital_kwargs.items():
			if key in PARAM_ALIASES:
				kwargs[PARAM_ALIASES[key]] = value
			else:
				kwargs[key] = value

		self._untrained_classifier = RandomForestClassifier(
			labelCol=self.output_variable, featuresCol='assembler_features', predictionCol=self.prediction_column,
			probabilityCol=self.probability_column, seed=seed, **kwargs
		)

