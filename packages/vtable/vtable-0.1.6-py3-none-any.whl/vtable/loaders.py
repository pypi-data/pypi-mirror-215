from importlib import import_module
import pandas as pd

def fits_to_pandas(fits):
    df = pd.DataFrame(fits.tolist())
    df.columns = fits.columns.names
    return df 


class Loader:
    """A class to load data from filse of different formats, that doesn't fail when
    modules to load those files don't exist

    """

    def __init__(self):
        self.opts = {
            'csv': ('pandas.read_csv', None),
            'csv.gz': ('pandas.read_csv', None),
            'parquet': ('pandas.read_parquet', None),
            'fits': ('astropy.io.fits.getdata', fits_to_pandas),
        }

    def load(self, path):
        filetype = get_filetype(path)

        try:
            importstr, convertor = self.opts[filetype]
        except KeyError:
            raise ValueError(f"No loader defined for files of type {filetype}")

        package = ".".join(importstr.split('.')[:-1])
        func = importstr.split('.')[-1]
        pkg = import_module(package)
        # print(pkg)
        # func = eval(importstr)
        # func = eval(f"{pkg}.{func}")

        try:
            func = pkg.__dict__[func]
        except KeyError:
            raise ValueError(f"Package {package} has no function called {func}")

        df = func(path)
        if convertor is not None:
            df = convertor(df)
        return df 


def get_filetype(path):
    tokens = path.split('.')

    # If the suffix is gz, include previous suffix
    if tokens[-1] in "gz bz2".split():
        tokens[-1] = ".".join(tokens[-2:])

    return tokens[-1]

