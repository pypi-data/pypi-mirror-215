import os

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="ABIN",
    root_path=os.path.dirname(f"{os.environ['HOME']}/abin_sim/"),
    settings_files=[ "settings.toml", ],
)
