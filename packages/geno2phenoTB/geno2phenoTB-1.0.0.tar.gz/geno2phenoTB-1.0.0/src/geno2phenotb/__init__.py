"""Init of geno2phenotb package."""


from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "geno2phenoTB"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

__author__ = "Bernhard Reuter, Jules Kreuer"
__maintainer__ = "Bernhard Reuter"
__email__ = "bernhard-reuter@gmx.de"
