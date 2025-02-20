import os
import csv
import pathlib
from mpmath import mp


TEST_SETS_DIR = f'{pathlib.Path(__file__).parent}/../test_sets'
IV_PARAMETER_NAMES = ['photocurrent', 'saturation_current',
                      'resistance_series', 'resistance_shunt', 'n',
                      'cells_in_series']


def set_globals():
    r"""
    Sets library parameters that must be the same whenever the libraries are
    imported.

    ivcurves scripts should import these libraries from this script's
    namespace to use these library parameter settings.

    The following are set:

    - ``mpmath``: The precision of calculations (``mp.dps``) is set to 40
      decimal places.
    """
    mp.dps = 40 # set precision, 16*2 rounded up


def constants():
    r"""
    Commonly used constants of the ivcurves scripts.
    """
    num_pts = 100
    precision = 16
    atol = mp.mpmathify(1e-16)

    # Boltzmann's const (J/K), electron charge (C), temp (K)
    k, q, temp_cell = map(mp.mpmathify, [1.380649e-23, 1.60217663e-19, 298.15])
    vth = (k * temp_cell) / q

    return {'k': k, 'q': q, 'temp_cell': temp_cell, 'vth': vth, 'atol': atol,
            'precision': precision, 'num_pts': num_pts}


def mp_num_digits_left_of_decimal(num_mpf):
    r"""
    Finds the number of digits to the left of an mpmath float's decimal point.
    If the mpmath float is strictly between -1 and 1, the number of digits
    is zero.

    Parameters
    ----------
    num_mpf : numeric
        The mpmath float. [-]

    Returns
    -------
    int
        The number of digits to the left of the decimal point of ``num_mpf``,
        ignoring leading zeros.
    """
    if abs(num_mpf) < 1:
        # ignore leading zero
        return 0
    else:
        precision = constants()['precision']
        # force mpf to string in decimal format, no scientific notation
        # mpf string will have precision*2 significant digits
        # all leading zeros are stripped
        return mp.nstr(num_mpf, n=precision*2, min_fixed=-mp.inf,
                       max_fixed=mp.inf).find('.')


def mp_nstr_precision_func(num_mpf):
    r"""
    Converts an mpmath float to a string with 16 significant digits
    after the decimal place.

    Parameters
    ----------
    num_mpf : numeric
        The mpmath float. [-]

    Returns
    -------
    str
        A string representation of ``num_mpf`` with 16 significant digits
        after the decimal place.
    """
    precision = constants()['precision']
    ldigits = mp_num_digits_left_of_decimal(num_mpf)
    return mp.nstr(num_mpf, n=ldigits+precision, strip_zeros=False)


def read_iv_curve_parameter_sets(filename):
    r"""
    Returns a dictionary of indices to a list of these values:
    Index, photocurrent, saturation_current, resistance_series,
    resistance_shunt, n, and cells_in_series.
    The indices and values are read from the CSV file at ``filename``.

    Parameters
    ----------
    filename : str
        The path to a CSV file with these column names:
        Index, photocurrent, saturation_current, resistance_series,
        resistance_shunt, n, and cells_in_series.
        The path must exclude the file extension.

    Returns
    -------
    dict
    """
    with open(f'{filename}.csv', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        mapping = {}
        for row in reader:
            mapping[int(row['Index'])] = [mp.mpmathify(row[col])
                                            for col in IV_PARAMETER_NAMES]
        return mapping


def make_iv_curve_name(test_set_name, index):
    r"""
    Returns a unique name for an IV curve created from parameters of
    a test set's test case. The unique name is of the form
    ``'{test_set_name}_case_{index}'``.

    Parameters
    ----------
    test_set_name : str
        The name of the test set that contains the test case of the IV curve's
        parameters.

    index : int
        The Index of the test case of the IV curve's parameters.

    Returns
    -------
    str
        A unique name for the IV curve.
    """
    return f'{test_set_name}_case_{index}'


def get_filenames_in_directory(directory_path):
    """
    Returns a set of entries in the directory ``directory_path``.
    The filenames do not have file extensions.

    Returns
    -------
    set
        A set of filenames without file extensions.
    """
    return {entry.stem for entry in pathlib.Path(directory_path).iterdir()}


set_globals()

