from pyspark.sql.session import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.sql import functions as f
from pyspark.sql import DataFrame
from pyspark.sql.types import FloatType
from pandas import DataFrame as PandasDF
from amazonian import S3
from .Encoder import Encoder, Decoder
from .measure_performance import measure_performance
# from ..helpers.save_dictionary_as_dataframe import save_dictionary_as_dataframe, load_dictionary_as_dataframe


class Classifier:
    def __init__(
            self, feature_columns, target_column, negative_label, model, prediction_column=None,
            probability_column=None, probability_prefix=None, vectorized_features_column=None,
            encoded_prediction_column=None, raw_prediction_column=None,
            model_name=None,
            spark=None, s3=None
    ):
        """
        :type feature_columns: list[str]
        :type target_column: str
        :type prediction_column: str
        :type model: LogisticRegression
        :type spark: SparkSession or NoneType
        """
        if model_name is None:
            model_name = model.__class__.__name__

        if prediction_column is None:
            prediction_column = f'{target_column}_predicted'
        if probability_column is None:
            probability_column = f'{target_column}_probability'
        if probability_prefix is None:
            probability_prefix = f'{target_column}_'
        if vectorized_features_column is None:
            vectorized_features_column = f'{target_column}_features'
        if encoded_prediction_column is None:
            encoded_prediction_column = f'{target_column}_encoded_prediction'
        if raw_prediction_column is None:
            raw_prediction_column = f'{target_column}_raw_prediction'

        self._parameters = {
            'feature_columns': feature_columns,
            'target_column': target_column,
            'prediction_column': prediction_column,
            'probability_column': probability_column,
            'probability_prefix': probability_prefix,
            'vectorized_features_column': vectorized_features_column,
            'encoded_prediction_column': encoded_prediction_column,
            'raw_prediction_column': raw_prediction_column,
            'negative_label': negative_label,
            'model_name': model_name
        }
        if spark is None:
            spark = SparkSession.builder.getOrCreate()
        if s3 is None:
            s3 = S3()

        self._spark = spark
        self._s3 = s3
        self._model = model
        self._trained_model = None
        self._vector_assembler = VectorAssembler(inputCols=feature_columns, outputCol=vectorized_features_column)
        self._encoder = Encoder(column=target_column, negative_label=negative_label)
        self._decoder = None
        self._is_fit = False

    def copy(self, keep_trained=False):
        """
        :rtype: Classifier
        """
        model = self._model.copy()
        classifier_copy = self.__class__(spark=self._spark, s3=self._s3, model=model, **self._parameters)
        if keep_trained:
            if self._trained_model is not None and keep_trained:
                classifier_copy._trained_model = self._trained_model.copy()
            classifier_copy._encoder = self._encoder.copy()
            if self._decoder is not None:
                classifier_copy._decoder = self._decoder.copy()
            classifier_copy._is_fit = self._is_fit
        return classifier_copy

    @property
    def feature_columns(self):
        return self._parameters['feature_columns']

    @property
    def target_column(self):
        return self._parameters['target_column']

    @property
    def prediction_column(self):
        return self._parameters['prediction_column']

    @prediction_column.setter
    def prediction_column(self, prediction_column):
        self._parameters['prediction_column'] = prediction_column

    @property
    def probability_column(self):
        return self._parameters['probability_column']

    @probability_column.setter
    def probability_column(self, probability_column):
        self._parameters['probability_column'] = probability_column

    @property
    def probability_prefix(self):
        return self._parameters['probability_prefix']

    @probability_prefix.setter
    def probability_prefix(self, probability_prefix):
        self._parameters['probability_prefix'] = probability_prefix

    @property
    def vectorized_features_column(self):
        return self._parameters['vectorized_features_column']

    @property
    def encoded_prediction_column(self):
        return self._parameters['encoded_prediction_column']

    @property
    def raw_prediction_column(self):
        return self._parameters['raw_prediction_column']

    @property
    def negative_label(self):
        return self._parameters['negative_label']

    @property
    def model_name(self):
        return self._parameters['model_name']

    def fit(self, data):
        """
        :type data: DataFrame
        :rtype: ComprehensiveClassifier
        """
        if self._is_fit:
            raise RuntimeError('classifier is already fit')

        assembled_data = self._vector_assembler.transform(data)
        self._encoder.fit(data=assembled_data)
        self._decoder = Decoder(
            encoder=self._encoder, column=self.encoded_prediction_column, decoded_column=self.prediction_column
        )
        encoded_data = self._encoder.transform(data=assembled_data)
        model = self._model
        model.setFeaturesCol(self.vectorized_features_column)
        model.setLabelCol(self._encoder.encoded_column)
        model.setPredictionCol(self.encoded_prediction_column)
        model.setProbabilityCol(self.probability_column)
        model.setRawPredictionCol(self.raw_prediction_column)
        self._trained_model = model.fit(encoded_data)
        self._is_fit = True
        return self

    @classmethod
    def load(cls, path, spark=None, s3=None):
        if spark is None:
            spark = SparkSession.builder.getOrCreate()
        if s3 is None:
            s3 = S3()

        """parameters_dictionary = load_dictionary_as_dataframe(
            path=f'{path}/parameters.csv', spark=spark
        )"""
        parameters_dictionary = s3.load(path=f'{path}/parameters.pickle')
        pipeline = Pipeline.load(path=f'{path}/classifier.pipeline')
        model = pipeline.getStages()[0]
        classifier = cls(model=model, spark=spark, **parameters_dictionary)

        trained_model_path = f'{path}/trained_classifier.pipeline'
        trained_encoder_path = f'{path}/trained_encoder'

        exception = None
        try:
            trained_model_pipeline = Pipeline.load(path=trained_model_path)
            trained_model = trained_model_pipeline.getStages()[0]
            trained_model_loaded = True
        except Exception as exception:
            print(f'could not load trained_model from {trained_model_path}')
            trained_model = None
            trained_model_loaded = False

        try:
            trained_encoder = Encoder.load(path=trained_encoder_path, spark=spark)
            classifier._encoder = trained_encoder
            trained_encoder_loaded = True
        except Exception as exception:
            trained_encoder = None
            print(f'could not load encoder from {trained_encoder_path}')
            trained_encoder_loaded = False

        if trained_encoder is not None:
            trained_decoder = Decoder(
                encoder=trained_encoder, column=parameters_dictionary['encoded_prediction_column'],
                decoded_column=classifier.prediction_column
            )
            trained_decoder_loaded = True
        else:
            print(f'coult not build decoder from trained_encoder')
            trained_decoder = None
            trained_decoder_loaded = False

        if trained_model_loaded and trained_encoder_loaded and trained_decoder_loaded:
            classifier._trained_model = trained_model
            classifier._encoder = trained_encoder
            classifier._decoder = trained_decoder
            classifier._is_fit = True
            return classifier
        elif not (trained_model_loaded or trained_encoder_loaded or trained_decoder_loaded):
            return classifier
        else:
            raise exception

    def save(self, path, mode='overwrite'):
        """save_dictionary_as_dataframe(
            dictionary=self._parameters, path=f'{path}/parameters.csv', spark=self._spark
        )"""
        self._s3.save_pickle(obj=self._parameters, path=f'{path}/parameters.pickle', mode=mode)
        pipeline = Pipeline(stages=[self._model])
        if mode == 'overwrite':
            pipeline.write().overwrite().save(f'{path}/classifier.pipeline')
        else:
            pipeline.write().save(f'{path}/classifier.pipeline')

        if self._is_fit:
            trained_pipeline = Pipeline(stages=[self._trained_model])
            if mode == 'overwrite':
                trained_pipeline.write().overwrite().save(f'{path}/trained_classifier.pipeline')
            else:
                trained_pipeline.write().save(f'{path}/trained_classifier.pipeline')
            self._encoder.save(path=f'{path}/trained_encoder', mode=mode)

    def _transform_and_evaluate(self, data, evaluate):
        """
        :type data: DataFrame
        :rtype: dict[str, DataFrame or PandasDF]
        """
        if not self._is_fit:
            raise RuntimeError('model is not fit')

        if self.vectorized_features_column not in data.columns:
            assembled_data = self._vector_assembler.transform(data)
        else:
            assembled_data = data

        if evaluate:
            encoded_data = self._encoder.transform(data=assembled_data)
            encoded_predictions = self._trained_model.transform(encoded_data)
        else:
            encoded_predictions = self._trained_model.transform(assembled_data)

        predictions = self._decoder.transform(encoded_predictions)

        for index, label in self._decoder._mapping_dictionary.items():
            @f.udf(FloatType())
            def _get_probability_of_label(x):
                try:
                    return float(x[index])
                except:
                    return None

            probability_column = self._trained_model.getProbabilityCol()
            label_probability_column = f'probability_of_{self.probability_prefix}{str(label).lower().strip().replace(" ", "_")}'
            predictions = predictions.withColumn(
                label_probability_column, _get_probability_of_label(probability_column)
            )

        if evaluate:
            evaluation = measure_performance(
                prediction_data=predictions, labels=self._decoder.labels, target_column=self.target_column,
                prediction_column=self.prediction_column
            )
            evaluation['model_name'] = self.model_name
        else:
            evaluation = None

        return {'predictions': predictions, 'evaluation': evaluation}

    def evaluate(self, data):
        """
        :type data: DataFrame
        :rtype: PandasDF
        """
        results = self._transform_and_evaluate(data=data, evaluate=True)
        return results['evaluation']

    def transform(self, data):
        """
        :type data: DataFrame
        :rtype: DataFrame
        """
        results = self._transform_and_evaluate(data=data, evaluate=False)
        return results['predictions']
