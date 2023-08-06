"""Package for esterdb."""

import gzip
from pathlib import Path
import shutil
from typing import Optional, Union
import os
import logging

import platform
import tempfile

import urllib.request

import duckdb

from esterdb.__about__ import __version__, EXTENSION_NAME


__all__ = ["get_connection", "run_query_file", "__version__"]

logger = logging.getLogger(__name__)


class WTTException(Exception):
    """Base exception for esterdb."""


class EsterDBConfigurationException(WTTException):
    """Exception for esterdb configuration."""


def run_query_file(
    con: duckdb.DuckDBPyConnection, file_path: Union[Path, str]
) -> duckdb.DuckDBPyConnection:
    """Run a query from a file."""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    return con.execute(file_path.read_text())


def get_connection(
    database: str = ":memory:",
    read_only: bool = False,
    config: Optional[dict] = None,
    file_path: Optional[Path] = None,
) -> duckdb.DuckDBPyConnection:
    """Return a connection with esterdb loaded."""
    if "ESTERDB_LICENSE" not in os.environ:
        raise EsterDBConfigurationException(
            "ESTERDB_LICENSE environment variable not set. "
            "Check the docs or email at help@wheretrue.com"
        )

    if config is None:
        config = {"allow_unsigned_extensions": True}
    else:
        config["allow_unsigned_extensions"] = True

    con = duckdb.connect(
        database=database,
        read_only=read_only,
        config=config,
    )

    try:
        con.load_extension(EXTENSION_NAME)
        return con
    except duckdb.IOException as exp:
        logger.info("Extension not found, installing. This only happens once per version/machine.")
        extension_path = os.getenv("ESTERDB_EXTENSION_PATH")

        if extension_path:
            extension_path = Path(extension_path).absolute()
            con.install_extension(str(extension_path), force_install=True)
            con.load_extension(EXTENSION_NAME)

        elif file_path is not None and file_path.exists():
            con.install_extension(str(file_path.absolute()), force_install=True)
            con.load_extension(EXTENSION_NAME)

        else:
            version = __version__
            name = "esterdb"

            platform_uname = platform.uname()
            operating_system = platform_uname.system
            architecture = platform_uname.machine

            if operating_system.lower() == "windows":
                duckdb_arch = "windows_amd64"
            elif operating_system.lower() == "darwin" and architecture.lower() == "x86_64":
                duckdb_arch = "osx_amd64"
            elif operating_system.lower() == "darwin" and architecture.lower() == "arm64":
                duckdb_arch = "osx_arm64"
            elif operating_system.lower() == "linux" and architecture.lower() == "x86_64":
                duckdb_arch = "linux_amd64_gcc4"
            else:
                raise WTTException(
                    f"Unable to find extension for {operating_system} {architecture}"
                )

            filename = f"{name}.duckdb_extension.gz"
            url = f"https://dbe.wheretrue.com/{name}/{version}/v0.8.0/{duckdb_arch}/{filename}"
            logger.info("Downloading extension from %s", url)

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)
                temp_file_name = temp_dir_path / filename

                try:
                    urllib.request.urlretrieve(url, temp_file_name)
                except Exception as exp:
                    raise WTTException(
                        f"Unable to download extension from {url}"
                    ) from exp

                output_file = temp_dir_path / filename.rstrip(".gz")
                with gzip.open(temp_file_name, "rb") as f_in:
                    with open(output_file, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)

                if not output_file.exists():
                    raise WTTException(
                        f"Unable to find extension file at {output_file}"
                    ) from exp

                logging.info("Installing extension from %s", output_file)
                con.install_extension(output_file.as_posix(), force_install=True)

                con.load_extension(EXTENSION_NAME)

    return con
