"""Package for esterdb."""

from esterdb.__about__ import __version__
from esterdb.main import get_connection, run_query_file

__all__ = ["get_connection", "run_query_file", "__version__"]
