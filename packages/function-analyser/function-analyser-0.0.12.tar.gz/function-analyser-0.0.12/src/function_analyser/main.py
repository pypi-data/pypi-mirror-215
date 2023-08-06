import argparse
import os
import pathlib

from function_analyser.parse_function import parse_files
from function_analyser.statistics import get_statistics, filter_by_percentile


def parse_args():
    parser = argparse.ArgumentParser(description='Function analysis')
    parser.add_argument('-f', '--filepath', help='Source file path to analyse', required=False)
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()
    if args["filepath"]:
        file_path = args["filepath"]
    else:
        file_path = os.getcwd()

    series_list = parse_files(file_path)
    if len(series_list) > 0:
        for series in series_list:
            print(get_statistics(series))

        # use percentiles over specific thresholds ...
        series_list2 = filter_by_percentile(series_list)
        for series in series_list2:
            # note - we want the function names (i.e. index) as well ...
            print(get_statistics(series, include_index=True))

        # extract main offender (-1 being last in list) ...
        worst_offender = series_list2[0].index[-1]
        print(f"Best contender / Worst offender is {worst_offender}")
    else:
        print("No source files found.")


if __name__ == '__main__':
    main()
