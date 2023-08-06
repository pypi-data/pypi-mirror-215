import numpy as np
import pandas

from parse_function import FUNCTION_LENGTHS, PARAMETER_COUNT


def get_mean(series):
    mean = series.mean()
    if mean is np.nan:
        mean = None
    else:
        # 2 decimal places
        mean = float("{:.2f}".format(mean))
    return mean


def get_mode(series):
    mode = series.mode()
    if mode is np.nan:
        mode = None
    if len(mode) == 0:
        mode = None
    elif len(mode) > 0:
        mode = mode.tolist()
    return mode


def get_mean_median_mode_max_min(series):
    mean = get_mean(series)
    median = series.median()
    if median is np.nan:
        median = None
    mode = get_mode(series)
    max = series.max()
    if max is np.nan:
        max = None
    min = series.min()
    if min is np.nan:
        min = None
    d = {"mean": mean, "median": median, "mode": mode, "max": max, "min": min}
    return d


def get_statistics(series: pandas.Series, include_index=False):
    """
    Return the stats for a given series
    :param series
    :param include_index
    :return:
    """
    d = get_mean_median_mode_max_min(series)

    type = None
    try:
        type = series.type
    except AttributeError:
        # no type, ignore ...
        pass

    if type:
        d["type"] = type

    if include_index:
        d["function_names"] = series.index.tolist()

    return d


def filter_series_by_threshold(series, threshold):
    """
    Filter series by threshold
    :param series:
    :param threshold:
    :return:
    """
    series = series.loc[lambda x: x > threshold]
    return series


def get_function_lengths_over_threshold(series, threshold=25):
    series = filter_series_by_threshold(series, threshold)
    series.type = "function_lengths_over_threshold_" + str(threshold)
    return series


def get_parameter_count_over_threshold(series, threshold=4):
    series = filter_series_by_threshold(series, threshold)
    series.type = "parameter_count_over_threshold_" + str(threshold)
    return series


def apply_thresholds(series_list):
    series_list2 = []
    for series in series_list:
        if series.type == FUNCTION_LENGTHS:
            series2 = get_function_lengths_over_threshold(series)
        elif series.type == PARAMETER_COUNT:
            series2 = get_parameter_count_over_threshold(series)
        series_list2.append(series2)
    return series_list2


def filter_series_by_percentile(series, percentile=95):
    """
    Filter series by quartile
    :param series:
    :param percentile:
    :return:
    """
    series = series.loc[lambda x: x > np.percentile(x, percentile)]
    # TODO - use the old type as suffix ...
    series.type = "percentile_" + str(percentile)
    return series


def filter_by_percentile(series_list, percentile=95):
    series_list2 = []
    for series in series_list:
        series = filter_series_by_percentile(series, percentile)
        series_list2.append(series)
    return series_list2
