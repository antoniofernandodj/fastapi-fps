
from dynaconf import Dynaconf  # type: ignore
import pathlib
import os

THIS_DIR = str(pathlib.Path(__file__).parent)

files = [
    os.path.join(THIS_DIR, f)
    for f in ['settings.toml', '.secrets.toml']
]

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=files,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
