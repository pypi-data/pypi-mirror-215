from pandas import DataFrame as PandasDF
from pyspark.sql import DataFrame as SparkDF


def assert_has_columns(df, columns):
    """
    :type df: PandasDF or SparkDF
    :type columns: str or list[str]
    """

    if isinstance(columns, str):
        columns = [columns]

    df_columns = list(df.columns)
    missing = [col for col in columns if col not in df_columns]
    if len(missing) > 0:
        message1 = f'Missing columns: "{", ".join(missing)}"'
        message2 = f'but has columns: "{", ".join(df_columns)}"'
        if len(message2) > 300:
            message2 = message2[:200] + ' ... ' + message2[-95:]
        message = message1 + '\n' + message2
        print(message)
        raise KeyError(message)
    else:
        return True
