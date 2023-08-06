"""
Documentar.
"""
import dynaconf
from rds_core.helpers import env

environment = env("ENVIRONMENT", "local")

settings = dynaconf.Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[f"settings.{environment}.{ext}" for ext in ["yaml", "toml"]],
)
