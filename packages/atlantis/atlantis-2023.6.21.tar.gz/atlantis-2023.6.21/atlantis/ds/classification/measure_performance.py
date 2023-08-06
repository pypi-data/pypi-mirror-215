from pyspark.sql import functions as f
from pyspark.sql import DataFrame
from pandas import DataFrame as PandasDF


def measure_performance_of_label(prediction_data, target_column, prediction_column, label):
    """
    :type prediction_data: DataFrame
    :type target_column:
    :type prediction_column:
    :type label: str
    :rtype: dict[str, float]
    """
    actual_predicted_df = prediction_data.select(
        f.col(target_column).alias('actual'), f.col(prediction_column).alias('predicted')
    ).groupby(
        'actual', 'predicted'
    ).agg(f.count(f.lit(1)).alias('count')).toPandas()

    actual_predicted_df['actual'] = (actual_predicted_df['actual'] == label).astype('int')
    actual_predicted_df['predicted'] = (actual_predicted_df['predicted'] == label).astype('int')
    actual_predicted_df = actual_predicted_df.groupby(['actual', 'predicted'], as_index=False).sum()
    try:
        dictionary = actual_predicted_df[['actual', 'predicted', 'count']].set_index(['actual', 'predicted']).to_dict()[
            'count']
        true_positive = dictionary.get((1, 1), 0)
        true_negative = dictionary.get((0, 0), 0)
        false_positive = dictionary.get((0, 1), 0)
        false_negative = dictionary.get((1, 0), 0)
    except KeyError as e:
        if actual_predicted_df.shape[0] == 0:
            true_positive = 0
            true_negative = 0
            false_positive = 0
            false_negative = 0
        else:
            raise e

    if true_positive == 0:
        precision = 0
        recall = 0
        f1_score = 0
    else:
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        f1_score = true_positive / (true_positive + 0.5 * (false_positive + false_negative))

    if true_positive + true_negative + false_positive + false_negative == 0:
        accuracy = 0
    else:
        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)

    return {
        'label': label,
        'true_negative': true_negative, 'false_positive': false_positive, 'false_negative': false_negative,
        'true_positive': true_positive, 'precision': precision, 'recall': recall, 'f1_score': f1_score,
        'accuracy': accuracy
    }

def measure_performance(prediction_data, target_column, prediction_column, labels):
    """
    :type prediction_data: DataFrame
    :type target_column:
    :type prediction_column:
    :type labels: list[str]
    :rtype: PandasDF
    """
    records = [
        measure_performance_of_label(
            label=label, prediction_data=prediction_data,
            target_column=target_column, prediction_column=prediction_column
        )
        for label in labels
    ]
    return PandasDF.from_records(records)
