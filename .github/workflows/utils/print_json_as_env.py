import argparse
import json
import pathlib


def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def py_to_json_bool(bool_value):
    return 'true' if bool_value else 'false'


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
    json_bool = lambda bool_v: py_to_json_bool(bool(bool_v))
    absolute_path = lambda path: pathlib.Path(path).resolve()
    valid_keys_to_value_types = {'RUN_SCORER': json_bool,
                                 'REQUIREMENTS': absolute_path,
                                 'SUBMISSION_MAIN': absolute_path}

    for key, value_type in valid_keys_to_value_types.items():
        pr_config_validated[key] = value_type(pr_config_json[key])

    return pr_config_validated


def print_json_as_env(flat_json):
    for k, v in flat_json.items():
        print(f'{k}={v}')


def get_argparser():
    parser = argparse.ArgumentParser(
        description='Prints entires in flat JSON object like environment variables.'
    )
    parser.add_argument('path', type=str, help='Path to the JSON file')
    parser.add_argument('--validate-pr-config', action=argparse.BooleanOptionalAction,
                        help='Runs the pr_config.json validator.')
    return parser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    flat_json = load_json(args.path)

    if args.validate_pr_config:
        flat_json = validate_pr_config(flat_json)

    print_json_as_env(flat_json)

