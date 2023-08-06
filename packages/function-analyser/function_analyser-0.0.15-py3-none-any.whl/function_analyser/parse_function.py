import ast
import os
import pandas
from pandas import Series

FUNCTION_LENGTHS = "function_lengths"
PARAMETER_COUNT = "parameter_count"


def get_function_length(function_def: ast.FunctionDef):
    """
    return the length of an ast functiondef node
    :param function_def:
    :return: int
    """
    try:
        function_length = int(function_def.end_lineno - function_def.lineno)
    except Exception as e:
        # not an integer ...
        return None

    return function_length


def parse_functions(tree):
    """
    Parse functions in an AST tree
    :param tree:
    :return:
    """
    function_names = []
    function_lengths = []
    parameter_counts = []
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    for node in functions:
        parameter_count = len(node.args.args)
        function_length = get_function_length(node)
        if function_length and parameter_count:
            function_names.append(node.name)
            parameter_counts.append(parameter_count)
            function_lengths.append(function_length)

    return {"function_names": function_names, FUNCTION_LENGTHS: function_lengths, PARAMETER_COUNT: parameter_counts}


def parse_classes(tree):
    """
    Parse the classes in an AST tree
    :param tree:
    :return:
    """
    function_names = []
    function_lengths = []
    parameter_count = []
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    for clazz in classes:
        class_methods = [n for n in clazz.body if isinstance(n, ast.FunctionDef)]
        for node in class_methods:
            function_names.append(clazz.name + "." + node.name)
            parameter_count.append(len(node.args.args))
            function_lengths.append(get_function_length(node))

    return {"function_names": function_names, FUNCTION_LENGTHS: function_lengths, PARAMETER_COUNT: parameter_count}


def get_file_list(base_path, exclusion_list):
    file_list = []
    extension = ".py"
    exclude_directories = set(exclusion_list)
    for dname, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in exclude_directories]
        for fname in files:
            if fname.lower().endswith(extension):
                file_path = os.path.join(dname, fname)
                file_list.append(file_path)
    return file_list


def parse_files(file_path, config):
    """
    Parse files

    :param file_path:
    :param file_type:
    :param threshold:
    :return:
    """
    file_list = get_file_list(file_path, config.get("exclusions", []))

    print(f"Parsing {len(file_list)} source files in {file_path} ...")

    d = {}
    for file_item in file_list:
        with open(file_item) as file:
            file_series_list = parse_file(file)
            if file_series_list is None:
                continue
            for series in file_series_list:
                series_by_type = d.get(series.type)
                if isinstance(series_by_type, Series):
                    new_series = pandas.concat([series_by_type, series])
                    new_series.type = series.type
                    d[series.type] = new_series
                else:
                    d[series.type] = series

    series_list = []
    for key in d.keys():
        series_list.append(d[key])
    return series_list


def create_series(data: list, index: list, file_name, type=None):
    """
    Factory method for pandas series
    :param data:
    :param index:
    :param file_name:
    :param type:
    :return:
    """
    # create a series ...
    series = pandas.Series(data=data, index=index)
    series.filename = file_name
    if type is not None:
        series.type = type
    return series


def parse_file(file):
    """
    Pass in a file and yield function lengths
    :param file:
    :param function_length_threshold
    :param parameter_count_threshold
    :return:
    """
    # parse the file ...
    try:
        tree = ast.parse(file.read())
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Unable to parse file {file}, {e}")
        return None

    d1 = parse_functions(tree)
    d2 = parse_classes(tree)

    # concatenate the lists ...
    function_names = [*d1["function_names"], *d2["function_names"]]
    function_lengths = [*d1[FUNCTION_LENGTHS], *d2[FUNCTION_LENGTHS]]
    parameter_count = [*d1[PARAMETER_COUNT], *d2[PARAMETER_COUNT]]

    function_length_series = create_series(function_lengths, function_names, file.name, FUNCTION_LENGTHS)
    parameter_count_series = create_series(parameter_count, function_names, file.name, PARAMETER_COUNT)

    series_list = [function_length_series, parameter_count_series]
    return series_list


