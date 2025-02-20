import argparse
import json
import pathlib


def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def validate_pr_config(pr_config_json):
    """
    Validates that ``RUN_SCORER`` is a Boolean, and ``REQUIREMENTS`` and
    ``SUBMISSION_MAIN`` are paths that point to existing files.

    This can throw a ``ValueError``, ``FileNotFoundError``,
    or ``RuntimeError``.

    Parameters
    ----------
    pr_config_json : dict
        A dictionary from environment variable names to their values.

    Returns
    -------
    dict
        A validated mapping from environment variables to to their values.
    """
    pr_config_validated = {}
    valid_keys_to_value_types = {'RUN_SCORER': bool,
                                 'REQUIREMENTS': pathlib.Path,
                                 'SUBMISSION_MAIN': pathlib.Path}

    for key, value_type in valid_keys_to_value_types.items():
        pr_config_validated[key] = value_type(pr_config_json[key])

    for k, v in valid_keys_to_value_types.items():
        if isinstance(v, pathlib.Path):
            valid_keys_to_value_types[k] = f"'{v}'"
            valid_keys_to_value_types[f'{k}_PATH'] = f"'{v.parent}'"

    return pr_config_validated


def format_bool_variables(key, validated_dict, options):
    """
    Converts ``validated_dict[key]`` from a bool to a bash-style Boolean
    string. This modifies ``validated_dict``. If ``validated_dict[key]`` is
    not a bool, nothing is done.

    This function does not check ``options``.

    Parameters
    ----------
    key : str
        A key of ``validated_dict``.

    validated_dict : dict
        A dict with key ``key`` where ``validated_dict[key]`` is possibly
        a bool.

    options : dict
        A dict containing options that affect the behavior of the functions
        called during the iteration.
    """
    value = validated_dict[key]
    if isinstance(value, bool):
        validated_dict[key] = 'true' if value else 'false'


def format_path_variables(key, validated_dict, options):
    """
    Converts ``validated_dict[key]`` from a ``pathlib.Path`` to a string
    containing the path in quotes. This modifies ``validated_dict``. If
    ``validated_dict[key]`` is not a ``pathlib.Path``, nothing is done.

    The ``options`` that are used by this function are:

    - ``split_path_variables`` : bool

      If ``split_path_variables`` is ``True``, two additional entires are added
      to ``validated_dict``:

      - ``{key}_FILENAME``: only the filename that ``validated_dict[key]`` points
        to.
      - ``{key}_PATH``: only the path to the parent folder containing the file
        ``validated_dict[key]`` points to.

    Parameters
    ----------
    key : str
        A key of ``validated_dict``.

    validated_dict : dict
        A dict with key ``key`` where ``validated_dict[key]`` is possibly
        a ``pathlib.Path``.

    options : dict
        A dict containing options that affect the behavior of the functions
        called during the iteration.
    """
    str_path = lambda path: str(path)
    quote_path = lambda path: f'"{path}"'
    if options.get('quote_path_variables', False):
        format_path = quote_path
    else:
        format_path = str_path

    value = validated_dict[key]
    if isinstance(value, pathlib.Path):
        validated_dict[key] = format_path(value)
        if options.get('split_path_variables', False):
            validated_dict[f'{key}_FILENAME'] = format_path(value.name)
            validated_dict[f'{key}_PATH'] = format_path(value.parent)


def format_variable_values(validated_dict, options):
    """
    Iterates through the keys of ``validated_dict`` and runs functions to
    modify their corresponding values.It allows for new keys to be added to
    ``validated_dict`` by the functions, but any new keys will not be iterated
    over.

    The functions called must have these three positional parameters:

    #. ``key``: The current key of the iteration.
    #. ``validated_dict``
    #. ``options``

    Parameters
    ----------
    validated_dict : dict
        A dict.

    options : dict
        A dict containing options that affect the behavior of the functions
        called during the iteration.
    """
    functions = [
        format_bool_variables,
        format_path_variables
    ]
    for k in list(validated_dict.keys()):
        for f in functions:
            f(k, validated_dict, options)


def print_json_as_env(validated_dict):
    """
    Iterates through ``validated_dict`` and prints the string
    ``'{key}={value}'``.
    """
    for k, v in validated_dict.items():
        print(f'{k}={v}')


def get_argparser():
    parser = argparse.ArgumentParser(
        description='Prints entries in flat JSON object like environment variables.'
    )
    parser.add_argument('path', type=str, help='Path to the JSON file.')
    parser.add_argument('--validate-pr-config', action=argparse.BooleanOptionalAction,
                        help='Runs the pr_config.json validator.')
    parser.add_argument('--split-path-variables', action=argparse.BooleanOptionalAction,
                        help='Adds two additional variables when a path variable P is encountered: a parent directory variable (P_PATH), and a filename variable (P_FILENAME).')
    parser.add_argument('--quote-path-variables', action=argparse.BooleanOptionalAction,
                        help='Wrap path variables in double quotes (").')
    return parser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    flat_json = load_json(args.path)

    if args.validate_pr_config:
        flat_json = validate_pr_config(flat_json)

    # Run bash environment variable formatting
    format_variable_values(flat_json, args.__dict__)

    print_json_as_env(flat_json)

